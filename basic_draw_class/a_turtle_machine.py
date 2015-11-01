__author__ = 'Administrator'
import turtle
import math
from math import *
class my_turtle(turtle.Turtle):
    def __init__(self, direct_list=[], length_list=[], name='zero'):
        turtle.Turtle.__init__(self)
        self.direct_list = direct_list
        self.length_list = length_list
        t_shape = self.create_shape(direct_list, length_list)
        self.getscreen().register_shape(name, t_shape)
        self.shape(name)

    def get_point_by_radar(self, id, obstacle_list):
        origin_direction = self.direct_list[id]
        length = self.length_list[id]
        now_direction = (origin_direction + self.heading()) % 360
        start_point = self.pos()

    @staticmethod
    def create_shape(direct_list=[], length_list=[]):
        a_turtle = turtle.Shape('compound')
        a_turtle.addcomponent(((0,16), (-2,14), (-1,10), (-4,7),
                                  (-7,9), (-9,8), (-6,5), (-7,1), (-5,-3), (-8,-6),
                                  (-6,-8), (-4,-5), (0,-7), (4,-5), (6,-8), (8,-6),
                                  (5,-3), (7,1), (6,5), (9,8), (7,9), (4,7), (1,10),
                                  (2,14)), 'black')

        radia_poly = map(lambda direct, length: (cos(direct/180.0*pi)*length, sin(direct/180.0*pi)*length), direct_list, length_list)
        radia_poly_list = [((0, 0), x) for x in radia_poly]
        for radia in radia_poly_list:
            a_turtle.addcomponent(radia,'red')
        return a_turtle

