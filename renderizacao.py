"""
Sistema de renderização do jogo
"""
import pygame
from imgs import *

class GerenciadorRenderizacao:
    """Gerencia toda a renderização visual do jogo"""
    
    def __init__(self, jogo):
        self.jogo = jogo
        self._cache_imagens = {}
    
    def renderizar_frame_completo(self):
        """Renderiza um frame completo do jogo"""
        self.jogo.tela.fill(self.jogo.config.COR_FUNDO)
        
        self.desenhar_labirinto()
        self.desenhar_caminhos_explorados()
        self.desenhar_caminho_final()
        self.desenhar_player()
        
        # Interface renderizada pelo GerenciadorInterface
        self.jogo.interface.desenhar_ui(self.jogo.tela, self.jogo.obter_estado_jogo())
    
    def desenhar_labirinto(self):
        """Desenha o labirinto base com posicionamento centralizado"""
        for i in range(len(self.jogo.labirinto)):
            for j in range(len(self.jogo.labirinto[i])):
                x_pixel = self.jogo.offset_x + (j * self.jogo.tamanho_celula)
                y_pixel = self.jogo.offset_y + (i * self.jogo.tamanho_celula)
                self._desenhar_celula_labirinto(i, j, x_pixel, y_pixel)
    
    def _desenhar_celula_labirinto(self, i, j, x_pixel, y_pixel):
        """Desenha uma célula específica do labirinto"""
        tipo_celula = self.jogo.labirinto[i][j]
        imagem = self._obter_imagem_celula(tipo_celula)
        
        imagem_redimensionada = self._redimensionar_imagem_cached(
            imagem, self.jogo.tamanho_celula, self.jogo.tamanho_celula
        )
        
        self.jogo.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
    
    def _obter_imagem_celula(self, tipo_celula):
        """Retorna a imagem correspondente ao tipo de célula"""
        mapeamento = {
            0: imagem_chao,
            1: imagen_arvore,
            'e': imagem_casa,
            'm': imagem_chao
        }
        return mapeamento.get(tipo_celula, imagem_chao)
    
    def desenhar_caminhos_explorados(self):
        """Desenha os caminhos explorados com transparência"""
        for i in range(min(self.jogo.indice_exploracao, len(self.jogo.caminhos_explorados))):
            x, y = self.jogo.caminhos_explorados[i]
            x_pixel = self.jogo.offset_x + (x * self.jogo.tamanho_celula)
            y_pixel = self.jogo.offset_y + (y * self.jogo.tamanho_celula)
            self._desenhar_overlay_exploracao(x_pixel, y_pixel)
    
    def _desenhar_overlay_exploracao(self, x, y):
        """Desenha overlay de exploração em uma posição"""
        superficie = pygame.Surface((self.jogo.tamanho_celula, self.jogo.tamanho_celula))
        superficie.set_alpha(128)  # 50% transparente
        
        cor = (self.jogo.config.COR_EXPLORACAO if self.jogo.caminho_encontrado 
               else (255, 180, 180))
        superficie.fill(cor)
        
        self.jogo.tela.blit(superficie, (x, y))
    
    def desenhar_caminho_final(self):
        """Desenha o caminho final encontrado"""
        if not self.jogo.caminho_encontrado:
            return
        
        for i in range(min(self.jogo.indice_caminho, len(self.jogo.caminho_final))):
            x, y = self.jogo.caminho_final[i]
            x_pixel = self.jogo.offset_x + (x * self.jogo.tamanho_celula)
            y_pixel = self.jogo.offset_y + (y * self.jogo.tamanho_celula)
            
            # Overlay do caminho final
            superficie = pygame.Surface((self.jogo.tamanho_celula, self.jogo.tamanho_celula))
            superficie.set_alpha(180)  # Mais opaco que exploração
            superficie.fill(self.jogo.config.COR_CAMINHO_FINAL)
            
            self.jogo.tela.blit(superficie, (x_pixel, y_pixel))
    
    def desenhar_player(self):
        """Desenha o player na posição atual"""
        if self.jogo.mover_player and self.jogo.caminho_encontrado:
            self._atualizar_posicao_player()
        
        if self.jogo.player_manager and self.jogo.player_manager.player:
            self.jogo.player_manager.desenhar(self.jogo.tela)
    
    def _atualizar_posicao_player(self):
        """Atualiza a posição do player baseada no progresso da animação"""
        if (self.jogo.indice_player < len(self.jogo.caminho_final) and 
            self.jogo.player_manager):
            
            x, y = self.jogo.caminho_final[self.jogo.indice_player]
            self.jogo.player_manager.mover_para_posicao(x, y)
    
    def _redimensionar_imagem_cached(self, imagem, largura, altura):
        """Redimensiona uma imagem com cache para performance"""
        chave_cache = (id(imagem), largura, altura)
        
        if chave_cache not in self._cache_imagens:
            imagem_redimensionada = pygame.transform.scale(imagem, (largura, altura))
            self._cache_imagens[chave_cache] = imagem_redimensionada
        
        return self._cache_imagens[chave_cache]
    
    def limpar_cache(self):
        """Limpa o cache de imagens"""
        self._cache_imagens.clear()
