import basegeo as bg
import pygame
import math

class Point(bg.Point):

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 6)

    def draw_shift(self, screen):
        pygame.draw.circle(screen, (255, 0, 255), (self.x, self.y), 10)
        
class Circle(bg.Circle):

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.centre.x, self.centre.y), self.radius, 5)

    def draw_shift(self, screen):
        pygame.draw.circle(screen, (255, 0, 255), (self.centre.x, self.centre.y), self.radius, 10)
    

class Line(bg.Line):

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 0), (-1, (self.a - self.c)/self.b), (1001, (-1001*self.a - self.c)/self.b), 3)

    def draw_shift(self, screen):
        pygame.draw.line(screen, (255, 0, 255), (-1, (self.a - self.c)/self.b), (1001, (-1001*self.a - self.c)/self.b), 5)

class Triangle(bg.Triangle):

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 0), (self.a.x, self.a.y), (self.b.x, self.b.y), 3)
        pygame.draw.line(screen, (255, 255, 0), (self.a.x, self.a.y), (self.c.x, self.c.y), 3)
        pygame.draw.line(screen, (255, 255, 0), (self.c.x, self.c.y), (self.b.x, self.b.y), 3)

    def draw_shift(self, screen):
        pygame.draw.line(screen, (255, 0, 255), (self.a.x, self.a.y), (self.b.x, self.b.y), 5)
        pygame.draw.line(screen, (255, 0, 255), (self.a.x, self.a.y), (self.c.x, self.c.y), 5)
        pygame.draw.line(screen, (255, 0, 255), (self.c.x, self.c.y), (self.b.x, self.b.y), 5)
        
    def inscribed_circle(self):
        return Circle(self.incenter().x, self.incenter().y, Line(self.a, self.b).dist(self.incenter()))

    def circumscribed_circle(self):
        return Circle(self.center_circumscribed_circle().x, self.center_circumscribed_circle().y, self.a.dist(self.center_circumscribed_circle()))

    def minimal_circle(self):
        v1 = bg.Vector(self.a, self.b)
        v2 = bg.Vector(self.a, self.c)
        x = v1 * v2
        y = v1 ^ v2
        alfa = abs(math.atan2(y, x))
        v1 = bg.Vector(self.b, self.a)
        v2 = bg.Vector(self.b, self.c)
        x = v1 * v2
        y = v1 ^ v2
        beta = abs(math.atan2(y, x))
        v1 = bg.Vector(self.c, self.b)
        v2 = bg.Vector(self.c, self.a)
        x = v1 * v2
        y = v1 ^ v2
        gamma = abs(math.atan2(y, x))
        if alfa < math.pi / 2 and beta < math.pi / 2 and gamma < math.pi / 2:
            return self.circumscribed_circle()
        else:
            if alfa >= math.pi / 2:
                x = self.b.x - (self.b.x - self.c.x) / 2
                y = self.b.y - (self.b.y - self.c.y) / 2
                radi = self.b.dist(self.c) / 2
            if beta >= math.pi / 2:
                x = self.a.x - (self.a.x - self.c.x) / 2
                y = self.a.y - (self.a.y - self.c.y) / 2
                radi = self.a.dist(self.c) / 2     
            if gamma >= math.pi / 2:
                x = self.b.x - (self.b.x - self.a.x) / 2
                y = self.b.y - (self.b.y - self.a.y) / 2
                radi = self.b.dist(self.a) / 2     
            return Circle(x, y, radi)    


class figures_list:

    def __init__(self):
        self.figures = []

    def add(self, other):
        self.figures.append(other)
        
    def delet(self, other):
        self.figures.pop(self.figures.index(other))

    def draw(self, screen):
        for i in self.figures:
            i.draw(screen)

    def update(self):
        for i in self.figures:
            i.update()


class figures_shift_list(figures_list):

    def draw(self, screen):
        for i in self.figures:
            i.draw_shift(screen)

    def release(self, new_home, typef, typec):
        if len(self.figures) == 1:
            if typec == 0:
                new_home.add(self.figures[0].inscribed_circle())
            if typec == 1:
                new_home.add(self.figures[0].circumscribed_circle()) 
            if typec == 2:
                new_home.add(self.figures[0].minimal_circle())            
        if len(self.figures) == 2:
            if self.figures[0].ftype == 'Point' and self.figures[1].ftype == "Point":
                if typef == 0:
                    new_home.add(Circle(self.figures[0], self.figures[1]))
                if typef == 1:
                    new_home.add(Line(self.figures[0], self.figures[1]))
            elif self.figures[0].ftype == 'Circle' and self.figures[1].ftype == "Circle":
                q, a = self.figures[0].cross_circle(self.figures[1])
                for i in range(q):
                    new_home.add(Point(a[i].x, a[i].y))
        if len(self.figures) == 3:
            new_home.add(Triangle(self.figures[0], self.figures[1], self.figures[2]))
        self.figures = []