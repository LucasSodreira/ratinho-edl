def criar_labirinto(arquivo):
    with open(arquivo, "r") as f:
        primeira_linha = f.readline().strip().split()
        altura = int(primeira_linha[0])
        largura = int(primeira_linha[2])

        labirinto = []
        for _ in range(altura):
            linha = f.readline().strip()
            linha_labirinto = []
            for c in linha:
                if c == '0':
                    # caractere para representar caminho livre
                    linha_labirinto.append(0)
                elif c == '1':
                    # caractere para representar a parede
                    linha_labirinto.append(1)
                elif c == 'e':
                    # caractere para representar a saída
                    linha_labirinto.append('e')
                elif c == 'm':
                    # caractere para representar a posição do rato
                    linha_labirinto.append('m')
            labirinto.append(linha_labirinto)

    return labirinto

def encontrar_posicao_inicial(labirinto):
    for i in range(len(labirinto)):
        for j in range(len(labirinto[i])):
            if labirinto[i][j] == 'm':
                # Invertendo as coordenadas para corresponder à ordem (x, y)
                return (j, i)
            
def encontrar_posicao_saida(labirinto):
    for i in range(len(labirinto) - 1, -1, -1):
        for j in range(len(labirinto[i])):
            if labirinto[i][j] == 'e':
                # Invertendo as coordenadas para corresponder à ordem (x, y)
                return (j, i)