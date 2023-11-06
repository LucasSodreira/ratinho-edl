import pygame

# Maze size
n = 5

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


def isValid(n, maze, x, y, res):
    if x >= 0 and y >= 0 and x < n and y < n and maze[x][y] == 0 and res[x][y] == 0:
        return True
    return False

def RatMaze(n, maze, move_x, move_y, x, y, res):
    if x == n-1 and y == n-1:
        return True
    for i in range(4):
        x_new = x + move_x[i]
        y_new = y + move_y[i]
        if isValid(n, maze, x_new, y_new, res):
            res[x_new][y_new] = 1
            if RatMaze(n, maze, move_x, move_y, x_new, y_new, res):
                return True
            res[x_new][y_new] = 0
    return False

def solveMaze(maze):
    res = [[0 for i in range(n)] for i in range(n)]
    res[0][0] = 1
    move_x = [-1, 1, 0, 0]
    move_y = [0, 0, -1, 1]
    
    if RatMaze(n, maze, move_x, move_y, 0, 0, res):
        for i in range(n):
            for j in range(n):
                print(res[i][j], end=' ')
            print()
    else:
        print('Solution does not exist')

# Create a simple maze
maze = [
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0]
]

# Solve the maze
solveMaze(maze)

# Initialize Pygame
pygame.init()

FPS = 30
clock = pygame.time.Clock()

l = criar_labirinto("labirinto.txt")

# Set up display dimensions
screen_width, screen_height = 800, 600
cell_size = screen_width // n
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rat in a Maze")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Rat:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x * cell_size, self.y * cell_size, cell_size, cell_size))

def draw_maze():
    for i in range(n):
        for j in range(n):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size))
            if maze[i][j] == 0:
                pygame.draw.rect(screen, WHITE, (j * cell_size, i * cell_size, cell_size, cell_size))

rat = Rat(0, 0)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)
    draw_maze()
    rat.draw()
    pygame.display.update()
    
    # Move the rat along the path found by the algorithm
    if rat.x < n - 1 and maze[rat.y][rat.x + 1] == 1:
        rat.move(1, 0)
    elif rat.y < n - 1 and maze[rat.y + 1][rat.x] == 1:
        rat.move(0, 1)

    pygame.time.delay(500)  # Delay for animation

pygame.quit()
