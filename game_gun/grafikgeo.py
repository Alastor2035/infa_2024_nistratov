import basegeo as bg
import pygame
import math
import random
from colors import *

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

    def update(self, width, height):
        for i in self.figures:
            i.update(width, height)


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

class balls_list(figures_list):

    def catch(self, x, y):
        su = 0 
        for i in self.figures:
            if i.catch(x, y, 0):
                self.delet(i)
                su += i.cost
        return su
    
    def generate(self,WIDTH, HEIGHT):
        a = random.randint(1, 8)
        for i in range(a):
            x = random.randint(50, WIDTH-50)
            y = random.randint(50, HEIGHT-50)
            vx = random.randint(-5, 5)
            vy = random.randint(-5, 5)
            color = COLORS_LIST[random.randint(1, len(COLORS_LIST)-1)]
            scale = random.randint(1, 7)
            ball = Ball(x, y, scale, color, vx, vy)
            self.add(ball)  

    def update(self, width, height):
        sc = 0
        for i in self.figures:
            for j in self.figures:
                if i.collapses < 1 and j.collapses < 1:
                    if i.centre.dist(j.centre) <= i.radius + j.radius and i.centre.dist(j.centre)>0:
                        i.collapse(j)
        for i in self.figures:
            if i.ftype == 'Ball':
                i.update(width, height)
            else:
                sc += i.update(width, height, self)
        for i in self.figures:
            i.collapses = 0
        return sc


class Ball(Circle):

    def __init__(self, x, y, scale, color, vx, vy):
        self.radius = 7 * scale
        self.cost = 10 // scale
        self.collapses = 0
        self.color = color
        self.vx = vx
        self.scale = scale
        self.vy = vy
        super().__init__(x, y, self.radius)
        self.ftype = 'Ball'

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.centre.x, self.centre.y), self.radius)

    def update(self, width, height):
        if self.centre.x - self.radius <= 0: 
            self.vx = - self.vx 
            self.x = self.radius * 1.3
        if self.centre.x + self.radius >=  width: 
            self.vx = - self.vx 
            self.x = width - self.radius * 1.3
        if self.centre.y - self.radius <= 0: 
            self.vy = - self.vy
            self.y = self.radius * 1.3
        if self.centre.y + self.radius >=  height:
            self.vy = - self.vy 
            self.y = height - self.radius * 1.3
        self.centre.x += self.vx 
        self.centre.y += self.vy


    def catch(self, x, y, r):
        return self.radius + r >= self.centre.dist(bg.Point(x, y))
    
    def collapse(self, ball, fo = 0, ctype = 0):
        self.collapses = +1
        if ctype == 0:
            sspe = bg.Vector(self.vx, self.vy)
            ospe = bg.Vector(ball.vx, ball.vy)
            d = bg.Vector(self.centre, ball.centre)
            putv = (d * sspe) * ((1/d.dist())**2) * d
            getv = (d * ospe) * ((1/d.dist())**2) * d
            ball.collapse(self, putv, 1)
        else:
            sspe = bg.Vector(self.vx, self.vy)
            d = bg.Vector(self.centre, ball.centre)
            putv = (d * sspe) * ((1/d.dist())**2) * d
            getv = fo
        self.vx -= (putv.x * self.scale - getv.x * ball.scale) / self.scale
        self.vy -= (putv.y * self.scale - getv.y * ball.scale) / self.scale



    
class Ball_hunter(Ball):

    def __init__(self, x, y, scale, color, vx, vy):
        self.angle = 0
        super().__init__(x, y, scale, color, vx, vy)
        self.ftype = 'Ball_hunter'
        self.cost = -(scale + abs(vx) + abs(vy))//2


    def update(self, width, height, Balls_list):
        if self.centre.x - self.radius <= 0: 
            Balls_list.delet(self)
            return 0
        if self.centre.x + self.radius >=  width: 
            Balls_list.delet(self)
            return 0
        if self.centre.y - self.radius <= 0: 
            Balls_list.delet(self)
            return 0
        if self.centre.y + self.radius >=  height:
            Balls_list.delet(self)
            return 0
        super().update(width, height)
        self.angle += 5
        for i in Balls_list.figures:
            if i.ftype == 'Ball':
                if i.catch(self.centre.x, self.centre.y, self.radius):
                    Balls_list.delet(i)
                    return i.cost
        return 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.centre.x, self.centre.y), self.radius - 5*self.radius/7)
        for i in range(15):
            angle = math.radians(i * 360 / 15) + self.angle
            start_x = self.centre.x + int((self.radius - 5*self.radius/7) * math.cos(angle))
            start_y = self.centre.y + int((self.radius - 5*self.radius/7) * math.sin(angle))
            end_x = self.centre.x + int((self.radius ) * math.cos(angle))
            end_y = self.centre.y + int((self.radius ) * math.sin(angle))
            pygame.draw.line(screen, self.color, (start_x, start_y), (end_x, end_y), 2)

class Gun:
     
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def shot(self, x, y, tp):
        np = bg.Vector(self.x, self.y, x, y)
        if tp == 0:
            return Ball_hunter(self.x, self.y, 5, WHITE, np.x / np.dist() * 5, np.y / np.dist() * 5)
        return Ball_hunter(self.x, self.y, 2, RED, np.x / np.dist() * 20, np.y / np.dist() * 20)
    
    def draw(self, screen, x, y):
        pygame.draw.circle(screen, RED, (self.x, self.y), 10)
