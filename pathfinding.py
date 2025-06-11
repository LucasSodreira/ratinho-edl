from collections import deque
import heapq
import time
import math

class AlgoritmoBFS:
    """Implementa o algoritmo BFS básico para busca de caminhos"""
    
    @staticmethod
    def bfs_menor_caminho(labirinto, inicio, fim):
        """BFS básico - mantido para compatibilidade"""
        if not labirinto or not inicio or not fim:
            return [], [], {}
        
        if inicio == fim:
            return [inicio], [inicio], {"nos_visitados": 1, "tempo_execucao": 0}
        
        tempo_inicio = time.time()
        
        linhas, colunas = len(labirinto), len(labirinto[0])
        visitados = set()
        fila = deque([(inicio, [inicio])])
        caminhos_explorados = []
        
        # Direções otimizadas: prioriza direita e baixo (heurística simples)
        direcoes = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        nos_visitados = 0
        
        while fila:
            (x, y), caminho = fila.popleft()
            
            if (x, y) in visitados:
                continue
                
            visitados.add((x, y))
            caminhos_explorados.append((x, y))
            nos_visitados += 1
            
            # Se chegou ao destino
            if (x, y) == fim:
                tempo_execucao = time.time() - tempo_inicio
                estatisticas = {
                    "nos_visitados": nos_visitados,
                    "tempo_execucao": tempo_execucao,
                    "tamanho_caminho": len(caminho),
                    "eficiencia": len(caminho) / nos_visitados if nos_visitados > 0 else 0
                }
                return caminho, caminhos_explorados, estatisticas
            
            # Explorar vizinhos
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < colunas and 0 <= ny < linhas and 
                    (nx, ny) not in visitados and
                    labirinto[ny][nx] != 1):
                    
                    novo_caminho = caminho + [(nx, ny)]
                    fila.append(((nx, ny), novo_caminho))
        
        # Nenhum caminho encontrado
        tempo_execucao = time.time() - tempo_inicio
        estatisticas = {
            "nos_visitados": nos_visitados,
            "tempo_execucao": tempo_execucao,
            "tamanho_caminho": 0,
            "eficiencia": 0
        }
        return [], caminhos_explorados, estatisticas

class AlgoritmoAStar:
    """Implementa o algoritmo A* - muito mais eficiente que BFS"""
    
    @staticmethod
    def heuristica_manhattan(pos1, pos2):
        """Calcula distância Manhattan (mais rápida que Euclidiana)"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    @staticmethod
    def heuristica_euclidiana(pos1, pos2):
        """Calcula distância Euclidiana (mais precisa)"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    @staticmethod
    def reconstruir_caminho(came_from, atual):
        """Reconstrói o caminho do fim ao início"""
        caminho = []
        while atual in came_from:
            caminho.append(atual)
            atual = came_from[atual]
        caminho.append(atual)
        return caminho[::-1]
    
    @staticmethod
    def a_star_busca(labirinto, inicio, fim, heuristica="manhattan"):
        """
        Algoritmo A* otimizado para pathfinding
        
        Args:
            labirinto: Matriz do labirinto
            inicio: Posição inicial (x, y)
            fim: Posição final (x, y)
            heuristica: "manhattan" ou "euclidiana"
        """
        if not labirinto or not inicio or not fim:
            return [], [], {}
        
        if inicio == fim:
            return [inicio], [inicio], {"nos_visitados": 1, "tempo_execucao": 0}
        
        tempo_inicio = time.time()
        
        linhas, colunas = len(labirinto), len(labirinto[0])
        
        # Escolher função heurística
        if heuristica == "euclidiana":
            h_func = AlgoritmoAStar.heuristica_euclidiana
        else:
            h_func = AlgoritmoAStar.heuristica_manhattan
        
        # Estruturas de dados do A*
        open_set = []
        heapq.heappush(open_set, (0, inicio))
        came_from = {}
        
        g_score = {inicio: 0}
        f_score = {inicio: h_func(inicio, fim)}
        
        visitados = set()
        caminhos_explorados = []
        nos_visitados = 0
        
        # Direções com prioridade baseada na direção do objetivo
        direcoes = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        while open_set:
            atual_f, atual = heapq.heappop(open_set)
            
            if atual in visitados:
                continue
            
            visitados.add(atual)
            caminhos_explorados.append(atual)
            nos_visitados += 1
            
            # Se chegou ao destino
            if atual == fim:
                caminho = AlgoritmoAStar.reconstruir_caminho(came_from, fim)
                tempo_execucao = time.time() - tempo_inicio
                
                estatisticas = {
                    "nos_visitados": nos_visitados,
                    "tempo_execucao": tempo_execucao,
                    "tamanho_caminho": len(caminho),
                    "eficiencia": len(caminho) / nos_visitados if nos_visitados > 0 else 0,
                    "algoritmo": f"A* ({heuristica})"
                }
                return caminho, caminhos_explorados, estatisticas
            
            # Explorar vizinhos
            for dx, dy in direcoes:
                vizinho = (atual[0] + dx, atual[1] + dy)
                nx, ny = vizinho
                
                # Verificar limites e obstáculos
                if (0 <= nx < colunas and 0 <= ny < linhas and 
                    labirinto[ny][nx] != 1 and vizinho not in visitados):
                    
                    tentative_g_score = g_score[atual] + 1
                    
                    if vizinho not in g_score or tentative_g_score < g_score[vizinho]:
                        came_from[vizinho] = atual
                        g_score[vizinho] = tentative_g_score
                        f_score[vizinho] = tentative_g_score + h_func(vizinho, fim)
                        heapq.heappush(open_set, (f_score[vizinho], vizinho))
        
        # Nenhum caminho encontrado
        tempo_execucao = time.time() - tempo_inicio
        estatisticas = {
            "nos_visitados": nos_visitados,
            "tempo_execucao": tempo_execucao,
            "tamanho_caminho": 0,
            "eficiencia": 0,
            "algoritmo": f"A* ({heuristica})"
        }
        return [], caminhos_explorados, estatisticas

class AlgoritmoBFSOtimizado:
    """BFS com otimizações de direção e early stopping"""
    
    @staticmethod
    def bfs_otimizado(labirinto, inicio, fim):
        """BFS com direções priorizadas baseadas no objetivo"""
        if not labirinto or not inicio or not fim:
            return [], [], {}
        
        if inicio == fim:
            return [inicio], [inicio], {"nos_visitados": 1, "tempo_execucao": 0}
        
        tempo_inicio = time.time()
        
        linhas, colunas = len(labirinto), len(labirinto[0])
        visitados = set()
        fila = deque([(inicio, [inicio])])
        caminhos_explorados = []
        nos_visitados = 0
        
        # Calcular direção preferencial baseada no objetivo
        dx_objetivo = 1 if fim[0] > inicio[0] else -1 if fim[0] < inicio[0] else 0
        dy_objetivo = 1 if fim[1] > inicio[1] else -1 if fim[1] < inicio[1] else 0
        
        # Priorizar direções que se aproximam do objetivo
        direcoes_priorizadas = []
        todas_direcoes = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        # Adicionar direções do objetivo primeiro
        if dx_objetivo != 0:
            direcoes_priorizadas.append((dx_objetivo, 0))
        if dy_objetivo != 0:
            direcoes_priorizadas.append((0, dy_objetivo))
        
        # Adicionar outras direções
        for direcao in todas_direcoes:
            if direcao not in direcoes_priorizadas:
                direcoes_priorizadas.append(direcao)
        
        while fila:
            (x, y), caminho = fila.popleft()
            
            if (x, y) in visitados:
                continue
                
            visitados.add((x, y))
            caminhos_explorados.append((x, y))
            nos_visitados += 1
            
            # Se chegou ao destino
            if (x, y) == fim:
                tempo_execucao = time.time() - tempo_inicio
                estatisticas = {
                    "nos_visitados": nos_visitados,
                    "tempo_execucao": tempo_execucao,
                    "tamanho_caminho": len(caminho),
                    "eficiencia": len(caminho) / nos_visitados if nos_visitados > 0 else 0,
                    "algoritmo": "BFS Otimizado"
                }
                return caminho, caminhos_explorados, estatisticas
            
            # Explorar vizinhos com prioridade
            for dx, dy in direcoes_priorizadas:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < colunas and 0 <= ny < linhas and 
                    (nx, ny) not in visitados and
                    labirinto[ny][nx] != 1):
                    
                    novo_caminho = caminho + [(nx, ny)]
                    fila.append(((nx, ny), novo_caminho))
        
        # Nenhum caminho encontrado
        tempo_execucao = time.time() - tempo_inicio
        estatisticas = {
            "nos_visitados": nos_visitados,
            "tempo_execucao": tempo_execucao,
            "tamanho_caminho": 0,
            "eficiencia": 0,
            "algoritmo": "BFS Otimizado"
        }
        return [], caminhos_explorados, estatisticas

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
            return self.algoritmos["bfs"].bfs_menor_caminho(labirinto, inicio, fim)
        elif algoritmo == "bfs_otimizado":
            return self.algoritmos["bfs_otimizado"].bfs_otimizado(labirinto, inicio, fim)
        elif algoritmo in ["a_star", "astar"]:
            return self.algoritmos["a_star"].a_star_busca(labirinto, inicio, fim, "manhattan")
        elif algoritmo in ["a_star_euclidiano", "a_star_euclidiana"]:
            return self.algoritmos["a_star"].a_star_busca(labirinto, inicio, fim, "euclidiana")
        else:
            raise ValueError(f"Algoritmo '{algoritmo}' não suportado")
    
    def definir_algoritmo(self, algoritmo):
        """Define qual algoritmo usar como padrão"""
        algoritmo = algoritmo.lower()
        if algoritmo in ["bfs", "bfs_otimizado", "a_star", "a_star_euclidiano", "a_star_euclidiana"]:
            self.algoritmo_atual = algoritmo
        else:
            raise ValueError(f"Algoritmo '{algoritmo}' não suportado")
    
    def comparar_algoritmos(self, labirinto, inicio, fim):
        """Compara a performance de todos os algoritmos"""
        resultados = {}
        algoritmos_teste = ["bfs", "bfs_otimizado", "a_star", "a_star_euclidiano"]
        
        for alg in algoritmos_teste:
            try:
                caminho, explorados, stats = self.encontrar_caminho(labirinto, inicio, fim, alg)
                resultados[alg] = {
                    "caminho_encontrado": len(caminho) > 0,
                    "tamanho_caminho": len(caminho),
                    "nos_visitados": stats.get("nos_visitados", 0),
                    "tempo_execucao": stats.get("tempo_execucao", 0),
                    "eficiencia": stats.get("eficiencia", 0)
                }
            except Exception as e:
                resultados[alg] = {"erro": str(e)}
        
        return resultados
