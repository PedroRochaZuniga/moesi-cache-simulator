# moesi-cache-simulator
# 🧠 MOESI Cache Coherence Simulation

🌎 [Read in English](#-english) | 🇧🇷 [Leia em Português](#-português)

---

## 🇺🇸 English

### 📌 About

This project is a simulation of the **MOESI cache coherence protocol**, developed in **2025** as part of studies in Computer Architecture.

It models a simplified multiprocessor system where multiple caches interact with a shared main memory. To make the simulation more intuitive, a **Minecraft-inspired inventory system** was used, where each memory position represents an item and its quantity.

---

### ⚙️ Features

* Simulation of MOESI protocol states:

  * Modified (M)
  * Owned (O)
  * Exclusive (E)
  * Shared (S)
  * Invalid (I)
* Multi-cache environment (3 processors/players)
* Read and write operations (hit/miss)
* FIFO cache replacement policy
* Write-back mechanism
* Interactive command-line interface
* Randomized main memory

---

### 🧠 Concepts Covered

* Computer Architecture
* Cache Coherence Protocols
* MOESI Protocol
* Memory Hierarchy
* State Machines
* Multiprocessor Systems
* Object-Oriented Programming (OOP)

---

### 🎮 Design Idea

The system uses a **Minecraft-style chest** as an abstraction:

* Each memory address stores an item and its quantity
* Players represent processors (each with its own cache)
* Operations simulate real cache access and modification

---

### ▶️ How to Run

```bash
python main.py
```

---

⚠️ **Note:**
This project reflects my knowledge in 2025 and was developed for educational purposes, focusing on understanding cache coherence mechanisms.

---

## 🇧🇷 Português

### 📌 Sobre

Este projeto é uma simulação do **protocolo de coerência de cache MOESI**, desenvolvido em **2025** como parte dos estudos em Arquitetura de Computadores.

Ele modela um sistema multiprocessado simplificado, onde múltiplas caches interagem com uma memória principal compartilhada. Para tornar a simulação mais intuitiva, foi utilizado um sistema inspirado no **Minecraft**, onde cada posição da memória representa um item e sua quantidade.

---

### ⚙️ Funcionalidades

* Simulação dos estados do protocolo MOESI:

  * Modified (M)
  * Owned (O)
  * Exclusive (E)
  * Shared (S)
  * Invalid (I)
* Ambiente com múltiplas caches (3 processadores/jogadores)
* Operações de leitura e escrita (hit/miss)
* Política de substituição FIFO
* Mecanismo de write-back
* Interface interativa via terminal
* Memória principal com dados aleatórios

---

### 🧠 Conceitos Utilizados

* Arquitetura de Computadores
* Protocolos de Coerência de Cache
* Protocolo MOESI
* Hierarquia de Memória
* Máquinas de Estado
* Sistemas Multiprocessados
* Programação Orientada a Objetos (POO)

---

### 🎮 Ideia de Design

O sistema utiliza um **baú estilo Minecraft** como abstração:

* Cada posição da memória armazena um item e sua quantidade
* Os jogadores representam processadores (cada um com sua cache)
* As operações simulam acessos reais à memória

---

### ▶️ Como Executar

```bash
python main.py
```

---

⚠️ **Nota:**
Este projeto reflete meu nível de conhecimento em 2025 e foi desenvolvido com fins educacionais, com foco na compreensão de coerência de cache.

