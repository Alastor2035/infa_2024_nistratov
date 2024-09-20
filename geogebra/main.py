import pygame
import basegeo as bg
import grafikgeo as gg
import auxiliar as aux
from draw import *
from colors import *


FPS = 60
WIDTH = 1000
HEIGHT = 800
typef = 0
typec = 0
inf = 0
point_mod = 0
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geogebra")
clock = pygame.time.Clock()

figures_g = gg.figures_list()
figures_shift_g = gg.figures_shift_list()
reseter = []



running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                point_mod = (point_mod+1)%2
            if e.key == pygame.K_q:
                typef = (typef+1)%2
            if e.key == pygame.K_c:
                typec = (typec+1)%3     
            if e.key == pygame.K_i:
                inf = (inf+1)%2  
            if e.key == pygame.K_z:
                figures_g.figures = reseter[-2]
                reseter.pop()
            if e.key == pygame.K_DELETE:
                for i in figures_shift_g.figures:
                    figures_g.delet(i)
                reseter.append([])
                for i in figures_g.figures:
                    reseter[-1].append(i)
                figures_shift_g.figures = []
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = pygame.mouse.get_pos()
                point = gg.Point(x, y)
                figures_g.add(point)
                reseter.append([])
                for i in figures_g.figures:
                    reseter[-1].append(i)
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 3:
                x, y = pygame.mouse.get_pos()
                point = gg.Point(x, y)
                dists = []
                dists_shifts = []
                nom = 0
                for i in figures_g.figures:
                    if point_mod == 0 and i.ftype == "Point":
                        dists.append([point.dist(i), nom])
                    if point_mod == 1 and i.ftype != "Point":
                        dists.append([point.dist(i), nom])  
                    nom += 1
                nom = 0
                for i in figures_shift_g.figures:
                    if point_mod == 0 and i.ftype == "Point":
                        dists_shifts.append([point.dist(i), nom])
                    if point_mod == 1 and i.ftype != "Point":
                        dists_shifts.append([point.dist(i), nom])   
                    nom += 1
                if len(dists_shifts) != 0 and len(dists) != 0:
                    dists.sort(key=lambda x: x[0])
                    dists_shifts.sort(key=lambda x: x[0])
                    if dists[0][0] < dists_shifts[0][0]:
                        figures_shift_g.add(figures_g.figures[dists[0][1]])
                    else:
                        figures_shift_g.delet(figures_shift_g.figures[dists_shifts[0][1]])
                elif len(dists_shifts) == 0:
                    dists.sort(key=lambda x: x[0])
                    figures_shift_g.add(figures_g.figures[dists[0][1]])
                else:
                    dists_shifts.sort(key=lambda x: x[0])
                    figures_shift_g.delet(figures_g.figures[dists[0][1]])
            elif e.button == 2:
                figures_shift_g.release(figures_g, typef, typec)
                reseter.append([])
                for i in figures_g.figures:
                    reseter[-1].append(i)                
    screen.fill((0, 0, 0))
    figures_g.draw(screen)
    if inf == 0:
        drawText(screen, WHITE, "i - скрыть/показать справку", pygame.Rect(100, 10, 300, 30), font_size=16)
        drawText(screen, WHITE, "ЛКМ - поставить точку", pygame.Rect(100, 20, 300, 40), font_size=16)
        drawText(screen, WHITE, "ПКМ - выделить ближайшее", pygame.Rect(100, 40, 300, 60), font_size=16)
        drawText(screen, WHITE, "колёсико - реализовать построение", pygame.Rect(100, 60, 300, 80), font_size=16)
        drawText(screen, WHITE, "пробел - настройка выделения(point_mode/figure_mode)", pygame.Rect(100, 80, 300, 100), font_size=16)
        drawText(screen, WHITE, "c - настройка окружности для треугольника", pygame.Rect(100, 100, 300, 120), font_size=16)
        drawText(screen, WHITE, "q - настройка рисования линия/круг(line_mode/circle_mode)", pygame.Rect(100, 120, 300, 120), font_size=16)
        drawText(screen, WHITE, "Программа строит прямые, окружности, триугольники, ", pygame.Rect(100, 140, 300, 120), font_size=16)
        drawText(screen, WHITE, "пересечения окружностей, описанную, вписанную и минимальную окружность", pygame.Rect(100, 160, 300, 120), font_size=16)
    if point_mod == 0:
        drawText(screen, MAGENTA, "point mode", pygame.Rect(850, 0, 100, 100), font_size=25)
    else:
        drawText(screen, MAGENTA, "figure mode", pygame.Rect(850, 0, 100, 100), font_size=25)
    if typef == 0:
        drawText(screen, MAGENTA, "circle mode", pygame.Rect(850, 50, 100, 100), font_size=25)
    else:
        drawText(screen, MAGENTA, "line mode", pygame.Rect(850, 50, 100, 100), font_size=25)
    if typec == 0:
        drawText(screen, MAGENTA, "вписанная", pygame.Rect(850, 100, 100, 100), font_size=25)
    elif typec == 1:
        drawText(screen, MAGENTA, "описанная", pygame.Rect(850, 100, 100, 100), font_size=25)    
    else:
        drawText(screen, MAGENTA, "минимальная", pygame.Rect(850, 100, 100, 100), font_size=25)    
    figures_shift_g.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)