"""
Gerenciamento de labirintos - carregamento, validação e utilitários
"""
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
            raise FileNotFoundError(f"Arquivo de labirinto não encontrado: {arquivo}")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            if not linhas:
                raise ValueError("Arquivo de labirinto está vazio")
            
            # Parse da primeira linha para obter dimensões
            primeira_linha = linhas[0].strip()
            altura, largura = GerenciadorLabirinto._parse_dimensoes(primeira_linha)
            
            # Processar o labirinto
            labirinto = []
            posicao_rato_atual = None
            posicao_saida_atual = None
            
            for linha_num, linha in enumerate(linhas[1:altura+1], 1):
                linha_labirinto, pos_rato, pos_saida = GerenciadorLabirinto._processar_linha(
                    linha.strip(), linha_num, posicao_rato_atual, posicao_saida_atual
                )
                
                if pos_rato:
                    posicao_rato_atual = pos_rato
                if pos_saida:
                    posicao_saida_atual = pos_saida
                
                labirinto.append(linha_labirinto)
            
            # Validar labirinto
            validacao = GerenciadorLabirinto.validar_labirinto(labirinto)
            if not validacao['valido']:
                raise ValueError(f"Labirinto inválido: {validacao['erro']}")
            
            return labirinto
                
        except (ValueError, IOError) as e:
            raise ValueError(f"Erro ao carregar labirinto: {e}")
    
    @staticmethod
    def _parse_dimensoes(primeira_linha):
        """Parse das dimensões da primeira linha do arquivo"""
        if 'x' in primeira_linha.lower():
            # Formato: "20x30" ou "20 x 30"
            partes = primeira_linha.lower().replace('x', ' ').split()
        elif ',' in primeira_linha:
            # Formato: "20,30" ou "20, 30"
            partes = primeira_linha.replace(',', ' ').split()
        else:
            # Formato: "20 30"
            partes = primeira_linha.split()
        
        if len(partes) < 2:
            raise ValueError(f"Formato de dimensões inválido: {primeira_linha}")
        else:
            altura = int(partes[0])
            largura = int(partes[1])
        
        return altura, largura
    
    @staticmethod
    def _processar_linha(linha, linha_num, posicao_rato_atual, posicao_saida_atual):
        """Processa uma linha do labirinto"""
        linha_labirinto = []
        pos_rato = None
        pos_saida = None
        
        for j, c in enumerate(linha):
            if c == '0' or c == ' ':
                linha_labirinto.append(0)  # Caminho livre
            elif c == '1' or c == '#':
                linha_labirinto.append(1)  # Parede
            elif c.lower() == 'm':
                linha_labirinto.append('m')  # Posição do rato
                if posicao_rato_atual is not None:
                    raise ValueError(f"Múltiplas posições de rato encontradas")
                pos_rato = (j, linha_num - 1)
            elif c.lower() == 'e':
                linha_labirinto.append('e')  # Saída
                if posicao_saida_atual is not None:
                    raise ValueError(f"Múltiplas saídas encontradas")
                pos_saida = (j, linha_num - 1)
            else:
                # Caractere desconhecido, assumir como parede
                linha_labirinto.append(1)
        
        return linha_labirinto, pos_rato, pos_saida
    
    @staticmethod
    def encontrar_posicao_inicial(labirinto):
        """Encontra a posição inicial do rato no labirinto"""
        for i in range(len(labirinto)):
            for j in range(len(labirinto[i])):
                if labirinto[i][j] == 'm':
                    return (j, i)
        return None
                
    @staticmethod
    def encontrar_posicao_saida(labirinto):
        """Encontra a posição da saída no labirinto"""
        for i in range(len(labirinto) - 1, -1, -1):
            for j in range(len(labirinto[i]) - 1, -1, -1):
                if labirinto[i][j] == 'e':
                    return (j, i)
        return None
    
    @staticmethod
    def validar_labirinto(labirinto):
        """
        Valida se o labirinto tem uma estrutura válida.
        
        Returns:
            dict: Informações sobre a validação
        """
        if not labirinto:
            return {'valido': False, 'erro': 'Labirinto vazio'}
        
        altura = len(labirinto)
        largura = len(labirinto[0]) if altura > 0 else 0
        
        # Verificar se todas as linhas têm o mesmo tamanho
        for i, linha in enumerate(labirinto):
            if len(linha) != largura:
                return {
                    'valido': False, 
                    'erro': f'Linha {i+1} tem tamanho diferente ({len(linha)} vs {largura})'
                }
        
        # Contar elementos especiais
        ratos = saidas = 0
        for linha in labirinto:
            for celula in linha:
                if celula == 'm':
                    ratos += 1
                elif celula == 'e':
                    saidas += 1
        
        if ratos != 1:
            return {'valido': False, 'erro': f'Deve haver exatamente 1 rato, encontrados: {ratos}'}
        if saidas != 1:
            return {'valido': False, 'erro': f'Deve haver exatamente 1 saída, encontradas: {saidas}'}

        return {
            'valido': True,
            'altura': altura,
            'largura': largura,
            'ratos': ratos,
            'saidas': saidas
        }
    
    @staticmethod
    def eh_posicao_valida(x, y, labirinto):
        """
        Verifica se uma posição é válida no labirinto.
        
        Args:
            x, y: Coordenadas a verificar
            labirinto: Matriz do labirinto
            
        Returns:
            bool: True se a posição é válida e transitável
        """
        if not labirinto:
            return False
        
        altura = len(labirinto)
        largura = len(labirinto[0]) if altura > 0 else 0
        
        # Verificar limites
        if x < 0 or x >= largura or y < 0 or y >= altura:
            return False
        
        # Verificar se não é parede
        celula = labirinto[y][x]
        return celula != 1
