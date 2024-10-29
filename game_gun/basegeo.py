import math


class Point:
    def __init__(self, x, y=None, polar=False):
        self.ftype = 'Point'
        if polar:
            self.x = x * math.cos(y)
            self.y = x * math.sin(y)   
        if y is None:
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"
    
    def __abs__(self):
        return self.dist()

    def __eq__(self, point):
        if point.ftype == "Point":
            if round(self.x, 5) == round(point.x, 5) and round(self.y, 5) == round(point.y, 5):
                return True
            else:
                return False            
        else:
            return False

    def dist(self, x=None, y=None):
        if x is None and y is None:
            x = 0
            y = 0
            return math.hypot(self.x - x, self.y - y) 
        elif x.ftype == "Point":
            y = x.y
            x = x.x           
            return math.hypot(self.x - x, self.y - y)   
        elif x.ftype == "Line":
            return x.dist(self)
        elif x.ftype == 'Circle':
            return self.dist(x.centre)-x.radius
        elif x.ftype == 'Triangle':
            return min(self.dist_to_segment(x.a, x.b), self.dist_to_segment(x.b, x.c), self.dist_to_segment(x.a, x.c))
            
    def dist_to_segment(self, start, finish):
        x1, y1 = self.x, self.y
        x2, y2 = start.x, start.y
        x3, y3 = finish.x, finish.y
        lig = False
        line = False
        seg = False
        v1 = Vector(x2, y2, x1, y1)
        v2 = Vector(x2, y2, x3, y3)
        if x1 == x2 and y1 == y2:
            lig = True
        else:
            if v1 ^ v2 == 0:
                line = True
                if v1 * v2 >= 1:
                    lig = True
                    if v1.dist() <= v2.dist():
                        seg = True
        p1 = Point(x1, y1)
        start = Point(x2, y2)
        end = Point(x3, y3)
        vs = Vector(start, p1)
        v2 = Vector(start, end)
        ve = Vector(end, p1)
        rev2 = Vector(end, start)
        if seg:
            return 0
        elif v2 * vs >= 0 and rev2 * ve >= 0 and not line:
            return abs((v2 ^ vs) / v2.dist())
        else:
            return min(abs(vs.dist()), abs(ve.dist()))   

    def __add__ (self, p):
            return Point(self.x+p.x, self.y + p.y)
    
    
    def turn(self, angle, point=False):
        if point:
            dox = self.x - point.x
            doy = self.y - point.y
            x = dox * math.cos(angle) - doy * math.sin(angle)
            y = dox * math.sin(angle) + doy * math.cos(angle)    
            x += point.x
            y += point.y
        else:
            x = self.x * math.cos(angle) - self.y * math.sin(angle)
            y = self.x * math.sin(angle) + self.y * math.cos(angle)      
        return Point(x, y)

    def on_segment(self, p1, p2):
        v1 = Vector(p1, self)
        v2 = Vector(p1, p2)
        if self == p1 or self == p2:
            return True
        else:
            if v1 ^ v2 == 0:
                if v1 * v2 >= 1:
                    if v1.dist() <= v2.dist():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
    
    
class Vector(Point):
    def __init__(self, x1, y1=None, x2=None, y2=None):
        self.ftype = 'Vector'
        if y2 is not None:
            self.x = x2 - x1
            self.y = y2 - y1
        elif type(y1) != int and type(y1) != float and y1 is not None:
            self.x = y1.x - x1.x
            self.y = y1.y - x1.y
        else:
            super().__init__(x1, y1)
        
    def dot_product(self, v):
        return self.x * v.x + self.y * v.y
    
    def __mul__(self, v):
        if type(v) != int and type(v) != float:
            return self.dot_product(v)
        else:
            return Vector(self.x * v, self.y * v)

    def cross_product(self, v):
        return self.x * v.y - v.x * self.y
    
    def __xor__(self, v):
        return self.cross_product(v)
    
    def __rmul__(self, v):
        return Vector(self.x * v, self.y * v)
    
  
class Line:
    def __init__(self, p0, p1, c=None):
        self.ftype = 'Line'
        if c is None:
            self.b = p0.x - p1.x
            self.a = p1.y - p0.y
            self.c = -self.a * p0.x - self.b * p0.y
            self.p0 = p0
            self.p1 = p1
        else:
            self.a = p0
            self.b = p1
            self.c = c
        if self.b != 0:
            self.normvec = Vector(self.a, (-self.a - self.c) / self.b, 2 * self.a, (-2 * self.a - self.c) / self.b)
        else:
            self.normvec = Vector(self.a, 0, 2 * self.a, 0)
        
    def __str__(self):
        return f"{self.a} {self.b} {self.c}"    
    
    def perpendecular(self, p):
        return Line(self.b, -self.a, -self.b * p.x + self.a * p.y)
    
    def contains(self, p):
        if p.x * self.a + p.y * self.b + self.c == 0:
            return True
        else:
            return False
        
    def position(self, p1, p2):
        if (self.a * p1.x + self.b * p1.y + self.c) * (self.a * p2.x + self.b * p2.y + self.c) > 0:
            return True
        else:
            return False
        
    def is_parallel(self, line):
        if line.b == 0 or line.a == 0:
            if line.b == 0 and line.a == 0:
                if self.a == 0 and self.b == 0:
                    return True
            elif line.b == 0:
                if self.b == 0:
                    return True
                else:
                    return False
            elif line.a == 0:
                if self.a == 0:
                    return True
                else:
                    return False            
            
        else:
            if self.a / line.a == self.b / line.b:
                return True
            else:
                return False
        
    def __eq__(self, line):
        if line.a == 0 or line.b == 0 or line.c == 0:
            if line.a == 0 or self.a == 0:
                if line.a == 0 and self.a == 0:
                    if line.b == 0 or self.b == 0 or line.c == 0:
                        if (line.b == 0 and self.b == 0) or (line.c == 0 and self.c == 0):
                            return True
                        else:
                            return True
                    elif self.b / line.b == self.c / line.c:
                        return True
                    else:
                        return False
                else:
                    return False
            elif line.b == 0 or self.b == 0:
                if line.b == 0 and self.b == 0:
                    if line.c == 0 or self.c == 0:
                        if line.c == 0 and self.c == 0:
                            return True
                        else:
                            return False
                    elif self.a / line.a == self.c / line.c:
                        return True
                    else:
                        return False
                else:
                    return False                
            elif line.c == 0 or self.c == 0:
                if self.a / line.a == self.b / line.b:
                    return True
                else:
                    return False                
        else:
            if self.a / line.a == self.b / line.b and self.c / line.c == self.a / line.a:
                return True
            else:
                return False       
            
    def dist(self, p):
        return abs((self.a * p.x + self.b * p.y + self.c) / (math.sqrt(self.a**2 + self.b**2)))

    def parallel(self, twisted):
        return Line(self.a, self.b, self.c + twisted * (math.sqrt(self.a**2 + self.b**2)))
    
    def foot_of_perp(self, p):
        if self.a == 0:
            return Point(p.x, -self.c / self.b)
        elif self.b == 0:
            return Point(-self.c / self.a, p.y)
        else:
            x = (self.b**2 * p.x - self.a * self.b * p.y - self.a * self.c) / (self.a**2 + self.b**2)
            y = (-self.a * x - self.c) / self.b
            return Point(x, y)
        
    def cross(self, line):
        if not self.is_parallel(line):
            x = (self.b * line.c - line.b * self.c) / (self.a * line.b - line.a * self.b)
            y = (line.a * self.c - self.a * line.c) / (self.a * line.b - line.a * self.b)            
            return Point(x, y)
        else:
            return False

    def turn(self, angle):
        return Line(Point(self.a, self.b).turn(angle).x, Point(self.a, self.b).turn(angle).y, self.c)   
    
    
class Circle:
    def __init__(self, x, y, r=None):
        self.ftype = 'Circle'
        if r is not None:
            self.centre = Point(x, y)
            self.radius = r
        else:
            self.centre = x
            self.radius = x.dist(y)

    def __str__(self):
        return f"{self.centre.x} {self.centre.y} {self.radius}" 

    def dist(self, line):
        if line.dist(self.centre) > self.radius:
            return line.dist(self.centre) - self.radius
        else:
            return 0

    def cross_line(self, line):
        if line.dist(self.centre) > self.radius:
            return 0, None
        elif line.dist(self.centre) == self.radius:
            return 1, [line.foot_of_perp(self.centre)]
        else:
            rst = (self.radius**2 - line.dist(self.centre)**2)**0.5
            norm = (line.a**2 + line.b**2)**0.5
            udx = line.a / norm
            udy = line.b / norm 
            perpx1 = -udy * rst
            perpy1 = udx * rst
            perpx2 = udy * rst
            perpy2 = -udx * rst            
            x1 = line.foot_of_perp(self.centre).x + perpx1
            y1 = line.foot_of_perp(self.centre).y + perpy1        
            x2 = line.foot_of_perp(self.centre).x + perpx2
            y2 = line.foot_of_perp(self.centre).y + perpy2               
            return 2, [Point(x1, y1), Point(x2, y2)]

    def viewing_angle(self, point):
        hypotenuse = point.dist(self.centre)
        cathet1 = self.radius
        cathet2 = (hypotenuse**2 - cathet1**2)**0.5
        cangle = (hypotenuse**2 + cathet2**2 - cathet1**2) / (2 * hypotenuse * cathet2)
        return 2 * abs(math.acos(cangle))

    def tangent(self, point):
        if point.dist(self.centre) < self.radius:
            return 0, []
        elif point.dist(self.centre) == self.radius:
            return 1, [point]
        else:
            pos1 = Line(Point(0, 0), Point(self.centre.x - point.x, self.centre.y - point.y)).turn(self.viewing_angle(point) / 2).foot_of_perp(Point(self.centre.x - point.x, self.centre.y - point.y))
            pos2 = Line(Point(0, 0), Point(self.centre.x - point.x, self.centre.y - point.y)).turn(2 * math.pi - (self.viewing_angle(point) / 2)).foot_of_perp(Point(self.centre.x - point.x, self.centre.y - point.y))
            return 2, [Point(pos1.x + point.x, pos1.y + point.y), Point(pos2.x + point.x, pos2.y + point.y)]

    def arc(self, p1, p2):
        v1 = Vector(p1.x - self.centre.x, p1.y - self.centre.y)
        v2 = Vector(p2.x - self.centre.x, p2.y - self.centre.y)
        x = v1 * v2
        y = v1 ^ v2
        alfa = abs(math.atan2(y, x))
        return alfa * self.radius

    def cross_circle(self, circle):
        if self.centre.dist(circle.centre) < abs(self.radius - circle.radius) or self.centre.dist(circle.centre) > abs(self.radius + circle.radius):
            return 0, None
        elif self.centre.dist(circle.centre) == abs(self.radius - circle.radius) or self.centre.dist(circle.centre) == abs(self.radius + circle.radius):
            if self.centre.dist(circle.centre) == 0:
                return 3, None
            else:
                q, a1 = self.cross_line(Line(self.centre, circle.centre))
                q, a2 = circle.cross_line(Line(self.centre, circle.centre))
                if a1[0] == a2[0] or a1[0] == a2[1]:
                    return 1, [a1[0]]
                else:
                    return 1, [a1[1]]
        else:
            q, a1 = self.cross_line(Line(self.centre, circle.centre))  
            if (a1[0].x - circle.centre.x) ** 2 + (a1[0].y - circle.centre.y) ** 2 <= circle.radius ** 2:
                p = a1[0]
            else:
                p = a1[1]
            a = self.centre.dist(circle.centre)
            b = self.radius
            c = circle.radius
            angle = math.acos((b ** 2 + a ** 2 - c ** 2) / (2 * a * b))
            neop1 = Point(p.x - self.centre.x, p.y - self.centre.y).turn(2 * math.pi - angle)
            neop2 = Point(p.x - self.centre.x, p.y - self.centre.y).turn(angle)
            return 2, [Point(neop1.x + self.centre.x, neop1.y + self.centre.y), Point(neop2.x + self.centre.x, neop2.y + self.centre.y)]


class Triangle:
    def __init__(self, p1, p2, p3):
        self.ftype = 'Triangle'
        self.a = p1
        self.b = p2
        self.c = p3

    def __str__(self):
        return f"{self.a}, {self.b}, {self.c}"

    def bisector(self, ang_nom):
        if ang_nom == 1:
            o = self.a
            a = self.b
            b = self.c
        if ang_nom == 2:
            o = self.b
            a = self.c
            b = self.a 
        if ang_nom == 3:
            o = self.c
            a = self.a
            b = self.b
        v1 = Vector(o, a)
        v2 = Vector(o, b)
        x = v1 * v2
        y = v1 ^ v2
        bisang = math.atan2(y, x) / 2
        bisp = a.turn(bisang, o)
        return Line(o, bisp)

    def center_of_gravity(self):
        return Point((self.a.x + self.b.x + self.c.x) / 3, (self.a.y + self.b.y + self.c.y) / 3)

    def incenter(self):
        return self.bisector(1).cross(self.bisector(3))

    def cross_height(self):
        return Line(Line(self.a, self.b).foot_of_perp(self.c), self.c).cross(Line(Line(self.c, self.b).foot_of_perp(self.a), self.a))

    def center_circumscribed_circle(self):
        p0 = Point(self.a.x - (self.a.x - self.b.x) / 2, self.a.y - (self.a.y - self.b.y) / 2)
        perp1 = Line(self.a, self.b).perpendecular(p0)
        p1 = Point(self.a.x - (self.a.x - self.c.x) / 2, self.a.y - (self.a.y - self.c.y) / 2)
        perp2 = Line(self.a, self.c).perpendecular(p1)        
        return perp1.cross(perp2)
    
    def inscribed_circle(self):
        return Circle(self.incenter().x, self.incenter().y, Line(self.a, self.b).dist(self.incenter()))

    def circumscribed_circle(self):
        return Circle(self.center_circumscribed_circle().x, self.center_circumscribed_circle().y, self.a.dist(self.center_circumscribed_circle()))

    def point_position(self, point):
        if point.on_segment(self.a, self.b) or point.on_segment(self.c, self.b) or point.on_segment(self.a, self.c):
            return True
        else:
            if Line(self.a, self.c).position(self.b, point) and Line(self.a, self.b).position(self.c, point) and Line(self.b, self.c).position(self.a, point):
                return True
            else:
                return False

    def minimal_circle(self):
        v1 = Vector(self.a, self.b)
        v2 = Vector(self.a, self.c)
        x = v1 * v2
        y = v1 ^ v2
        alfa = abs(math.atan2(y, x))
        v1 = Vector(self.b, self.a)
        v2 = Vector(self.b, self.c)
        x = v1 * v2
        y = v1 ^ v2
        beta = abs(math.atan2(y, x))
        v1 = Vector(self.c, self.b)
        v2 = Vector(self.c, self.a)
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
