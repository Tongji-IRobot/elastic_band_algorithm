__author__ = 'Administrator'
# -*- encoding=utf-8 -*-
import turtle
from basic_draw_class.basic_draw import *
import time
from basic_draw_class.a_turtle_machine import *
from math import sqrt
import random
P0 = 80
RADIUS = 20
Kr = 1
from main import *
import main


def test_draw():
    obstacle_list, path = init_obstacle_and_path()
    draw(obstacle_list[0].vertices, True)
    draw(path)


def test_calculate_f1():
    line = [Point(-50, -50), Point(-50, 0), Point(50, 40)]
    draw(line)

    f1 = calculate_f1(*line)
    draw([line[1], line[1] + f1*100])
    time.sleep(10)


def test_calculate_f2():
    obstacle_list, path = init_obstacle_and_path()
    f2_list = list()
    f2_list.append(Point(0, 0))

    for i in range(len(path)-2):
        f2_list.append(calculate_f2(path[i+1], obstacle_list))
    for ob in obstacle_list:
        draw(ob.vertices, True)
    draw(path)
    for i in range(len(path)-1):
        print path[i], f2_list[i]
        draw([path[i], path[i] + f2_list[i]*10])
    time.sleep(10)


def test_dynamic_demo():
    ob_list, path = init_obstacle_and_path(1)
    turtle.Turtle().getscreen().screensize(100, 2000)
    for ob in ob_list:
        draw(ob.vertices, True, draw_circle=True)
    robot = init_robot_pen(path[0])
    draw(path)
    dynamic_windows_follow(ob_list, path, robot, draw_frequence=1000)
    time.sleep(60)
