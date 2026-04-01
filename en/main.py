import random

# 50 items representing Main Memory positions (Minecraft-inspired)
ITEMS = ["Wood", "Stone", "Iron", "Wool", "Meat", "Sand", "Glass", "Bucket", "Apple", "Snow",
         "Dirt", "Basalt", "Granite", "Gravel", "Gold", "Diamond", "Coal", "Copper", "Clay",
         "Bone", "Feather", "String", "Wheat", "Paper", "Book", "Sugar", "Honey", "Wax",
         "Lapis", "Redstone", "Quartz", "Obsidian", "Ice", "Crystal", "Aluminum", "Amethyst",
         "Potato", "Beetroot", "Watermelon", "Pumpkin", "Carrot", "Mint", "Brick",
         "Mushroom", "Magma", "FlintAndSteel", "Egg", "Bamboo", "Furnace", "Ruby"]


def create_main_memory(size=50):
    memory = []
    for i in range(size):
        item = random.choice(ITEMS)
        quantity = random.randint(1, 100)
        data = f"{item}:{quantity}"
        memory.append(data)
    return memory


MAIN_MEMORY = create_main_memory()


def show_main_memory():
    print("Line | Data")
    for i in range(50):
        print(f"{i:<5} | {MAIN_MEMORY[i]}")


class CacheLine:
    def __init__(self):
        self.tag = None
        self.data = None
        self.state = "I"

    def __repr__(self):
        return f"Tag = {self.tag}, Data = {self.data}, State = {self.state}"


class Cache:
    def __init__(self, size=5):
        self.lines = [CacheLine() for _ in range(size)]
        self.fifo = []

    def show_cache(self):
        print(" Line | Tag  |   Data   | State")
        print("-------------------------------")
        for i, line in enumerate(self.lines):
            print(f"{i:<6} | {str(line.tag):<4} | {str(line.data):<8} | {line.state}")
        print("-------------------------------")

    def search_cache(self, tag):
        for line in self.lines:
            if line.tag == tag and line.state != "I":
                return line
        return None

    def write_back(self, line):
        if line is None:
            return
        if line.state in ["M", "O"]:
            MAIN_MEMORY[line.tag] = line.data
            print(f"--> WRITE-BACK: Tag {line.tag} returned to main memory.")

    def load_block(self, tag, owner_data=None):
        for i, line in enumerate(self.lines):
            if line.tag is None or line.state == "I":
                return self.insert_line(i, tag, owner_data)

        index = self.fifo.pop(0)
        line = self.lines[index]
        self.write_back(line)
        return self.insert_line(index, tag, owner_data)

    def insert_line(self, index, tag, owner_data=None):
        line = self.lines[index]
        line.tag = tag
        line.data = owner_data if owner_data else MAIN_MEMORY[tag]
        line.state = "E"

        if index in self.fifo:
            self.fifo.remove(index)
        self.fifo.append(index)

        return line


def find_tag_in_caches(tag):
    result = []
    for cache in CACHES:
        for line in cache.lines:
            if line.tag == tag and line.state != "I":
                result.append((cache, line))
    return result


def read(cache, tag):
    line = cache.search_cache(tag)
    if line:
        print(f"READ HIT - State was {line.state}")
        return line.data

    print("READ MISS")
    others = find_tag_in_caches(tag)

    if not others:
        new_line = cache.load_block(tag)
        new_line.state = "E"
        return new_line.data

    owner = None
    for c, l in others:
        if l.state in ["M", "O"]:
            owner = (c, l)
            break

    if owner:
        c, l = owner
        if l.state == "M":
            l.state = "O"
        new_line = cache.load_block(tag, l.data)
        new_line.state = "S"
        return new_line.data

    for c, l in others:
        if l.state == "E":
            l.state = "S"

    new_line = cache.load_block(tag)
    new_line.state = "S"
    return new_line.data


def write(cache, tag, new_data):
    line = cache.search_cache(tag)

    if line:
        print(f"WRITE HIT - State is {line.state}")

        if line.state == "M":
            line.data = new_data
            return

        if line.state == "E":
            line.state = "M"
            line.data = new_data
            return

        if line.state in ["S", "O"]:
            for c, l in find_tag_in_caches(tag):
                if c != cache:
                    l.state = "I"

            line.state = "M"
            line.data = new_data
            return

    print(f"WRITE MISS - loading block {tag}...")
    for c, l in find_tag_in_caches(tag):
        if c != cache:
            l.state = "I"

    new_line = cache.load_block(tag)
    new_line.state = "M"
    new_line.data = new_data


def parse_data(data):
    item, qty = data.split(":")
    return item, int(qty)


def view_item(cache, tag):
    data = read(cache, tag)
    item, qty = parse_data(data)
    print(f"Item: {item} | Quantity: {qty}")


def take_item(cache, tag, amount):
    data = read(cache, tag)
    item, qty = parse_data(data)

    if amount > qty:
        print("Not enough items!")
        return

    new_qty = qty - amount
    write(cache, tag, f"{item}:{new_qty}")
    print(f"You took {amount} of {item}. Remaining: {new_qty}")


def add_item(cache, tag, amount):
    data = read(cache, tag)
    item, qty = parse_data(data)

    new_qty = qty + amount
    write(cache, tag, f"{item}:{new_qty}")
    print(f"You added {amount} of {item}. Total: {new_qty}")


def show_chest():
    print("\n----- MAIN MEMORY (CHEST) -----")
    for i in range(50):
        print(f"{i} | {MAIN_MEMORY[i]}")
    print("=================================")


def choose_player():
    print("Choose player:")
    print("1 - Player 1")
    print("2 - Player 2")
    print("3 - Player 3")

    choice = int(input(">> "))
    if choice == 1:
        return Player1
    elif choice == 2:
        return Player2
    elif choice == 3:
        return Player3
    else:
        print("Invalid choice!")
        return choose_player()


def menu():
    while True:
        print("\n------ CHEST MENU ------")
        print("1 - View item")
        print("2 - Take item")
        print("3 - Add item")
        print("4 - Show main memory")
        print("5 - Show cache")
        print("6 - Exit")

        choice = int(input(">> "))

        if choice in [1, 2, 3, 5]:
            player = choose_player()

        if choice == 1:
            tag = int(input("Memory index (0-49): "))
            view_item(player, tag)

        elif choice == 2:
            tag = int(input("Memory index (0-49): "))
            qty = int(input("Amount: "))
            take_item(player, tag, qty)

        elif choice == 3:
            tag = int(input("Memory index (0-49): "))
            qty = int(input("Amount: "))
            add_item(player, tag, qty)

        elif choice == 4:
            show_chest()

        elif choice == 5:
            player.show_cache()

        elif choice == 6:
            print("Exiting...")
            break


Player1 = Cache()
Player2 = Cache()
Player3 = Cache()
CACHES = [Player1, Player2, Player3]

menu()