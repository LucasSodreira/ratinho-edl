from labirinto import GerenciadorLabirinto
from pathfinding import GerenciadorPathfinding

# Instância global do gerenciador de pathfinding
_pathfinder = GerenciadorPathfinding()

# Funções de compatibilidade para manter a interface existente
def criar_labirinto(arquivo):
    """Interface compatível para criação de labirinto"""
    return GerenciadorLabirinto.criar_labirinto(arquivo)

def encontrar_posicao_inicial(labirinto):
    """Interface compatível para encontrar posição inicial"""
    return GerenciadorLabirinto.encontrar_posicao_inicial(labirinto)

def encontrar_posicao_saida(labirinto):
    """Interface compatível para encontrar posição da saída"""
    return GerenciadorLabirinto.encontrar_posicao_saida(labirinto)

def bfs_menor_caminho(labirinto, inicio, fim):
    """Interface compatível para BFS"""
    return _pathfinder.encontrar_caminho(labirinto, inicio, fim, "bfs")

def eh_posicao_valida(x, y, labirinto):
    """Interface compatível para validação de posição"""
    return GerenciadorLabirinto.eh_posicao_valida(x, y, labirinto)

def validar_labirinto(labirinto):
    """Interface compatível para validação de labirinto"""
    return GerenciadorLabirinto.validar_labirinto(labirinto)

# Exportar classes principais para uso direto
__all__ = [
    'criar_labirinto',
    'encontrar_posicao_inicial',
    'encontrar_posicao_saida',
    'bfs_menor_caminho',
    'eh_posicao_valida',
    'validar_labirinto',
    'GerenciadorLabirinto',
    'GerenciadorPathfinding'
]