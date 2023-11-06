import pygame

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

def main():
    # Inicialização do PyGame
    pygame.init()

    FPS = 30
    clock = pygame.time.Clock()

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
    rato = pygame.Rect(posicao_inicial[0] * largura_celula, posicao_inicial[1] * altura_celula, largura_celula, altura_celula)

    # Define a direção do rato
    global direcao
    direcao = pygame.Vector2(0, altura_celula)

    # Define o retângulo que representa as dimensões do labirinto
    labirinto = pygame.Rect(0, 0, largura_tela, altura_tela)
    
    # Laço principal do jogo
    while True:
        # Atualiza o estado do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move o rato
        rato.move_ip(direcao)

        # Verifica se o rato colidiu com o labirinto
        if rato.colliderect(labirinto):
            # Reverta a última movimentação para evitar colisão
            rato.move_ip(-direcao.x, -direcao.y)
            # Vire o rato 90 graus
            virar()

        # Desenha o jogo na tela
        tela.fill((1, 0, 0))
        
        for i in range(len(l)):
            for j in range(len(l[0])):
                if l[i][j] == 0:
                    pygame.draw.rect(tela, (25, 0, 0), (j * largura_celula, i * altura_celula, largura_celula, altura_celula))
                elif l[i][j] == 1:
                    pygame.draw.rect(tela, (255, 255, 255), (j * largura_celula, i * altura_celula, largura_celula, altura_celula))

        pygame.draw.rect(tela, (255, 0, 0), rato)
        pygame.display.update()
        clock.tick(FPS)

# Vira o rato 90 graus para a esquerda
def virar():
    global direcao
    direcao = direcao.rotate(90)

if __name__ == "__main__":
    main()
