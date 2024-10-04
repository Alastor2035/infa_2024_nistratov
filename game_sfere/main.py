import pygame
import random
import basegeo as bg
import grafikgeo as gg
import auxiliar as aux
from draw import *
from colors import *


print("Your name:")
name = input()

FPS = 60
WIDTH = 1000
HEIGHT = 800
score = 0
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the boll")
clock = pygame.time.Clock()

balls_list = gg.balls_list()


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                a = random.randint(1, 8)
                for i in range(a):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    vx = random.randint(-5, 5)
                    vy = random.randint(-5, 5)
                    color = COLORS_LIST[random.randint(1, len(COLORS_LIST)-1)]
                    scale = random.randint(1, 7)
                    ball = gg.Ball(x, y, scale, color, vx, vy)
                    balls_list.add(ball)   
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = pygame.mouse.get_pos()
                score += balls_list.catch(x, y)

                 
    screen.fill((0, 0, 0))
    drawText(screen, WHITE, "Счёт:" + str(score), pygame.Rect(500, 10, 300, 30), font_size=50)
    balls_list.update(WIDTH, HEIGHT)
    balls_list.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
f = open("game_sfere/score.txt",'r')
e = []
for i in f.readlines():
    e.append(i)
f.close()

f = open("game_sfere/score.txt",'w')
for i in e:
    f.write(i)
f.write(name + ": " + str(score) + '\n')
f.close()