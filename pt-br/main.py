import random

#50 itens para cada um ser um index da Memória Principal, vamos baser no Minecraft
ITENS = ["Madeira", "Pedra", "Ferro", "Lã", "Carne", "Areia", "Vidro", "Balde", "Maçã", "Neve", "Terra", "Basalto", "Granito", "Grevilha", "Ouro", "Diamante", "Carvão", "Cobre", "Argila", "Osso", "Pena", "Linha", "Trigo", "Papel", "Livro", "Açúcar", "Mel", "Cera", "Lapis", "Redstone", "Quartzo", "Obsidiana", "Gelo", "Cristal", "Aluminio", "Ametista", "Batata", "Beterraba", "Melancia", "Abobora", "Cenoura", "Menta", "Tijolo", "Cogumelo", "Magma", "Isqueiro", "Ovo", "Bambu", "Fornalha", "Rubi"]

def criar_memoria_principal(tamanho=50):
    memoria = []
    for i in range(tamanho):
        item = random.choice(ITENS)
        quantidade = random.randint(1,100)
        dado = f"{item}:{quantidade}"
        memoria.append(dado)
    return memoria

MEMORIA_PRINCIPAL = criar_memoria_principal()

def mostrar_memoria_principal():
    print("Linha | Dado")
    for i in range(50):
        print(f"{i:<5} | {MEMORIA_PRINCIPAL[i]}")


#Classe de apenas uma linha da Cache
class LinhadaCache:
    def __init__(self):
        self.tag = None
        self.dado = None
        self.estado = "I"
   
    def __repr__(self):
        return f"Tag = {self.tag}, Dado = {self.dado}, Estado = {self.estado}"
   
#Classe da Cache em geral
class Cache:
    #inicializa a classe Cache com cinco linhas, cada linha sendo uma classe LinhadCache
    def __init__(self,tamanho=5):
        self.linhas = [LinhadaCache() for i in range(tamanho)]
        self.fifo = []


    #apresenta a cache num modelo específico
    def mostrar_cache(self):
        print(" Linha | Tag  |   Dado   | Estado")
        print("-------------------------------")
        i = 0
        for linha in self.linhas:
            print(f"{i:<6} | {str(linha.tag):<4} | {str(linha.dado):<8} | {linha.estado}")
            i += 1
        print("-------------------------------")
   
    #busca por uma tag, retorna a linha caso hit, e None caso Miss
    def buscar_na_cache(self,tag):
        for linha in self.linhas:
            if linha.tag == tag and linha.estado != "I":
                return linha
        return None
   
    def write_back(self, linha):
        if linha is None:
            return
        # linha.estado == "O"'
        # O estado Owned significa que a memória está desatualizada, então é necessario salvar
        if linha.estado == "M" or linha.estado == "O":
            MEMORIA_PRINCIPAL[linha.tag] = linha.dado
            # print para visualizar quando isso acontece
            print(f"--> WRITE-BACK: O item da tag {linha.tag} voltou para o baú principal.")

    
    def carrega_bloco(self,tag:int,dados_owner:str = None):
        #linha livre
        i = 0
        for linha in self.linhas:
            if linha.tag is None or linha.estado == "I":
                return self.inserir_na_linha(i,tag,dados_owner)
            i += 1
        #fifo
        index_sub = self.fifo.pop(0)
        linha_sub = self.linhas[index_sub]
        self.write_back(linha_sub)
        return self.inserir_na_linha(index_sub,tag)

    
    def inserir_na_linha(self,indice:int,tag:int,dados_owner:str =None):
        #coloca asa novas informações na linha, o estado fica temporário
        linha = self.linhas[indice]
        linha.tag = tag
        if dados_owner is not None:
            linha.dado = dados_owner
        else:
            linha.dado = MEMORIA_PRINCIPAL[tag]
        linha.estado = "E"
        if indice in self.fifo:
            self.fifo.remove(indice)
        self.fifo.append(indice)
        return linha
   

#desccobrir quais caches tem a tag especifica            
def tag_nas_caches(tag:int):
    resultado = []
    for cache in CACHES:
        for linha in cache.linhas:
            if linha.tag == tag and linha.estado != "I":
                resultado.append((cache, linha))
    return resultado


#faz a LEITURA de uma tag na cache, caso esa tag já esta na cache n muda nada, caso n esteja, ve se as outras caches ja possuem o dado, e altera seus estados
# e adiciona esse dado tbm na cache desejada, ja com o novo estado, alterado
def ler(cache,tag):
    linha = cache.buscar_na_cache(tag)
    if linha is not None:
        print(f"READ HIT - Estado era {linha.estado}")
        return linha.dado
    else:
        print(f"READ MISS")
        resto = tag_nas_caches(tag)
        if len(resto) == 0:
            nova_linha = cache.carrega_bloco(tag,dados_owner=None)
            nova_linha.estado = "E"
            return nova_linha.dado
        owner = None
        for cache_compartilhada, linha_compartilhda in resto:
            if linha_compartilhda.estado == "M" or linha_compartilhda.estado == "O":
                owner = (cache_compartilhada, linha_compartilhda)
                break
        if owner is not None:
            cache_o , linha_o = owner
            if linha_o.estado == "M":
                linha_o.estado = "O"
            novo_dado = linha_o.dado
            nova_linha = cache.carrega_bloco(tag,dados_owner=novo_dado)
            nova_linha.estado = "S"
            return nova_linha.dado
        for cache_compartilhada,linha_compartilhda in resto:
            if linha_compartilhda.estado == "E":
                linha_compartilhda.estado = "S"
        nova_linha = cache.carrega_bloco(tag,dados_owner = None)
        nova_linha.estado = "S"
        return nova_linha.dado


#faz a escrita em uma cache, caso esta já possua o valor, altera-se seu estado e o das outras dependendo
def escrita(cache,tag,novo_dado):
    linha = cache.buscar_na_cache(tag)
    if linha is not None:
        print(f"WRITE HIT - Estado é {linha.estado}")
        if linha.estado == "M":
            linha.dado = novo_dado
            return
        if linha.estado == "E":
            linha.estado = "M"
            linha.dado = novo_dado
            return
        if linha.estado == "S":
            for cache_compartilhada, linha_compartilhada in tag_nas_caches(tag):
                if cache_compartilhada != cache:
                    linha_compartilhada.estado = "I"
            linha.estado = "M"
            linha.dado = novo_dado
            return
        if linha.estado == "O":
            for cache_compartilhada, linha_compartilhada in tag_nas_caches(tag):
                if cache_compartilhada != cache:
                    linha_compartilhada.estado = "I"        
            linha.estado = "M"
            linha.dado = novo_dado
            return
    else:
        print(f"WRITE MISS - carregando bloco {tag} para escrita...")
        for cache_compartilhada, linha_compartilhada in tag_nas_caches(tag):
            if linha_compartilhada != cache:
                linha_compartilhada.estado = "I"
       
        nova_linha = cache.carrega_bloco(tag)
        nova_linha.estado = "M"
        nova_linha.dado = novo_dado


def quantidade_atual(dado):
    item, qtd = dado.split(":")
    return item, int(qtd)


def ver_item(cache,tag):
    dado = ler(cache,tag)
    item, qtd = quantidade_atual(dado)
    print(f"Item: {item} | Quantidade: {qtd}")


def pegar_item(cache,tag,quantidade_desejada):
    dado = ler(cache,tag)
    item, qtd = quantidade_atual(dado)
    if quantidade_desejada > qtd:
        print("Não há itens suficientes no baú!")
        return
    else:
        nova_qtd = qtd - quantidade_desejada
        novo_dado = f"{item}:{nova_qtd}"
        escrita(cache,tag,novo_dado)
        print(f"Você pegou {quantidade_desejada} de {item},  ainda restam {nova_qtd}")


def adicionar_item(cache,tag,quantidade):
    dado = ler(cache,tag)
    item, qtd = quantidade_atual(dado)
    nova_qtd = quantidade + qtd
    novo_dado = f"{item}:{nova_qtd}"
    escrita(cache,tag,novo_dado)
    print(f"Você adicionou {quantidade} de {item}, agora temos {nova_qtd}")


def mostar_bau():
    print()
    print("----- BAÚ (MEMÓRIA PRINCIPAL) -----")
    for i in range(50):
        print(f"{i} | {MEMORIA_PRINCIPAL[i]}")
    print("=====================================")


def escolher_player():
    print("Escolha o seu jogador:")
    print("1 - Player 1")
    print("2 - Player 2")
    print("3 - Player 3")
    escolha = int(input(">> "))
    if escolha == 1:
        return Player1
    elif escolha == 2:
        return Player2
    elif escolha == 3:
        return Player3
    else:
        print("Escolha números de 1 a 3!")
        return escolher_player()


def menu():
    while True:
        print(" ")
        print("--------- MENU DO BAÚ ---------")
        print("1 - Ver um item")
        print("2 - Pegar um item")
        print("3 - Adicionar item")
        print("4 - Ver memória principal")
        print("5 - Ver cache do jogador")
        print("6 - Sair :(")
        escolha = int(input(">> "))
        print(" ")
        if escolha in [1,2,3,5]:
            player = escolher_player()
        if escolha == 1:
            print(" ")
            tag = int(input("Espaço do item (0-49): "))
            ver_item(player, tag)
        if escolha == 2:
            print(" ")
            tag = int(input("Espaço do item (0-49): "))
            qtd = int(input("Quantidade para pegar: "))
            pegar_item(player,tag,qtd)
        if escolha == 3:
            print(" ")
            tag = int(input("Espaço do item (0-49): "))
            qtd = int(input("Quantidade a ser adicionada: "))
            adicionar_item(player, tag, qtd)
        if escolha == 4:
            print(" ")
            mostar_bau()
        if escolha == 5:
            print(" ")
            player.mostrar_cache()
        if escolha == 6:
            print(" ")
            print("Encerrando...")
            break
        if escolha > 6 or escolha < 1:
            print(" ")
            print("Valor inválido! Reconectando...")
            menu()



#Criando cache para os 3 processadores (aq a gnt ta usando players como processadores, então são os 3 jogadores)
Player1 = Cache()
Player2 = Cache()
Player3 = Cache()
CACHES = [Player1,Player2,Player3]


menu()
