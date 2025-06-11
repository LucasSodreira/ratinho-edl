import pygame
from imgs import imagen_P_Lado

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.finished = False

class GerenciadorPlayer:
    """Gerencia a criação e movimento do player"""
    
    def __init__(self, posicao_inicial, tamanho_celula, offset_x, offset_y):
        self.posicao_inicial = posicao_inicial
        self.tamanho_celula = tamanho_celula
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.player = None
        self._criar_player()
    
    def _criar_player(self):
        """Cria o player com a imagem redimensionada"""
        try:
            player_image = pygame.image.load('img/person/frame-1.png')
            player_image = self._redimensionar_imagem(player_image)
        except pygame.error:
            # Fallback: usar a imagem do sistema de imgs.py
            player_image = self._redimensionar_imagem(imagen_P_Lado)
        
        self.player = Player(
            self.offset_x + (self.posicao_inicial[0] * self.tamanho_celula),
            self.offset_y + (self.posicao_inicial[1] * self.tamanho_celula),
            player_image
        )
    
    def _redimensionar_imagem(self, imagem):
        """Redimensiona uma imagem para o tamanho da célula"""
        return pygame.transform.scale(imagem, (self.tamanho_celula, self.tamanho_celula))
    
    def atualizar_dimensoes(self, tamanho_celula, offset_x, offset_y):
        """Atualiza as dimensões quando a tela é redimensionada"""
        self.tamanho_celula = tamanho_celula
        self.offset_x = offset_x
        self.offset_y = offset_y
        self._criar_player()
    
    def mover_para_posicao(self, x, y):
        """Move o player para uma posição específica do labirinto"""
        if self.player:
            self.player.rect.x = self.offset_x + (x * self.tamanho_celula)
            self.player.rect.y = self.offset_y + (y * self.tamanho_celula)
    
    def desenhar(self, tela):
        """Desenha o player na tela"""
        if self.player:
            tela.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
    
    def resetar(self):
        """Reseta o estado do player"""
        if self.player:
            self.player.finished = False
            self.mover_para_posicao(self.posicao_inicial[0], self.posicao_inicial[1])
