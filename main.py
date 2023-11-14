import pygame
from imgs import *
from rato import *
class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.finished = False  # Adicione um atributo para controlar se o jogador terminou

cache = {}

def is_valid(x, y, maze):
    return 0 <= x < len(maze[0]) and 0 <= y < len(maze)

def find_exit(maze, x, y, path, correct_path, wrong_path):
    if not is_valid(x, y, maze) or maze[y][x] == 1:
        return False

    if (x, y) in cache:
        return cache[(x, y)]

    if maze[y][x] == 'e':
        player.finished = True
        return True

    if (x, y) in path:
        return False

    path.append((x, y))
    
    if find_exit(maze, x + 1, y, path, correct_path, wrong_path):
        correct_path.append((x, y))
        cache[(x, y)] = True
        return True
    
    elif find_exit(maze, x - 1, y, path, correct_path, wrong_path):
        correct_path.append((x, y))
        cache[(x, y)] = True
        return True

    elif find_exit(maze, x, y - 1, path, correct_path, wrong_path):
        correct_path.append((x, y))
        cache[(x, y)] = True
        return True

    elif find_exit(maze, x, y + 1, path, correct_path, wrong_path):
        correct_path.append((x, y))
        cache[(x, y)] = True
        return True

    wrong_path.append((x, y))
    cache[(x, y)] = False

    path.pop()
    return False


# Inicialização do PyGame
pygame.init()

FPS = 30
clock = pygame.time.Clock()

l = criar_labirinto("labirinto.txt")

num_linhas = len(l)
num_colunas = len(l[0])

# Calcula o tamanho da tela com base no tamanho do labirinto
largura_tela = num_colunas * 30
altura_tela = num_linhas * 30
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Calcula o tamanho das células do labirinto
largura_celula = largura_tela // num_colunas
altura_celula = altura_tela // num_linhas

# Calcula a posição inicial do rato
posicao_inicial = encontrar_posicao_inicial(l)
posicao_saida = encontrar_posicao_saida(l)
posicao_atual = encontrar_posicao_inicial(l)

player_image = pygame.image.load('person/frame-1.png')
player = Player(posicao_inicial[0] * largura_celula, posicao_inicial[1] * altura_celula, player_image)

correct_path = []  # Pilha para o caminho correto
wrong_path = []    # Pilha para o caminho errado

# Crie a lista de coordenadas do caminho correto e ordene-as

# Laço principal do jogo
running = True  # Variável para controlar o loop principal

def redimensionar_imagem(imagem, largura, altura):
    return pygame.transform.scale(imagem, (largura, altura))

while running:

    # Atualiza o estado do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Se o usuário fechar a janela, encerre o jogo

    find_exit(l, posicao_inicial[0], posicao_inicial[1], [], correct_path, wrong_path)

    path_coordinates = correct_path[:]
    path_coordinates.reverse()
    
    # Desenha o jogo na tela
    tela.fill((0,255,32))
    
    tela.blit(player.image, (player.rect.x, player.rect.y))

    for i in range(len(l)):
        for j in range(len(l[0])):
            # Desenha a imagem correspondente à condição
            if l[i][j] == 0:
                imagem_redimensionada = redimensionar_imagem(imagem_chao, largura_celula, altura_celula)
                tela.blit(imagem_redimensionada, (j * largura_celula, i * altura_celula))
            if l[i][j] == 1:
                    imagem_redimensionada = redimensionar_imagem(imagen_arvore, largura_celula, altura_celula)
                    tela.blit(imagem_redimensionada, (j * largura_celula, i * altura_celula))
            if l[i][j] == 'e':
                imagem_redimensionada = redimensionar_imagem(imagem_casa, largura_celula, altura_celula)
                tela.blit(imagem_redimensionada, (j * largura_celula, i * altura_celula))
            if l[i][j] == 'm':
                imagem_redimensionada = redimensionar_imagem(imagem_casa, largura_celula, altura_celula)
                tela.blit(imagem_redimensionada, (j * largura_celula, i * altura_celula))

            font = pygame.font.Font(None, 8)
            text = font.render(f'({j+1},{i+1})', True, (255, 255, 255))
            text_rect = text.get_rect(center=(
                j * largura_celula + largura_celula // 2, i * altura_celula + altura_celula // 2))
            tela.blit(text, text_rect)
            
    pygame.display.update()
    clock.tick(FPS)

    for x, y in path_coordinates:
        pygame.draw.rect(tela, (0, 0, 255), (x * largura_celula, y * altura_celula, largura_celula, altura_celula))
        pygame.display.update()  # Atualize a tela para mostrar o retângulo
        pygame.time.delay(10)
        
    for x, y in wrong_path: 
        pygame.draw.rect(tela, (25, 25, 0), (x * largura_celula, y * altura_celula, largura_celula, altura_celula))
        pygame.display.update()  # Atualize a tela para mostrar o retângulo
        pygame.time.delay(10)
        