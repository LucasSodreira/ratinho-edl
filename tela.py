"""
Gerenciamento de tela e dimensões
"""
import pygame
import os

class GerenciadorTela:
    """Gerencia configuração e redimensionamento da tela"""
    
    def __init__(self, jogo):
        self.jogo = jogo
        self.fullscreen = False
        
        # Obter informações da tela
        info_tela = pygame.display.Info()
        self.resolucao_nativa = (info_tela.current_w, info_tela.current_h)
    
    def inicializar_tela_maximizada(self):
        """Inicializa a tela em modo maximizado usando API do Windows"""
        # Configurar variável de ambiente do SDL para centralizar
        os.environ['SDL_WINDOW_CENTERED'] = '1'
        
        # Primeiro criar uma janela pequena
        self.jogo.tela = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Ratinho no Labirinto - BFS Pathfinding")
        
        # Aguardar um pouco para garantir que a janela foi criada
        pygame.time.wait(100)
        
        self._maximizar_com_api_windows()
        
        # Aguardar um pouco mais para garantir que as mudanças foram aplicadas
        pygame.time.wait(100)
        
        self.calcular_dimensoes_tela()
    
    def _maximizar_com_api_windows(self):
        """Usa API do Windows para maximizar a janela"""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Obter handle da janela do pygame
            hwnd = pygame.display.get_wm_info()["window"]
            
            # Constantes do Windows
            SW_MAXIMIZE = 3
            
            # Maximizar janela
            ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
            print("✅ Janela maximizada via API do Windows")
            
        except (ImportError, KeyError, AttributeError, OSError) as e:
            print(f"⚠️ Não foi possível maximizar automaticamente: {e}")
            print("💡 Você pode maximizar manualmente pressionando F11")
    
    def calcular_dimensoes_tela(self):
        """Calcula as dimensões adaptativas baseadas no tamanho atual da tela"""
        largura_tela, altura_tela = self.jogo.tela.get_size()
        
        # Área disponível para o labirinto (descontando UI e margens)
        largura_disponivel = largura_tela - (self.jogo.config.MARGEM_LATERAL * 2)
        altura_disponivel = altura_tela - self.jogo.config.MARGEM_UI - 20
        
        # Calcular tamanho ideal da célula baseado no espaço disponível
        tamanho_celula_largura = largura_disponivel // self.jogo.num_colunas
        tamanho_celula_altura = altura_disponivel // self.jogo.num_linhas
        
        # Usar o menor para manter proporção quadrada
        self.jogo.tamanho_celula = min(tamanho_celula_largura, tamanho_celula_altura, 80)  # Máximo 80px
        self.jogo.tamanho_celula = max(self.jogo.tamanho_celula, 20)  # Mínimo 20px
        
        # Dimensões do labirinto renderizado
        self.jogo.largura_labirinto = self.jogo.num_colunas * self.jogo.tamanho_celula
        self.jogo.altura_labirinto = self.jogo.num_linhas * self.jogo.tamanho_celula
        
        # Posição para centralizar o labirinto
        self.jogo.offset_x = (largura_tela - self.jogo.largura_labirinto) // 2
        self.jogo.offset_y = 20  # Margem superior fixa
    
    def alternar_fullscreen(self):
        """Alterna entre modo fullscreen e janela"""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            self.jogo.tela = pygame.display.set_mode(self.resolucao_nativa, pygame.FULLSCREEN)
        else:
            self.jogo.tela = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
            self._maximizar_com_api_windows()
        
        self.calcular_dimensoes_tela()
        
        # Atualizar player se existir
        if hasattr(self.jogo, 'player_manager') and self.jogo.player_manager:
            self.jogo.player_manager.atualizar_dimensoes(
                self.jogo.tamanho_celula, self.jogo.offset_x, self.jogo.offset_y
            )
    
    def redimensionar_janela(self, nova_largura, nova_altura):
        """Redimensiona a janela e recalcula as dimensões"""
        if not self.fullscreen:
            self.jogo.tela = pygame.display.set_mode((nova_largura, nova_altura), pygame.RESIZABLE)
            self.calcular_dimensoes_tela()
            
            # Atualizar player se existir
            if hasattr(self.jogo, 'player_manager') and self.jogo.player_manager:
                self.jogo.player_manager.atualizar_dimensoes(
                    self.jogo.tamanho_celula, self.jogo.offset_x, self.jogo.offset_y
                )
