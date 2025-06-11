"""
Gerenciamento centralizado de eventos do jogo
"""
import pygame

class GerenciadorEventos:
    """Centraliza todo o processamento de eventos"""
    
    def __init__(self, jogo):
        self.jogo = jogo
        self.teclas_algoritmos = {
            pygame.K_1: "bfs",
            pygame.K_2: "bfs_otimizado", 
            pygame.K_3: "a_star",
            pygame.K_4: "a_star_euclidiano"
        }
    
    def processar_eventos(self):
        """Processa todos os eventos do jogo"""
        for event in pygame.event.get():
            if not self._processar_evento_sistema(event):
                return False
        
        return True
    
    def _processar_evento_sistema(self, event):
        """Processa eventos do sistema (quit, resize)"""
        if event.type == pygame.QUIT:
            return False
        
        elif event.type == pygame.VIDEORESIZE and not self.jogo.fullscreen:
            self.jogo.gerenciador_tela.redimensionar_janela(event.w, event.h)
        
        elif event.type == pygame.KEYDOWN:
            self._processar_evento_teclado(event)
        
        return True
    
    def _processar_evento_teclado(self, event):
        """Processa eventos de teclado"""
        if event.type != pygame.KEYDOWN:
            return
        
        # Controles de jogo
        if event.key == pygame.K_SPACE:
            self._alternar_pause()
        elif event.key == pygame.K_r:
            self.jogo.reiniciar_busca()
        elif event.key == pygame.K_c:
            self.jogo.comparar_algoritmos()
        elif event.key == pygame.K_ESCAPE:
            return False
        elif event.key == pygame.K_F11:
            self.jogo.alternar_fullscreen()
        elif event.key == pygame.K_q:
            return False
        elif event.key in self.teclas_algoritmos:
            algoritmo = self.teclas_algoritmos[event.key]
            nome_amigavel = self._obter_nome_algoritmo(algoritmo)
            print(f"🔄 Alterando para {nome_amigavel}")
            self.jogo.reiniciar_busca(algoritmo)
        elif event.key in [pygame.K_PLUS, pygame.K_EQUALS]:
            self._aumentar_velocidade()
        elif event.key == pygame.K_MINUS:
            self._diminuir_velocidade()
    
    def _alternar_pause(self):
        """Alterna entre pausado e executando"""
        if self.jogo.pausado:
            self.jogo.pausado = False
            print("▶️ Retomando animação")
        else:
            self.jogo.pausado = True
            print("⏸️ Pausando animação")
    
    def _obter_nome_algoritmo(self, algoritmo):
        """Retorna nome amigável do algoritmo"""
        nomes = {
            "bfs": "BFS básico",
            "bfs_otimizado": "BFS otimizado", 
            "a_star": "A* Manhattan",
            "a_star_euclidiano": "A* Euclidiano"
        }
        return nomes.get(algoritmo, algoritmo)
    
    def _aumentar_velocidade(self):
        """Aumenta a velocidade das animações"""
        config = self.jogo.config
        config.VELOCIDADE_EXPLORACAO = max(1, config.VELOCIDADE_EXPLORACAO - 1)
        config.VELOCIDADE_CAMINHO = max(2, config.VELOCIDADE_CAMINHO - 2)
        print(f"⚡ Velocidade aumentada: {config.VELOCIDADE_EXPLORACAO}")
    
    def _diminuir_velocidade(self):
        """Diminui a velocidade das animações"""
        config = self.jogo.config
        config.VELOCIDADE_EXPLORACAO += 1
        config.VELOCIDADE_CAMINHO += 2
        print(f"🐌 Velocidade diminuída: {config.VELOCIDADE_EXPLORACAO}")
