import pygame
import os

def carregar_imagem_segura(caminho, cor_fallback=(100, 100, 100), tamanho=(40, 40)):
    """
    Carrega uma imagem com fallback para uma superficie colorida se a imagem não existir.
    
    Args:
        caminho (str): Caminho para a imagem
        cor_fallback (tuple): Cor RGB para usar se a imagem não carregar
        tamanho (tuple): Tamanho da superficie fallback
    
    Returns:
        pygame.Surface: A imagem carregada ou uma superficie colorida
    """
    try:
        if os.path.exists(caminho):
            return pygame.image.load(caminho)
        else:
            print(f"Aviso: Imagem '{caminho}' não encontrada, usando fallback colorido")
            superficie = pygame.Surface(tamanho)
            superficie.fill(cor_fallback)
            return superficie
    except pygame.error as e:
        print(f"Erro ao carregar '{caminho}': {e}, usando fallback")
        superficie = pygame.Surface(tamanho)
        superficie.fill(cor_fallback)
        return superficie

# Carregamento das imagens com fallbacks
imagen_P_Lado = carregar_imagem_segura("img/P-Lado.png", (100, 100, 255))  # Azul para player
imagen_Parede = carregar_imagem_segura("img/Parede.png", (139, 69, 19))    # Marrom para parede
imagem_casa = carregar_imagem_segura("img/Casa.png", (255, 215, 0))         # Dourado para saída
imagem_chao = carregar_imagem_segura("img/Chao.png", (245, 245, 220))       # Bege claro para chão
imagen_arvore = carregar_imagem_segura("img/Arvore-3.png", (34, 139, 34))   # Verde para árvore/parede

# Função para obter cores baseadas no tipo de célula
def obter_cor_celula(tipo_celula):
    """
    Retorna uma cor padrão baseada no tipo de célula do labirinto.
    
    Args:
        tipo_celula: O tipo da célula ('0', '1', 'e', 'm')
    
    Returns:
        tuple: Cor RGB
    """
    cores = {
        0: (245, 245, 220),    # Chão - bege claro
        1: (34, 139, 34),      # Parede - verde escuro
        'e': (255, 215, 0),    # Saída - dourado
        'm': (245, 245, 220),  # Posição inicial - mesmo que chão
        'player': (100, 100, 255)  # Player - azul
    }
    return cores.get(tipo_celula, (128, 128, 128))  # Cinza como fallback