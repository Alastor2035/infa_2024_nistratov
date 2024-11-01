import pygame
from draw import *
from colors import *

class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, h, w, img=None):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)   
        
    def update(self):
        self.image.fill((CYAN))
        drawText(self.image, WHITE, f"{self.text}", pygame.Rect(0, 0, self.rect.width, self.rect.height), font_size=20)
        self.rect.center = (self.x, self.y) 
        