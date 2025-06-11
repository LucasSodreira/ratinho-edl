"""
Gerenciamento da interface do usuário
"""
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
            return "❌ Nenhum caminho encontrado", (255, 100, 100)
        elif estado_jogo['pausado']:
            return "⏸️ PAUSADO - Pressione ESPAÇO para continuar", (255, 255, 100)
        elif estado_jogo['mostrar_exploracao']:
            return "🔍 Explorando labirinto...", (255, 150, 100)
        elif estado_jogo['mostrar_caminho_final']:
            return "✨ Mostrando caminho encontrado...", (100, 255, 100)
        elif estado_jogo['mover_player'] and not estado_jogo['player_finished']:
            return "🐭 Ratinho seguindo o caminho...", (100, 200, 255)
        elif estado_jogo['player_finished']:
            return "🎉 SUCESSO! Ratinho chegou ao destino!", (100, 255, 100)
        else:
            return "✅ Pronto para iniciar", (200, 200, 200)
    
    def _desenhar_estatisticas(self, tela, font, estado_jogo, y_offset, largura_tela):
        """Desenha as estatísticas em duas colunas"""
        if estado_jogo['caminho_encontrado']:
            stats_col1 = [
                f"Algoritmo: {estado_jogo['estatisticas'].get('algoritmo', 'N/A')}",
                f"Tempo: {estado_jogo['estatisticas'].get('tempo_execucao', 0):.4f}s"
            ]
            stats_col2 = [
                f"Nós visitados: {estado_jogo['estatisticas'].get('nos_visitados', 0)}",
                f"Caminho: {len(estado_jogo['caminho_final'])} passos"
            ]
        else:
            stats_col1 = [
                f"Algoritmo: {estado_jogo['estatisticas'].get('algoritmo', 'N/A')}",
                "Status: Caminho não encontrado"
            ]
            stats_col2 = [
                f"Nós visitados: {estado_jogo['estatisticas'].get('nos_visitados', 0)}",
                f"Tempo: {estado_jogo['estatisticas'].get('tempo_execucao', 0):.4f}s"
            ]
        
        # Coluna 1
        for i, stat in enumerate(stats_col1):
            texto = font.render(stat, True, (200, 200, 200))
            tela.blit(texto, (20, y_offset + 30 + (i * 18)))
        
        # Coluna 2
        col2_x = largura_tela // 2
        for i, stat in enumerate(stats_col2):
            texto = font.render(stat, True, (200, 200, 200))
            tela.blit(texto, (col2_x, y_offset + 30 + (i * 18)))
    
    def _desenhar_controles(self, tela, font, estado_jogo, altura_tela):
        """Desenha os controles na parte inferior"""
        if not estado_jogo['caminho_encontrado']:
            controles = [
                "CONTROLES: [R] Reiniciar | [1-4] Algoritmos | [C] Comparar | [ESC] Sair"
            ]
        else:
            controles = [
                "CONTROLES: [ESPAÇO] Pausar/Continuar | [R] Reiniciar | [F11] Tela cheia | [+/-] Velocidade"
            ]
        
        y_controles = altura_tela - 30
        for i, controle in enumerate(controles):
            texto = font.render(controle, True, (150, 150, 150))
            # Centralizar texto
            texto_rect = texto.get_rect()
            x_centro = (tela.get_width() - texto_rect.width) // 2
            tela.blit(texto, (x_centro, y_controles + (i * 20)))
