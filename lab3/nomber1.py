import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


rect(screen, (130, 130, 130), (0, 0, 400, 400))

circle(screen, (255, 255, 0), (200, 200), 150)
circle(screen, (0, 0, 0), (200, 200), 150, 2)

rect(screen, (0, 0, 0), (110, 270, 170, 20))

polygon(screen, (0, 0, 0), [(2*30,3*30),
                                (2*30+8,3*30-8), (5*30,5*30), (5*30-8,5*30+8)])
polygon(screen, (0, 0, 0), [(400-2*30,3.5*30),
                                (400-2*30-8,3.5*30-8), (400-5*30,5*30), (400-5*30+8,5*30+8)])

circle(screen, (255, 0, 0), (110, 170), 30)
circle(screen, (0, 0, 0), (110, 170), 30, 2)
circle(screen, (0, 0, 0), (110, 170), 10)

circle(screen, (255, 0, 0), (400-110, 172), 30)
circle(screen, (0, 0, 0), (400-110, 172), 30, 2)
circle(screen, (0, 0, 0), (400-110, 172), 10)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()