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
pygame.display.set_caption("tank game")
clock = pygame.time.Clock()

balls_list = gg.balls_list()
tank = gg.Tank(200, 600)
f = open("game_gun/score.txt",'r')
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
            if e.key == pygame.K_a:
                tank.move(x = -5)
            if e.key == pygame.K_d:
                tank.move(x = 5)
            if e.key == pygame.K_s:
                tank.move(y = 5)
            if e.key == pygame.K_w:
                tank.move(y = -5)
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if e.button == 1:
                Bh = tank.shot(x, y, 0)
            if e.button == 3:
                Bh = tank.shot(x, y, 1)
            balls_list.add(Bh)
                 
    screen.fill((0, 0, 0))
    score += balls_list.update(WIDTH, HEIGHT)
    balls_list.draw(screen)
    x, y = pygame.mouse.get_pos()
    tank.draw(screen, x, y)
    drawText(screen, WHITE, "Счёт:" + str(score), pygame.Rect(500, 10, 300, 30), font_size=50)
    drawText(screen, WHITE, "Топ:", pygame.Rect(700, 10, 300, 30), font_size=50)
    for i in range(min(5, len(sclist))):
        drawText(screen, WHITE, sclist[i][1] + ": " + str(sclist[i][0]), pygame.Rect(700, 50+35*i, 300, 30), font_size=30)


    pygame.display.flip()
    clock.tick(FPS)
f = open("game_gun/score.txt",'r')
e = []
for i in f.readlines():
    e.append(list(i.split(': '))[::-1])
    e[-1][0] = int(e[-1][0][:-1])
f.close()
e.append([score, name])
e.sort(reverse=True)
f = open("game_gun/score.txt",'w')
for i in range(min(5, len(e))):
    f.write(e[i][1] + ": " + str(e[i][0]) + '\n')
f.close()