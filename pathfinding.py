"""
Algoritmos de pathfinding - BFS, A* e otimizações
"""
import time
import heapq
from collections import deque
from labirinto import GerenciadorLabirinto

class AlgoritmoBFS:
    """Implementa o algoritmo BFS básico para busca de caminhos"""
    
    @staticmethod
    def bfs_menor_caminho(labirinto, inicio, fim):
        """BFS básico - mantido para compatibilidade"""
        if not labirinto or not inicio or not fim:
            return [], [], {'erro': 'Parâmetros inválidos'}
        
        inicio_tempo = time.time()
        queue = deque([(inicio, [inicio])])
        visitados = set()
        caminhos_explorados = []
        nos_visitados = 0
        
        while queue:
            (x, y), caminho = queue.popleft()
            nos_visitados += 1
            
            if (x, y) in visitados:
                continue
            
            visitados.add((x, y))
            caminhos_explorados.append((x, y))
            
            # Verificar se chegou ao destino
            if (x, y) == fim:
                fim_tempo = time.time()
                return caminho, caminhos_explorados, {
                    'tempo_execucao': fim_tempo - inicio_tempo,
                    'nos_visitados': nos_visitados,
                    'algoritmo': 'BFS',
                    'caminho_encontrado': True
                }
            
            # Explorar vizinhos (direções: cima, baixo, esquerda, direita)
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                
                if (nx, ny) not in visitados and GerenciadorLabirinto.eh_posicao_valida(nx, ny, labirinto):
                    queue.append(((nx, ny), caminho + [(nx, ny)]))
        
        fim_tempo = time.time()
        return [], caminhos_explorados, {
            'tempo_execucao': fim_tempo - inicio_tempo,
            'nos_visitados': nos_visitados,
            'algoritmo': 'BFS',
            'caminho_encontrado': False
        }

class AlgoritmoAStar:
    """Implementa o algoritmo A* - muito mais eficiente que BFS"""
    
    @staticmethod
    def heuristica_manhattan(pos1, pos2):
        """Distância de Manhattan entre duas posições"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    @staticmethod
    def heuristica_euclidiana(pos1, pos2):
        """Distância euclidiana entre duas posições"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    
    @staticmethod
    def reconstruir_caminho(came_from, atual):
        """Reconstrói o caminho a partir do mapa came_from"""
        caminho = [atual]
        while atual in came_from:
            atual = came_from[atual]
            caminho.append(atual)
        return caminho[::-1]
    
    @staticmethod
    def a_star_busca(labirinto, inicio, fim, heuristica="manhattan"):
        """
        Implementação do algoritmo A*
        
        Args:
            labirinto: Matriz do labirinto
            inicio: Posição inicial (x, y)
            fim: Posição final (x, y)
            heuristica: "manhattan" ou "euclidiana"
        """
        inicio_tempo = time.time()
        
        # Escolher função heurística
        if heuristica == "euclidiana":
            h_func = AlgoritmoAStar.heuristica_euclidiana
        else:
            h_func = AlgoritmoAStar.heuristica_manhattan
        
        # Inicialização
        open_set = []
        heapq.heappush(open_set, (0, inicio))
        came_from = {}
        
        g_score = {inicio: 0}
        f_score = {inicio: h_func(inicio, fim)}
        
        visitados = set()
        caminhos_explorados = []
        nos_visitados = 0
        
        while open_set:
            _, atual = heapq.heappop(open_set)
            nos_visitados += 1
            
            if atual in visitados:
                continue
            
            visitados.add(atual)
            caminhos_explorados.append(atual)
            
            # Verificar se chegou ao destino
            if atual == fim:
                caminho = AlgoritmoAStar.reconstruir_caminho(came_from, atual)
                fim_tempo = time.time()
                return caminho, caminhos_explorados, {
                    'tempo_execucao': fim_tempo - inicio_tempo,
                    'nos_visitados': nos_visitados,
                    'algoritmo': f'A* ({heuristica})',
                    'caminho_encontrado': True
                }
            
            # Explorar vizinhos
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                vizinho = (atual[0] + dx, atual[1] + dy)
                
                if not GerenciadorLabirinto.eh_posicao_valida(vizinho[0], vizinho[1], labirinto):
                    continue
                
                tentative_g_score = g_score[atual] + 1
                
                if vizinho not in g_score or tentative_g_score < g_score[vizinho]:
                    came_from[vizinho] = atual
                    g_score[vizinho] = tentative_g_score
                    f_score[vizinho] = tentative_g_score + h_func(vizinho, fim)
                    
                    # Adicionar à fila se não estiver lá
                    if vizinho not in visitados:
                        heapq.heappush(open_set, (f_score[vizinho], vizinho))
        
        fim_tempo = time.time()
        return [], caminhos_explorados, {
            'tempo_execucao': fim_tempo - inicio_tempo,
            'nos_visitados': nos_visitados,
            'algoritmo': f'A* ({heuristica})',
            'caminho_encontrado': False
        }

class AlgoritmoBFSOtimizado:
    """BFS com otimizações de direção e early stopping"""
    
    @staticmethod
    def bfs_otimizado(labirinto, inicio, fim):
        """BFS otimizado com heurística de direção"""
        inicio_tempo = time.time()
        
        # Priorizar direções baseadas na posição do objetivo
        dx_objetivo = fim[0] - inicio[0]
        dy_objetivo = fim[1] - inicio[1]
        
        # Ordenar direções baseado na proximidade ao objetivo
        direcoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # cima, baixo, esquerda, direita
        direcoes_priorizadas = sorted(direcoes, key=lambda d: 
            abs(d[0] - (1 if dx_objetivo > 0 else -1 if dx_objetivo < 0 else 0)) +
            abs(d[1] - (1 if dy_objetivo > 0 else -1 if dy_objetivo < 0 else 0))
        )
        
        queue = deque([(inicio, [inicio])])
        visitados = set()
        caminhos_explorados = []
        nos_visitados = 0
        
        while queue:
            (x, y), caminho = queue.popleft()
            nos_visitados += 1
            
            if (x, y) in visitados:
                continue
            
            visitados.add((x, y))
            caminhos_explorados.append((x, y))
            
            # Verificar se chegou ao destino
            if (x, y) == fim:
                fim_tempo = time.time()
                return caminho, caminhos_explorados, {
                    'tempo_execucao': fim_tempo - inicio_tempo,
                    'nos_visitados': nos_visitados,
                    'algoritmo': 'BFS Otimizado',
                    'caminho_encontrado': True
                }
            
            # Explorar vizinhos com direções priorizadas
            for dx, dy in direcoes_priorizadas:
                nx, ny = x + dx, y + dy
                
                if (nx, ny) not in visitados and GerenciadorLabirinto.eh_posicao_valida(nx, ny, labirinto):
                    queue.append(((nx, ny), caminho + [(nx, ny)]))
        
        fim_tempo = time.time()
        return [], caminhos_explorados, {
            'tempo_execucao': fim_tempo - inicio_tempo,
            'nos_visitados': nos_visitados,
            'algoritmo': 'BFS Otimizado',
            'caminho_encontrado': False
        }

class GerenciadorPathfinding:
    """Gerencia diferentes algoritmos de pathfinding otimizados"""
    
    def __init__(self):
        self.algoritmo_atual = "a_star"  # Usar A* como padrão
        self.algoritmos = {
            "bfs": AlgoritmoBFS(),
            "bfs_otimizado": AlgoritmoBFSOtimizado(),
            "a_star": AlgoritmoAStar()
        }
    
    def encontrar_caminho(self, labirinto, inicio, fim, algoritmo=None):
        """
        Encontra um caminho usando o algoritmo especificado
        
        Args:
            labirinto: Matriz do labirinto
            inicio: Posição inicial (x, y)
            fim: Posição final (x, y)
            algoritmo: Algoritmo a ser usado (None usa o atual)
            
        Returns:
            tuple: (caminho, caminhos_explorados, estatisticas)
        """
        if algoritmo is None:
            algoritmo = self.algoritmo_atual
        
        algoritmo = algoritmo.lower()
        
        if algoritmo == "bfs":
            return AlgoritmoBFS.bfs_menor_caminho(labirinto, inicio, fim)
        elif algoritmo == "bfs_otimizado":
            return AlgoritmoBFSOtimizado.bfs_otimizado(labirinto, inicio, fim)
        elif algoritmo in ["a_star", "astar"]:
            return AlgoritmoAStar.a_star_busca(labirinto, inicio, fim, "manhattan")
        elif algoritmo in ["a_star_euclidiano", "a_star_euclidiana"]:
            return AlgoritmoAStar.a_star_busca(labirinto, inicio, fim, "euclidiana")
        else:
            print(f"⚠️ Algoritmo '{algoritmo}' não reconhecido, usando A*")
            return AlgoritmoAStar.a_star_busca(labirinto, inicio, fim, "manhattan")
    
    def definir_algoritmo(self, algoritmo):
        """Define qual algoritmo usar como padrão"""
        algoritmo = algoritmo.lower()
        if algoritmo in ["bfs", "bfs_otimizado", "a_star", "a_star_euclidiano", "a_star_euclidiana"]:
            self.algoritmo_atual = algoritmo
            print(f"Algoritmo alterado para: {algoritmo}")
        else:
            print(f"Algoritmo '{algoritmo}' não suportado")
    
    def comparar_algoritmos(self, labirinto, inicio, fim):
        """Compara a performance de todos os algoritmos"""
        resultados = {}
        algoritmos_teste = ["bfs", "bfs_otimizado", "a_star", "a_star_euclidiano"]
        
        for alg in algoritmos_teste:
            try:
                caminho, explorados, stats = self.encontrar_caminho(labirinto, inicio, fim, alg)
                resultados[alg] = {
                    'caminho': caminho,
                    'explorados': explorados,
                    'estatisticas': stats
                }
            except Exception as e:
                resultados[alg] = {'erro': str(e)}
        
        return resultados
