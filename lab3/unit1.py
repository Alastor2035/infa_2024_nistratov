import pygame
from pygame.draw import *
pygame.init()
screen = pygame.display.set_mode((300, 200))







pygame.display.update()
clock = pygame.time.Clock()
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()