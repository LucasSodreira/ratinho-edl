import os

class GerenciadorLabirinto:
    """Gerencia o carregamento e validação de labirintos"""
    
    @staticmethod
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
                altura, largura = GerenciadorLabirinto._parse_dimensoes(primeira_linha)
                
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
                    
                    linha_labirinto, pos_rato, pos_saida = GerenciadorLabirinto._processar_linha(
                        linha, linha_num, posicao_rato, posicao_saida
                    )
                    
                    if pos_rato:
                        posicao_rato = pos_rato
                    if pos_saida:
                        posicao_saida = pos_saida
                    
                    labirinto.append(linha_labirinto)
                
                if posicao_rato is None:
                    raise ValueError("Posição do rato ('m') não encontrada no labirinto")
                if posicao_saida is None:
                    raise ValueError("Saída ('e') não encontrada no labirinto")
                    
                return labirinto
                
        except (ValueError, IOError) as e:
            raise ValueError(f"Erro ao carregar labirinto: {e}")
    
    @staticmethod
    def _parse_dimensoes(primeira_linha):
        """Parse das dimensões da primeira linha do arquivo"""
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
        
        return altura, largura
    
    @staticmethod
    def _processar_linha(linha, linha_num, posicao_rato_atual, posicao_saida_atual):
        """Processa uma linha do labirinto"""
        linha_labirinto = []
        pos_rato = None
        pos_saida = None
        
        for j, c in enumerate(linha):
            if c == '0':
                linha_labirinto.append(0)
            elif c == '1':
                linha_labirinto.append(1)
            elif c == 'e':
                linha_labirinto.append('e')
                if posicao_saida_atual is not None:
                    raise ValueError("Múltiplas saídas encontradas no labirinto")
                pos_saida = (j, linha_num)
            elif c == 'm':
                linha_labirinto.append('m')
                if posicao_rato_atual is not None:
                    raise ValueError("Múltiplas posições do rato encontradas no labirinto")
                pos_rato = (j, linha_num)
            else:
                raise ValueError(f"Caractere inválido '{c}' na linha {linha_num + 1}, posição {j + 1}")
        
        return linha_labirinto, pos_rato, pos_saida
    
    @staticmethod
    def encontrar_posicao_inicial(labirinto):
        """Encontra a posição inicial do rato no labirinto"""
        for i in range(len(labirinto)):
            for j in range(len(labirinto[i])):
                if labirinto[i][j] == 'm':
                    # Invertendo as coordenadas para corresponder à ordem (x, y)
                    return (j, i)
                
    @staticmethod
    def encontrar_posicao_saida(labirinto):
        """Encontra a posição da saída no labirinto"""
        for i in range(len(labirinto) - 1, -1, -1):
            for j in range(len(labirinto[i])):
                if labirinto[i][j] == 'e':
                    # Invertendo as coordenadas para corresponder à ordem (x, y)
                    return (j, i)
    
    @staticmethod
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
    
    @staticmethod
    def eh_posicao_valida(x, y, labirinto):
        """Verifica se uma posição é válida no labirinto"""
        return (0 <= x < len(labirinto[0]) and 
                0 <= y < len(labirinto) and 
                labirinto[y][x] != 1)
