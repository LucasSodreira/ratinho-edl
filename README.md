# 🐭 Ratinho no Labirinto - Algoritmos de Pathfinding

Um projeto educacional em Python que demonstra diferentes **algoritmos de busca de caminho** através de uma visualização interativa de um rato encontrando o menor caminho em um labirinto.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-v2.6.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Algoritmos Implementados](#algoritmos-implementados)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Labirintos Disponíveis](#labirintos-disponíveis)
- [Controles](#controles)
- [Comparação de Performance](#comparação-de-performance)

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como material educacional para a disciplina de **Estrutura de Dados**, demonstrando na prática:

- Implementação de múltiplos algoritmos de pathfinding
- Comparação de eficiência entre algoritmos
- Uso de diferentes estruturas de dados (Fila, Heap, Set, Lista)
- Visualização de algoritmos de busca
- Interface gráfica responsiva e moderna

### 🎥 Demonstração

O programa mostra 3 fases distintas:
1. **Exploração**: Visualiza todos os caminhos explorados pelo algoritmo
2. **Caminho Final**: Destaca o menor caminho encontrado
3. **Movimento**: Anima o rato percorrendo o caminho ótimo

## 🧠 Algoritmos Implementados

### 1. **BFS (Breadth-First Search)** - Algoritmo Base
- **Garantia**: Sempre encontra o menor caminho
- **Eficiência**: ~15-25% (explora muitos nós desnecessários)
- **Estrutura**: Fila (FIFO)
- **Uso**: Aprendizado e comparação

### 2. **BFS Otimizado** - Melhorias Heurísticas  
- **Melhoria**: Prioriza direções baseadas no objetivo
- **Eficiência**: ~30-50% (reduz exploração desnecessária)
- **Estrutura**: Fila com ordenação de direções
- **Uso**: Demonstrar como pequenas otimizações ajudam

### 3. **A\* Manhattan** - Algoritmo Inteligente ⭐
- **Heurística**: Distância Manhattan (|x1-x2| + |y1-y2|)
- **Eficiência**: ~80-95% (explora apenas caminhos promissores)
- **Estrutura**: Heap (Priority Queue)
- **Uso**: Solução de produção recomendada

### 4. **A\* Euclidiano** - Máxima Precisão
- **Heurística**: Distância Euclidiana (√[(x1-x2)² + (y1-y2)²])
- **Eficiência**: ~85-95% (mais preciso em diagonais)
- **Estrutura**: Heap (Priority Queue)
- **Uso**: Casos com movimento diagonal

## ✨ Funcionalidades

### 🎮 Recursos do Jogo
- **Seleção interativa de labirintos** - Menu para escolher mapas
- **Múltiplos algoritmos** - Compare performance em tempo real
- **Tela maximizada automática** - Experiência imersiva
- **Interface responsiva** - Adapta a qualquer resolução
- **Estatísticas detalhadas** - Eficiência, tempo, nós visitados
- **Controles intuitivos** - Teclas numéricas para trocar algoritmos

### 🔧 Recursos Técnicos
- **Sistema modular** - Código bem organizado
- **Detecção de labirintos impossíveis** - Evita travamentos
- **Fallback de imagens** - Funciona mesmo sem assets
- **API nativa do Windows** - Maximização real da janela
- **Comparação automática** - Todos algoritmos de uma vez

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Sistema operacional: Windows, Linux ou macOS

### Instalação Rápida
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ratinho-edl.git
cd ratinho-edl

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o projeto
python main.py
```

## 🚀 Como Usar

### Execução Básica
```bash
# Menu interativo de labirintos
python main.py

# Labirinto específico por nome
python main.py labirinto01

# Caminho completo
python main.py labirintos/maze64x64.txt
```

### Exemplos de Uso
```bash
# Testar com labirinto pequeno e rápido
python main.py maze64x64

# Testar com labirinto complexo 32x32  
python main.py labirinto01

# Usar labirinto padrão
python main.py labirinto
```

## 🗺️ Labirintos Disponíveis

| Arquivo | Dimensões | Dificuldade | Melhor Para |
|---------|-----------|-------------|-------------|
| `maze64x64.txt` | 10x10 | ⭐ Fácil | Testes rápidos e aprendizado |
| `labirinto.txt` | 17x17 | ⭐⭐ Médio | Demonstrações e comparações |
| `labirinto01.txt` | 32x32 | ⭐⭐⭐ Difícil | Teste de performance |

### Criando Seus Próprios Labirintos

1. **Formato do arquivo**:
   ```
   altura x largura
   1111111111
   1m00000001
   1011111101
   1000000001
   111111111e
   ```

2. **Legenda**:
   - `1` = Parede (intransponível)
   - `0` = Caminho livre
   - `m` = Posição inicial do rato
   - `e` = Saída (objetivo)

3. **Regras**:
   - Exatamente 1 rato (`m`) e 1 saída (`e`)
   - Bordas recomendadas como paredes
   - Deve existir um caminho válido

## 🎮 Controles

### Seleção de Algoritmos
| Tecla | Algoritmo | Eficiência Esperada |
|-------|-----------|-------------------|
| `1` | BFS Básico | ~15-25% |
| `2` | BFS Otimizado | ~30-50% |
| `3` | A* Manhattan | ~80-95% ⭐ |
| `4` | A* Euclidiano | ~85-95% |

### Controles Gerais
| Tecla | Ação |
|-------|------|
| `ESPAÇO` | Iniciar/Pausar animação |
| `R` | Reiniciar com A* Manhattan |
| `C` | Comparar todos os algoritmos |
| `F11` | Alternar fullscreen |
| `ESC` | Sair do programa |
| `+/-` | Ajustar velocidade da animação |

## 📊 Comparação de Performance

### Resultado Real - Labirinto 17x17

| Algoritmo | Nós Visitados | Eficiência | Tempo | Recomendação |
|-----------|---------------|------------|-------|--------------|
| BFS Básico | 150+ | ~14.8% | Alto | ❌ Apenas educacional |
| BFS Otimizado | 80-120 | ~30-45% | Médio | ⚠️ Para demonstração |
| A* Manhattan | 25-40 | ~80-95% | Baixo | ✅ **Recomendado** |
| A* Euclidiano | 25-45 | ~85-92% | Baixo | ✅ Para casos especiais |

### Por que A* é Superior?

**BFS tradicional**: Explora **TODOS** os caminhos possíveis nível por nível
```
Nós explorados: ████████████████ (muitos)
Eficiência: 14.8% ❌
```

**A* com heurística**: Explora apenas caminhos **PROMISSORES**
```
Nós explorados: ████ (poucos)
Eficiência: 90%+ ✅
```

## 🏗️ Estrutura do Projeto

```
ratinho-edl/
├── 📄 main.py              # Menu e inicialização 
├── 🎮 jogo.py              # Engine principal do jogo
├── 🧠 pathfinding.py       # Algoritmos de busca
├── 🗺️ labirinto.py         # Carregamento e validação
├── 👤 player.py            # Gerenciamento do personagem
├── 🎨 interface.py         # Interface gráfica
├── 🖼️ imgs.py              # Sistema de imagens
├── ⚙️ config.py            # Configurações globais
├── 📋 requirements.txt     # Dependências Python
├── 📖 README.md           # Esta documentação
├── 🗂️ labirintos/         # Mapas disponíveis
│   ├── maze64x64.txt      # 🟢 Fácil (10x10)
│   ├── labirinto.txt      # 🟡 Médio (17x17)  
│   └── labirinto01.txt    # 🔴 Difícil (32x32)
└── 🖼️ img/               # Assets gráficos (opcional)
    ├── P-Lado.png
    ├── Casa.png
    └── ...
```

## 🔬 Para Desenvolvedores

### Adicionando Novos Algoritmos

1. **Criar classe em `pathfinding.py`**:
   ```python
   class MeuAlgoritmo:
       @staticmethod
       def buscar(labirinto, inicio, fim):
           # Implementar algoritmo
           return caminho, explorados, estatisticas
   ```

2. **Registrar no gerenciador**:
   ```python
   # Em GerenciadorPathfinding
   elif algoritmo == "meu_algoritmo":
       return MeuAlgoritmo.buscar(labirinto, inicio, fim)
   ```

3. **Adicionar controle**:
   ```python
   # Em jogo.py - processar_eventos()
   elif event.key == pygame.K_5:
       self.reiniciar_busca("meu_algoritmo")
   ```

### Executando Testes
```bash
# Teste básico de importação
python -c "from rato import *; print('✅ Módulos OK')"

# Teste de algoritmo
python -c "
from pathfinding import AlgoritmoAStar
# Testar implementação
"
```
