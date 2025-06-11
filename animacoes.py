"""
Sistema de animações do jogo
"""
import pygame

class GerenciadorAnimacoes:
    """Gerencia todas as animações do jogo"""
    
    def __init__(self, jogo):
        self.jogo = jogo
        self.contador_frames = 0
    
    def atualizar(self):
        """Atualiza todas as animações"""
        if not self.jogo.pausado:
            self.contador_frames += 1
            self.contador_frames = self._processar_fases_animacao()
    
    def _processar_fases_animacao(self):
        """Processa as diferentes fases da animação"""
        # Fase 1: Exploração
        if self._atualizar_fase_exploracao():
            return 0
        
        # Fase 2: Caminho final
        if self._atualizar_fase_caminho_final():
            return 0
        
        # Fase 3: Movimento do player
        self._atualizar_fase_movimento_player()
        
        return self.contador_frames
    
    def _atualizar_fase_exploracao(self):
        """Atualiza a fase de exploração"""
        if (self.jogo.mostrar_exploracao and 
            self.contador_frames % self.jogo.config.VELOCIDADE_EXPLORACAO == 0):
            
            self.jogo.indice_exploracao += 1
            
            if self.jogo.indice_exploracao >= len(self.jogo.caminhos_explorados):
                self.jogo.mostrar_exploracao = False
                
                if self.jogo.caminho_encontrado:
                    self.jogo.mostrar_caminho_final = True
                else:
                    self.jogo.pausado = True
                
                return True
        
        return False
    
    def _atualizar_fase_caminho_final(self):
        """Atualiza a fase do caminho final"""
        if (self.jogo.mostrar_caminho_final and 
            self.jogo.caminho_encontrado and 
            self.contador_frames % self.jogo.config.VELOCIDADE_CAMINHO == 0):
            
            self.jogo.indice_caminho += 1
            
            if self.jogo.indice_caminho >= len(self.jogo.caminho_final):
                self.jogo.mostrar_caminho_final = False
                self.jogo.mover_player = True
                return True
        
        return False
    
    def _atualizar_fase_movimento_player(self):
        """Atualiza a fase de movimento do player"""
        if (self.jogo.mover_player and 
            self.jogo.caminho_encontrado and 
            self.contador_frames % self.jogo.config.VELOCIDADE_PLAYER == 0):
            
            self.jogo.indice_player += 1
            
            if self.jogo.indice_player >= len(self.jogo.caminho_final):
                self.jogo.player_manager.player.finished = True
    
    def resetar(self):
        """Reseta o estado das animações"""
        self.contador_frames = 0
