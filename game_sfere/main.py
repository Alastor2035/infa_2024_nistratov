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

f = open("game_sfere/score.txt",'r')
sclist = []
for i in f.readlines():
    sclist.append(list(i.split(': '))[::-1])
    sclist[-1][0] = int(sclist[-1][0][:-1])
f.close()
sclist.sort(reverse=True)


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                balls_list.generate(WIDTH, HEIGHT) 
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = pygame.mouse.get_pos()
                score += balls_list.catch(x, y)

                 
    screen.fill((0, 0, 0))
    balls_list.update(WIDTH, HEIGHT)
    balls_list.draw(screen)
    drawText(screen, WHITE, "Счёт:" + str(score), pygame.Rect(500, 10, 300, 30), font_size=50)
    drawText(screen, WHITE, "Топ:", pygame.Rect(700, 10, 300, 30), font_size=50)
    for i in range(min(5, len(sclist))):
        drawText(screen, WHITE, sclist[i][1] + ": " + str(sclist[i][0]), pygame.Rect(700, 50+35*i, 300, 30), font_size=30)


    pygame.display.flip()
    clock.tick(FPS)
f = open("game_sfere/score.txt",'r')
e = []
for i in f.readlines():
    e.append(list(i.split(': '))[::-1])
    e[-1][0] = int(e[-1][0][:-1])
f.close()
e.append([score, name])
e.sort(reverse=True)
f = open("game_sfere/score.txt",'w')
for i in range(min(5, len(e))):
    f.write(e[i][1] + ": " + str(e[i][0]) + '\n')
f.close()