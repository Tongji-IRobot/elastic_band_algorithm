# -*- encoding=utf-8 -*-
import turtle
import math


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __mul__(self, other):
        return Point(self.x*other, self.y*other)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __div__(self, other):
        return Point(self.x*1.0/other, self.y*1.0/other)

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y-other.y)**2)

    def __str__(self):
        return (self.x, self.y)

    def dot(self, other):
        return self.x*other.x+self.y*other.y

    def get_angle_from_zero_zero(self):
        # 从原点到改点的向量的角度   0~360
        result = round(math.atan2(self.y, self.x)*180.0/math.pi, 10) % 360.0
        return result

    def __str__(self):
        return str((self.x, self.y))

    def __eq__(self, other):
        if abs(self.x - other.x) < 10**-6 and abs(self.y - other.y) < 10**-6:
            return True
        else:
            return False


class Segment(object):
    def __init__(self, p1, p2):
        self.start = p1
        self.end = p2
        self.length = self.start.distance(self.end)

    def __str__(self):
        return 'start ', self.start,' end ',self.end

    def unit_length(self):
        start = self.start
        direction = self.end
        if start == direction:
            return Point(0, 0)
        else:
            return Point((direction.x-start.x), (direction.y-start.y))/start.distance(direction)

    def distance(self, point):
        if isinstance(point, Point):
            if self.end == self.start:
                return self.end.distance(point)
            seg_vector = self.end - self.start
            pt_vector = point - self.start
            t = seg_vector.dot(pt_vector)/self.length**2
            if t >= 1:
                distance = Point.distance(self.end, point)
            elif t <= 0:
                distance = Point.distance(self.start, point)
            else:
                distance = Point.distance(
                    self.start + Point(t*seg_vector.x, t*seg_vector.y), point)
            return distance


class Circle(Point):
    def __init__(self, point, r):
        super(Circle, self).__init__(point.x, point.y)
        if isinstance(point, Point):
            self.p = point
        elif isinstance(point, Circle):
            self.p = point.p
        self.r = r

    def __eq__(self, other):
        if isinstance(other, Circle):
            if abs(self.r - other.r) < 10**-6 and self.p == other.p:
                return True
            else:
                return False
        elif isinstance(other, Point):
            if self.p.x == other.x and self.p.y == other.y:
                return True
            else:
                return False

    def contain(self, point):
        if self.p.distance(point) <= self.r:
            return True
        else:
            return False

    def inter(self, other):
        if self.p.distance(other.p) < (self.r+other.r):
            return True
        else:
            return False

    def translate(self, x, y):
        tran = Point(x, y)
        return Circle(self.p + tran, self.r)

class Polygon(object):

    def __init__(self, *argv):
        self.vertices = list(argv)
        self.sides = self.sides()

    def __str__(self):
        return self.vertices

    def __mul__(self, other):
        return Polygon(*[point * other for point in self.vertices])

    def translate(self, x, y):
        tran = Point(x, y)
        return Polygon(*[point + tran for point in self.vertices])

    def sides(self):
        res = []
        args = self.vertices
        for i in xrange(-len(args), 0):
            res.append(Segment(args[i], args[i + 1]))
        return res

