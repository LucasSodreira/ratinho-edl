import pygame
from rato import Rato

def criar_labirinto(arquivo):
    with open(arquivo, "r") as f:
        linhas = f.readlines()
        labirinto = []
        for linha in linhas:
            linha = linha.strip()
            linha_labirinto = []
            for c in linha:
                if c == '0':
                    linha_labirinto.append(0)
                elif c == '1':
                    linha_labirinto.append(1)
                elif c == 'e':
                    linha_labirinto.append('e')  # Usamos um caractere para representar a saída
                elif c == 'm':
                    linha_labirinto.append('m')  # Usamos um caractere para representar a posição do rato
            labirinto.append(linha_labirinto)
    return labirinto

def encontrar_posicao_inicial(labirinto):
    for i in range(len(labirinto)):
        for j in range(len(labirinto[i])):
            if labirinto[i][j] == 'm':
                return (j, i)  # Invertendo as coordenadas para corresponder à ordem (x, y)
            

def solve_maze(maze, x, y, path):
    if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[0]) or maze[y][x] == 1:
        return False

    if maze[y][x] == 'e' or maze[y][x] == 's':
        return True

    if (x, y) in path:
        return False

    path.append((x, y))

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if solve_maze(maze, x + dx, y + dy, path):
            return True

    path.pop()
    return False

def main():
    # Inicialização do PyGame
    pygame.init()

    FPS = 30
    clock = pygame.time.Clock()
    

    frames = [pygame.image.load('person/frame-1.png'), 
              pygame.image.load('person/frame-2.png'),
              pygame.image.load('person/frame-3.png'), 
              pygame.image.load('person/frame-4.png')]

    frame_index = 0
    frame_change_delay = 1  # Altere isso para ajustar a velocidade da animação
    frame_counter = 0

    l = criar_labirinto("labirinto.txt")

    num_linhas = len(l)
    num_colunas = len(l[0])

    # Calcula o tamanho da tela com base no tamanho do labirinto
    largura_tela = num_colunas * 50
    altura_tela = num_linhas * 50
    tela = pygame.display.set_mode((largura_tela, altura_tela))

    # Calcula o tamanho das células do labirinto
    largura_celula = largura_tela // num_colunas
    altura_celula = altura_tela // num_linhas

    # Calcula a posição inicial do rato
    posicao_inicial = encontrar_posicao_inicial(l)
    
    # Define a direção do rato
    global direcao
    direcao = pygame.Vector2(0, altura_celula)

    # Define o retângulo que representa as dimensões do labirinto
    labirinto = pygame.Rect(0, 0, largura_tela, altura_tela)
    
    rato = Rato(frames, posicao_inicial[0] * largura_celula, posicao_inicial[1] * altura_celula, largura_celula, altura_celula)
    grupo_de_sprites = pygame.sprite.Group()
    grupo_de_sprites.add(rato)
    
    # Laço principal do jogo
    while True:
        # Atualiza o estado do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        frame_counter += 4

        if frame_counter <= frame_change_delay:
            frame_index = (frame_index + 1) % len(frames)
            frame_counter = 0

        path = []  # Para armazenar o caminho da resolução
        solve_maze(l, posicao_inicial[0], posicao_inicial[1], path)

        # Desenha o jogo na tela
        tela.fill((0, 0, 0))
        
        for i in range(len(l)):
            for j in range(len(l[0])):
                if l[i][j] == 0:
                    pygame.draw.rect(tela, (255, 255, 255), (j * largura_celula, i * altura_celula, largura_celula, altura_celula))
                elif l[i][j] == 1:
                    pygame.draw.rect(tela, (0, 0, 0), (j * largura_celula, i * altura_celula, largura_celula, altura_celula))
                elif l[i][j] == 'e':
                    pygame.draw.rect(tela, (0, 255, 0), (j * largura_celula, i * altura_celula, largura_celula, altura_celula))                    

        # Desenhe o rato do grupo de sprites
        grupo_de_sprites.draw(tela)
        
        if path:
            rato.rect.topleft = path[0][0] * largura_celula, path[0][1] * altura_celula
        
        pygame.display.update()
        clock.tick(FPS)
        
if __name__ == "__main__":
    main()
