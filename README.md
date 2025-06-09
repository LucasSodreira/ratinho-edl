# 🐭 Ratinho no Labirinto - Algoritmo BFS

Um projeto educacional em Python que demonstra o algoritmo de **Busca em Largura (BFS)** através de uma visualização interativa de um rato encontrando o menor caminho em um labirinto.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-v2.6.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Estruturas de Dados](#estruturas-de-dados)
- [Algoritmo BFS](#algoritmo-bfs)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Exemplos de Labirintos](#exemplos-de-labirintos)
- [Controles](#controles)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como material educacional para a disciplina de **Estrutura de Dados**, demonstrando na prática:

- Implementação do algoritmo **BFS (Breadth-First Search)**
- Uso de diferentes estruturas de dados (Fila, Lista, Conjunto, Tupla)
- Visualização de algoritmos de busca
- Tratamento de casos especiais (labirintos sem solução)
- Interface gráfica interativa com Pygame

### 🎥 Demonstração

O programa mostra 3 fases distintas:
1. **Exploração**: Visualiza todos os caminhos explorados pelo algoritmo
2. **Caminho Final**: Destaca o menor caminho encontrado
3. **Movimento**: Anima o rato percorrendo o caminho ótimo

## 🏗️ Estruturas de Dados

### 1. **Fila (Queue)** - Coração do BFS
```python
from collections import deque
fila = deque([(inicio, [inicio])])
```
- **Uso**: Implementação do algoritmo BFS
- **Complexidade**: O(1) para inserção/remoção
- **Por que?**: Garante exploração nível por nível

### 2. **Lista (List)** - Representação do Labirinto
```python
labirinto = [[1, 0, 1], [0, 0, 0], [1, 'e', 1]]
```
- **Uso**: Matriz 2D do labirinto e armazenamento de caminhos
- **Complexidade**: O(1) para acesso

### 3. **Conjunto (Set)** - Controle de Visitados
```python
visitados = set()
visitados.add((x, y))
```
- **Uso**: Verificação rápida de posições já visitadas
- **Complexidade**: O(1) em média
- **Benefício**: Evita ciclos infinitos

### 4. **Tupla (Tuple)** - Coordenadas
```python
posicao = (x, y)
```
- **Uso**: Representação imutável de coordenadas
- **Benefício**: Pode ser usada como chave em sets/dicts

## 🔍 Algoritmo BFS

### Por que BFS?

O **Breadth-First Search** é ideal para este projeto porque:

✅ **Garante o menor caminho** em grafos não-ponderados  
✅ **Explora sistematicamente** nível por nível  
✅ **Complexidade otimizada** O(V + E)  
✅ **Visualização clara** do processo de busca  

### Comparação de Algoritmos

| Algoritmo | Estrutura | Menor Caminho | Complexidade |
|-----------|-----------|---------------|--------------|
| **BFS** | Fila | ✅ Garantido | O(V + E) |
| DFS | Pilha | ❌ Não garante | O(V + E) |
| A* | Heap | ✅ Garantido | O(E log V) |

## ✨ Funcionalidades

### 🎮 Principais Recursos

- **Visualização em tempo real** do algoritmo BFS
- **Animação suave** com velocidade ajustável
- **Tratamento de erros** robusto
- **Suporte a múltiplos formatos** de arquivo
- **Estatísticas detalhadas** de performance
- **Interface intuitiva** com controles simples

### 🔧 Recursos Técnicos

- **Detecção automática** de labirintos impossíveis
- **Fallback de imagens** para máxima compatibilidade
- **Validação completa** de formato de arquivo
- **Sistema de configuração** centralizado
- **Logs informativos** no console

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/ratinho-edl.git
cd ratinho-edl
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o projeto**
```bash
python main.py
```

## 🚀 Como Usar

### Execução Básica
```bash
# Usa o labirinto padrão
python main.py

# Especifica um labirinto personalizado
python main.py meu_labirinto.txt
```

### Formato do Arquivo de Labirinto

```
10 x 10
1111111111
1m00000001
1011111101
1000000001
1111011111
1000000001
1011111101
1000000001
1011111101
111111111e
```

**Legenda:**
- `1` = Parede
- `0` = Caminho livre
- `m` = Posição inicial do rato
- `e` = Saída

## 📁 Exemplos de Labirintos

O projeto inclui vários labirintos de exemplo:

- `maze64x64.txt` - Labirinto teste simples
- `labirinto.txt` - Labirinto médio com obstáculos
- `labirinto01.txt` - Labirinto complexo 32x32

### Criando Seus Próprios Labirintos

1. Primeira linha: dimensões no formato `altura x largura`
2. Linhas seguintes: matriz do labirinto
3. Deve conter exatamente 1 rato (`m`) e 1 saída (`e`)

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| `ESPAÇO` | Iniciar/Pausar animação |
| `R` | Reiniciar busca |
| `Q` | Sair do programa |
| `+` | Aumentar velocidade |
| `-` | Diminuir velocidade |

## 📊 Interface

### Informações Exibidas

- **Status atual** da execução
- **Contador de progresso** para cada fase
- **Estatísticas de performance**:
  - Nós visitados
  - Tempo de execução
  - Eficiência do algoritmo
- **Instruções de controle**

### Estados da Aplicação

1. **Pausado**: Aguardando comando do usuário
2. **Explorando**: Mostrando busca em progresso
3. **Caminho Final**: Destacando solução encontrada
4. **Movimento**: Animando rato no caminho
5. **Sem Solução**: Indica labirinto impossível

## 📂 Estrutura do Projeto

```
ratinho-edl/
├── main.py              # Arquivo principal com interface gráfica
├── rato.py              # Lógica do algoritmo BFS e carregamento
├── imgs.py              # Sistema de carregamento de imagens
├── requirements.txt     # Dependências do projeto
├── .gitignore          # Arquivos ignorados pelo Git
├── README.md           # Documentação principal
├── labirintos/             
|    ├── labirinto.txt       # Exemplo de labirinto 17x17
|    ├── labirinto01.txt     # Exemplo de labirinto 32x32
|    └── maze64x64.txt       # Exemplo de labirinto 10x10
└── img/                
    ├── P-Lado.png
    ├── Parede.png
    ├── Casa.png
    ├── Chao.png
    └── Arvore-3.png
```

## 🔧 Configuração Avançada

### Personalizando Cores

Edite a classe `ConfiguracaoJogo` em `main.py`:

```python
class ConfiguracaoJogo:
    def __init__(self):
        # Cores personalizáveis
        self.COR_EXPLORACAO = (255, 120, 120)      # Vermelho
        self.COR_CAMINHO_FINAL = (120, 255, 120)   # Verde
        self.COR_FUNDO = (40, 40, 40)              # Cinza escuro
```

### Ajustando Performance

```python
# Velocidades (menor = mais rápido)
self.VELOCIDADE_EXPLORACAO = 2
self.VELOCIDADE_CAMINHO = 8
self.VELOCIDADE_PLAYER = 15
```

## 📈 Estatísticas do Projeto

- **Linguagem**: Python 3.8+
- **Biblioteca Gráfica**: Pygame 2.6.1
- **Estruturas de Dados**: Fila, Lista, Conjunto, Tupla
- **Algoritmo Principal**: BFS (Breadth-First Search)
- **Complexidade**: O(V + E) onde V = vértices, E = arestas

