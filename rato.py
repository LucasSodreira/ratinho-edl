from collections import deque
import os
import time

def criar_labirinto(arquivo):
    """
    Carrega o labirinto de um arquivo texto.
    
    Args:
        arquivo (str): Caminho para o arquivo do labirinto
        
    Returns:
        list: Matriz representando o labirinto
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        ValueError: Se o formato do arquivo for inválido
    """
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo '{arquivo}' não encontrado!")
    
    try:
        with open(arquivo, "r", encoding='utf-8') as f:
            primeira_linha = f.readline().strip()
            
            # Suporta diferentes formatos: "altura x largura", "alturaxlargura", "altura,largura"
            if 'x' in primeira_linha.lower():
                partes = primeira_linha.lower().replace('x', ' x ').split()
            elif ',' in primeira_linha:
                partes = primeira_linha.replace(',', ' , ').split()
            else:
                partes = primeira_linha.split()
            
            if len(partes) < 3:
                # Tentar formato simples como "18x18"
                if 'x' in primeira_linha.lower():
                    dimensoes = primeira_linha.lower().split('x')
                    if len(dimensoes) == 2:
                        altura = int(dimensoes[0].strip())
                        largura = int(dimensoes[1].strip())
                    else:
                        raise ValueError("Formato inválido na primeira linha. Esperado: 'altura x largura' ou 'alturaxlargura'")
                else:
                    raise ValueError("Formato inválido na primeira linha. Esperado: 'altura x largura' ou 'alturaxlargura'")
            else:
                altura = int(partes[0])
                largura = int(partes[2])
            
            if altura <= 0 or largura <= 0:
                raise ValueError("Dimensões do labirinto devem ser positivas")

            print(f"Carregando labirinto: {altura}x{largura}")

            labirinto = []
            posicao_rato = None
            posicao_saida = None
            
            for linha_num in range(altura):
                linha = f.readline().strip()
                if not linha:  # Linha vazia
                    raise ValueError(f"Arquivo tem menos linhas que o esperado. Esperado: {altura}, linha {linha_num + 1} está vazia")
                
                if len(linha) != largura:
                    raise ValueError(f"Linha {linha_num + 1} tem tamanho incorreto. Esperado: {largura}, encontrado: {len(linha)}")
                
                linha_labirinto = []
                for j, c in enumerate(linha):
                    if c == '0':
                        linha_labirinto.append(0)
                    elif c == '1':
                        linha_labirinto.append(1)
                    elif c == 'e':
                        linha_labirinto.append('e')
                        if posicao_saida is not None:
                            raise ValueError("Múltiplas saídas encontradas no labirinto")
                        posicao_saida = (j, linha_num)
                    elif c == 'm':
                        linha_labirinto.append('m')
                        if posicao_rato is not None:
                            raise ValueError("Múltiplas posições do rato encontradas no labirinto")
                        posicao_rato = (j, linha_num)
                    else:
                        raise ValueError(f"Caractere inválido '{c}' na linha {linha_num + 1}, posição {j + 1}")
                
                labirinto.append(linha_labirinto)
            
            if posicao_rato is None:
                raise ValueError("Posição do rato ('m') não encontrada no labirinto")
            if posicao_saida is None:
                raise ValueError("Saída ('e') não encontrada no labirinto")
                
            return labirinto
            
    except (ValueError, IOError) as e:
        raise ValueError(f"Erro ao carregar labirinto: {e}")

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

def bfs_menor_caminho(labirinto, inicio, fim):
    """
    Usa BFS otimizado para encontrar o menor caminho.
    
    Args:
        labirinto: Matriz do labirinto
        inicio: Tupla (x, y) da posição inicial
        fim: Tupla (x, y) da posição final
        
    Returns:
        tuple: (caminho_final, caminhos_explorados, estatisticas)
    """
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
            
            # Verificação otimizada
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

def eh_posicao_valida(x, y, labirinto):
    """Verifica se uma posição é válida no labirinto"""
    return (0 <= x < len(labirinto[0]) and 
            0 <= y < len(labirinto) and 
            labirinto[y][x] != 1)

def validar_labirinto(labirinto):
    """
    Valida se o labirinto tem uma estrutura válida.
    
    Returns:
        dict: Informações sobre a validação
    """
    if not labirinto:
        return {"valido": False, "erro": "Labirinto vazio"}
    
    altura = len(labirinto)
    largura = len(labirinto[0]) if altura > 0 else 0
    
    # Verificar se todas as linhas têm o mesmo tamanho
    for i, linha in enumerate(labirinto):
        if len(linha) != largura:
            return {"valido": False, "erro": f"Linha {i} tem tamanho inconsistente"}
    
    # Contar elementos especiais
    ratos = saidas = 0
    for linha in labirinto:
        for celula in linha:
            if celula == 'm':
                ratos += 1
            elif celula == 'e':
                saidas += 1
    
    if ratos != 1:
        return {"valido": False, "erro": f"Deve haver exatamente 1 rato, encontrados: {ratos}"}
    if saidas != 1:
        return {"valido": False, "erro": f"Deve haver exatamente 1 saída, encontradas: {saidas}"}
    
    return {
        "valido": True,
        "dimensoes": (largura, altura),
        "total_celulas": largura * altura,
        "paredes": sum(linha.count(1) for linha in labirinto),
        "caminhos_livres": sum(linha.count(0) for linha in labirinto)
    }