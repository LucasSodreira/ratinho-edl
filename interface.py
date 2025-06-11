import pygame

class GerenciadorInterface:
    """Gerencia toda a interface do usuário"""
    
    def __init__(self, config):
        self.config = config
    
    def desenhar_ui(self, tela, estado_jogo):
        """Desenha a interface do usuário de forma responsiva"""
        largura_tela, altura_tela = tela.get_size()
        y_offset = estado_jogo['offset_y'] + estado_jogo['altura_labirinto'] + 20
        
        # Fundo da UI com largura responsiva
        altura_ui = min(100, altura_tela - y_offset - 10)
        pygame.draw.rect(tela, (20, 20, 20), 
                        (10, y_offset - 5, largura_tela - 20, altura_ui))
        
        # Tamanhos de fonte adaptativos
        tamanho_fonte_base = max(16, min(32, estado_jogo['tamanho_celula'] // 2))
        font_pequena = pygame.font.Font(None, max(18, tamanho_fonte_base - 6))
        font_media = pygame.font.Font(None, tamanho_fonte_base + 4)
        
        # Desenhar status
        self._desenhar_status(tela, font_media, estado_jogo, y_offset)
        
        # Desenhar estatísticas
        if estado_jogo['estatisticas'] and altura_ui > 60:
            self._desenhar_estatisticas(tela, font_pequena, estado_jogo, y_offset, largura_tela)
        
        # Desenhar controles
        self._desenhar_controles(tela, font_pequena, estado_jogo, altura_tela)
    
    def _desenhar_status(self, tela, font, estado_jogo, y_offset):
        """Desenha o status atual do jogo"""
        status, cor = self._obter_status_e_cor(estado_jogo)
        texto_status = font.render(status, True, cor)
        tela.blit(texto_status, (20, y_offset))
    
    def _obter_status_e_cor(self, estado_jogo):
        """Determina o status atual e sua cor"""
        if not estado_jogo['caminho_encontrado']:
            if estado_jogo['pausado']:
                return "❌ CAMINHO NÃO ENCONTRADO - Pressione ESPAÇO para ver exploração", (255, 100, 100)
            elif estado_jogo['mostrar_exploracao']:
                return f"Explorando (sem saída)... {estado_jogo['indice_exploracao']}/{len(estado_jogo['caminhos_explorados'])}", (255, 150, 150)
            else:
                return "❌ Rato não conseguiu encontrar a saída! Pressione R para tentar outro labirinto", (255, 100, 100)
        elif estado_jogo['pausado']:
            return "PAUSADO - Pressione ESPAÇO para iniciar", self.config.COR_DESTAQUE
        elif estado_jogo['mostrar_exploracao']:
            return f"Explorando... {estado_jogo['indice_exploracao']}/{len(estado_jogo['caminhos_explorados'])}", self.config.COR_EXPLORACAO
        elif estado_jogo['mostrar_caminho_final']:
            return f"Menor caminho: {estado_jogo['indice_caminho']}/{len(estado_jogo['caminho_final'])} passos", self.config.COR_CAMINHO_FINAL
        elif estado_jogo['mover_player'] and not estado_jogo['player_finished']:
            return f"Rato se movendo... {estado_jogo['indice_player']}/{len(estado_jogo['caminho_final'])}", self.config.COR_TEXTO
        elif estado_jogo['player_finished']:
            return "✓ Saída encontrada! Pressione R para reiniciar", self.config.COR_CAMINHO_FINAL
        else:
            return "Pronto", self.config.COR_TEXTO
    
    def _desenhar_estatisticas(self, tela, font, estado_jogo, y_offset, largura_tela):
        """Desenha as estatísticas em duas colunas"""
        if estado_jogo['caminho_encontrado']:
            algoritmo = estado_jogo['estatisticas'].get('algoritmo', 'Desconhecido')
            stats_col1 = [
                f"Algoritmo: {algoritmo}",
                f"Nós visitados: {estado_jogo['estatisticas']['nos_visitados']}",
                f"Tempo: {estado_jogo['estatisticas']['tempo_execucao']:.3f}s"
            ]
            stats_col2 = [
                f"Eficiência: {estado_jogo['estatisticas']['eficiencia']:.1%}",
                f"Tamanho célula: {estado_jogo['tamanho_celula']}px"
            ]
        else:
            algoritmo = estado_jogo['estatisticas'].get('algoritmo', 'Desconhecido')
            stats_col1 = [
                f"Algoritmo: {algoritmo}",
                f"Nós explorados: {estado_jogo['estatisticas']['nos_visitados']}",
                f"Tempo: {estado_jogo['estatisticas']['tempo_execucao']:.3f}s"
            ]
            stats_col2 = [
                f"Status: Sem caminho disponível",
                f"Tamanho célula: {estado_jogo['tamanho_celula']}px"
            ]
        
        # Coluna 1
        for i, stat in enumerate(stats_col1):
            cor_stat = self.config.COR_TEXTO if estado_jogo['caminho_encontrado'] else (255, 180, 180)
            texto = font.render(stat, True, cor_stat)
            tela.blit(texto, (20, y_offset + 30 + i * 20))
        
        # Coluna 2
        col2_x = largura_tela // 2
        for i, stat in enumerate(stats_col2):
            cor_stat = self.config.COR_TEXTO if estado_jogo['caminho_encontrado'] else (255, 180, 180)
            texto = font.render(stat, True, cor_stat)
            tela.blit(texto, (col2_x, y_offset + 30 + i * 20))
    
    def _desenhar_controles(self, tela, font, estado_jogo, altura_tela):
        """Desenha os controles na parte inferior"""
        if not estado_jogo['caminho_encontrado']:
            controles = "❌ Sem saída! | ESPAÇO=Ver busca | R=A* | 1-4=Algoritmos | C=Comparar | F11=Fullscreen | ESC=Sair"
        else:
            controles = "⚡ ESPAÇO=Play/Pause | R=A* | 1-4=Algoritmos | C=Comparar | F11=Fullscreen | ESC=Sair | +/-=Velocidade"
        
        texto_controles = font.render(controles, True, (200, 200, 200))
        tela.blit(texto_controles, (20, altura_tela - 30))
