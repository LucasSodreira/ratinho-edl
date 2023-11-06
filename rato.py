import pygame

class Rato(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, largura, altura):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        # Atualize a imagem do sprite com base no índice do quadro atual
        self.image = self.frames[self.frame_index]
        
        # Atualize o índice do quadro para a próxima imagem
        self.frame_index = (self.frame_index + 1) % len(self.frames)
