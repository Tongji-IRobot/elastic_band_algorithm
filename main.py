# -*- encoding=utf-8 -*-
import turtle
from basic_draw_class.basic_draw import *
import time
from basic_draw_class.a_turtle_machine import *
from math import sqrt
import random
import matplotlib
import matplotlib.animation as animation
import os
os.popen()
P0 = 80
RADIUS = 20
Kr = 1

def init_obstacle_and_path(id=1):
    if id == 1:
        basic_mul = 2
        obstacle = Polygon(Point(-50, -50), Point(-50, 0), Point(0, 20), Point(30, 0), Point(30, -50))
        obstacle_list = list()
        obstacle_list.append(obstacle * basic_mul)
        obstacle = Polygon(*[Point(-50, -50), Point(-50, 0), Point(0, 20), Point(30, 0), Point(30, -50)])
        obstacle = obstacle.translate(100, 100)
        obstacle_list.append(obstacle * basic_mul)
        obstacle = obstacle.translate(-150, -240)
        obstacle_list.append(obstacle * basic_mul)
        path = [Point(0, -80), Point(-70, -60), Point(-80, 30), Point(40, 30), Point(40, 20), Point(70, 20)]
        path = [p * basic_mul for p in path]
    elif id == 2:
        basic_mul = 2
        obstacle = Polygon(Point(-100, 0), Point(0, 0), Point(-100, -100), Point(-200, -100))
        obstacle_list = list()
        obstacle_list.append(obstacle * basic_mul)
        obstacle = obstacle.translate(140, 0)
        obstacle_list.append(obstacle * basic_mul)
        path = [Point(-100, 10), Point(20, 10), Point(-80, -100)]
        path = [p * basic_mul for p in path]
    elif id == 3:
        turtle.Turtle().getscreen().screensize(100, 2000)
        basic_mul = 2
        size = 10
        obstacle =  Polygon(Point(-size, -size), Point(size, -size), Point(size, size), Point(-size, size))
        obstacle_list = list()
        for i in range(7):
            obstacle_list.append(obstacle.translate(random.randint(-60, 60), i*60+50) * basic_mul)
        path = [Point(0, 0), Point(0, 460)]
        path = [p * basic_mul for p in path]
    elif id == 4:
        turtle.Turtle().getscreen().screensize(100, 2000)
        basic_mul = 2
        size = 10
        obstacle = Polygon(Point(0, 50))
        obstacle_list = list()
        for i in range(6):
            obstacle_list.append(obstacle.translate(random.randint(-60, 60), i*60+50) * basic_mul)
        path = [Point(0, 0), Point(0, 460)]
        path = [p * basic_mul for p in path]
    return obstacle_list, path


def calculate_f2(point, obstacle_tuple):
    p = calculate_bubble_max_size_in_p(point, obstacle_tuple)
    if p >= P0:
        return Point(0, 0)
    else:
        h = p
        x = 0.2
        y = 0.2
        new_x = calculate_bubble_max_size_in_p(Point(point.x - h*x, point.y), obstacle_tuple) - \
                    calculate_bubble_max_size_in_p(Point(point.x + h*x, point.y), obstacle_tuple)
        new_y = calculate_bubble_max_size_in_p(Point(point.x, point.y - h*y), obstacle_tuple) - \
                    calculate_bubble_max_size_in_p(Point(point.x, point.y + h*y), obstacle_tuple)
        pian_dao = Point(new_x, new_y) / (2.0 * h)
        Fr = pian_dao * Kr * (p-P0)
        return Fr


def calculate_bubble_max_size_in_p(point, obstacle_tuple):
    t_dis_list = list([P0])
    for obstacle in obstacle_tuple:

        if isinstance(obstacle, Polygon):
            for side in obstacle.sides:
                t_dis = side.distance(point)
                t_dis_list.append(t_dis)
        elif isinstance(obstacle, Circle):
            t_dis_list.append(obstacle.p.distance(point) - obstacle.r, 0)
        elif isinstance(obstacle, Point):
            t_dis_list.append(obstacle.distance(point))
    return min(t_dis_list)


def unit_length(start, direction):
    return Point((direction.x-start.x), (direction.y-start.y))/start.distance(direction)


def calculate_f1(start_p, mid_p, end_p):
    u_line1 = unit_length(mid_p, start_p)
    u_line2 = unit_length(mid_p, end_p)
    return Point(u_line1.x+u_line2.x, u_line1.y+u_line2.y)


def draw(point_tuple, close=False, draw_circle=False, point_color='red', basic_mul=1, draw_speed=0):

    start = point_tuple[0]
    # Enlarged drawn images

    pen = turtle.Turtle()

    pen.hideturtle()
    pen.up()
    pen.setpos(start.x*basic_mul, start.y*basic_mul)
    pen.down()
    pen.speed(draw_speed)
    for p in point_tuple:

        pen.setpos(p.x*basic_mul, p.y*basic_mul)
        pen.dot(7, point_color)
        if draw_circle and isinstance(p, Circle):
            pen.speed(0)
            pen.up()
            pen.forward(p.r*basic_mul)
            pen.left(90)
            pen.down()
            for i in range(18):
                if i % 2 == 0:
                    pen.up()
                else:
                    pen.down()
                pen.circle(p.r*basic_mul, 20)
            pen.up()
            pen.setpos(p.x*basic_mul, p.y*basic_mul)
            pen.down()
    if close is True:
        pen.setpos(start.x*basic_mul, start.y*basic_mul)
    return pen


def divide_line_into_mul_circle(start, end, obstacle_list):
    # input two point and return a list of circle

    t_length = start.distance(end)
    direction = ((end - start) / end.distance(start))
    m = 0.0
    result_list = list()
    start_p = start
    while m < t_length:
        r = calculate_bubble_max_size_in_p(start_p, obstacle_list)
        result_list.append(Circle(start_p, r))
        m += r
        if r < 3:
            break
        start_p = start + direction * m
    r = calculate_bubble_max_size_in_p(end, obstacle_list)
    result_list.append(Circle(end, r))
    return result_list


def remove_too_close_point_in_path(path):
    i = 0
    while i < len(path) - 2:
        if path[i].distance(path[i+2]) < 0.8*(path[i].r+path[i+2].r):
            del path[i+1]
        else:
            i += 1
    return path


def add_point_to_path(path, obstacle_list):
    new_path = list()
    for i in range(len(path)-1):
        distance = path[i].distance(path[i+1])
        if distance < 0.95*(path[i].r+path[i+1].r):
            new_path.append(path[i])
            continue
        else:
            new_path.append(path[i])
            p = path[i].p + (path[i+1].p-path[i].p)*path[i].r/distance
            new_path.append(Circle(p, calculate_bubble_max_size_in_p(p, obstacle_list)))
    new_path.append(path[-1])
    return new_path


def flush_point_in_path(path, obstacle_list):
    new_path = list()
    for p in path:
        new_path.append(Circle(p, calculate_bubble_max_size_in_p(p, obstacle_list)))
    return new_path


def remove_duplicate_point_in_path(path):
    i = 0
    while i < len(path) - 1:
        if path[i] == path[i+1]:
            del path[i+1]
        else:
            i += 1
    return path


def opti_force(before_point, after_point, origin_force):
    dis = Point.distance(before_point, after_point)
    u = after_point-before_point
    dian_cheng = origin_force.dot(u)
    return (origin_force - origin_force * dian_cheng / dis / dis)


def cal_total_force_for_mid_point(before_point, after_point, mid_point, obstacle_list):
    f1 = calculate_f1(before_point, mid_point, after_point)
    f2 = calculate_f2(mid_point, obstacle_list)
    origin_f_total = f1*5+f2
    return opti_force(before_point, after_point, origin_f_total)


def final_main(obstacle_list, path, direction=None):
    new_path = list()
    for i in range(len(path)-1):
        new_path += divide_line_into_mul_circle(path[i], path[i+1], obstacle_list)
    new_path = remove_duplicate_point_in_path(new_path)
    new_path = remove_too_close_point_in_path(new_path)

    heat = 15.0
    min_distance = 4
    while min_distance > 3:
        min_distance = 0   # 用于终止计算线路迭代
        for i in range(len(new_path)-2):
            opti_f = cal_total_force_for_mid_point(new_path[i], new_path[i+2], new_path[i+1], obstacle_list)
            new_path[i+1] = Circle(new_path[i+1] + opti_f*heat/10.0, 0)
            min_distance = max(opti_f, min_distance)
            # 优化力的计算
        heat = heat / 1.5

        new_path = flush_point_in_path(new_path, obstacle_list)
        new_path = remove_duplicate_point_in_path(new_path)
        new_path = remove_too_close_point_in_path(new_path)
        new_path = add_point_to_path(new_path, obstacle_list)

        print heat
        if heat < 3:
            break
    return new_path


def init_robot_pen(init_point, next_point):
    robot = turtle.Turtle()
    robot.speed(1)
    robot = turtle.Turtle()
    robot.up()
    robot.setpos(init_point.x, init_point.y)
    robot.setheading(robot.towards(next_point.x, next_point.y))
    robot.shape('turtle')
    robot.down()
    robot.color('blue')
    return robot

def move_follow_path(path, robot, limit_step=10000000):
    path.pop(0)
    while path:
        target_point = path.pop(0)
        last_distance = 100000
        while True:#Point(robot.pos()[0], robot.pos()[1]).distance(target_point) < last_distance:
            last_distance = Point(robot.pos()[0], robot.pos()[1]).distance(target_point)
            rhead = robot.heading()
            phead = Point(target_point.x - robot.pos()[0], target_point.y - robot.pos()[1]).get_angle_from_zero_zero()
            angle = get_turn_left_angle(phead, rhead)

            max_turn_angle = 5
            if abs(abs(angle)-360) % 360 > 3 and abs(angle) > 3:
                if abs(angle) > max_turn_angle:
                    robot.left(max_turn_angle * angle / abs(angle))
                else:
                    robot.left(angle)
            robot.forward(5)
            if limit_step < 0:
                return
            else:
                limit_step -= 1
            if Point(robot.pos()[0], robot.pos()[1]).distance(target_point) < 5:
                break


def dynamic_windows_follow(ob_list, path, robot, draw_frequence=1, max_pen_list=3, path_methond=[final_main], max_step=-1, method_frequence=1):
    draw_time = draw_frequence
    pen_list = []
    m_fre = method_frequence
    while len(path) >= 2:
        m_fre+=1
        if m_fre >= method_frequence:
            m_fre=0

            head = robot.heading()
            index = int(((head+22.5) % 360)/45)
            direction = A_start.total_direct[index]
            for method in path_methond:
                path = method(ob_list, path, direction)

            draw_time += 1
            if draw_time >= draw_frequence:
                pen = draw(path, draw_circle=False, point_color='blue')
                pen_list.append(pen)
                if len(pen_list) > max_pen_list:
                    first_pen = pen_list.pop(0)
                    first_pen.clear()
                draw_time =0

        start_point = path.pop(0)
        target_point = path[0]
        rhead = robot.heading()
        phead = Point(target_point.x - start_point.x, target_point.y - start_point.y).get_angle_from_zero_zero()
        angle = get_turn_left_angle(phead, rhead)
        max_turn_angle = 7
        if abs(abs(angle)-360) % 360 > 3 and abs(angle) > 3:
            if abs(angle) > max_turn_angle:
                robot.left(max_turn_angle * angle / abs(angle))
            else:
                robot.left(angle)
        robot.forward(5)
        start_point = robot.pos()
        start_point = Point(start_point[0], start_point[1])
        if start_point.distance(target_point) < 20:
            path.pop(0)
            print 'pop one point'
        path.insert(0, Circle(start_point, 0))
        if max_step == -1:
            pass
        elif max_step == 0:
            return robot
        else:
            max_step -= 1
    print 'end'
    return robot


def get_turn_left_angle(target_head, now_head):

    if target_head < 180:
        if now_head < target_head:
            return target_head - now_head
        elif now_head > target_head + 180:
            return target_head - now_head + 360
        else:
            return target_head - now_head
    else:
        if target_head-180 < now_head < target_head:
            return target_head - now_head
        elif target_head < now_head:
            return target_head - now_head
        else:
            return target_head - now_head - 360


def show_demo(d=(0, 1)): # 15年9月demo
    '''test_draw()
    turtle.Screen().bye()
    test_calculate_f1()
    turtle.Screen().bye()
    test_calculate_f2()
    turtle.Screen().bye()'''
    ob_list, path = init_obstacle_and_path(1)
    for ob in ob_list:
        draw(ob.vertices, True)
    path = final_main(ob_list, path)
    draw(path)
    robot = init_robot_pen(path[d[0]], path[d[1]])
    move_follow_path(path, robot, limit_step=200)



def test_my_turtle():
    z = my_turtle([90, 120, 60], [100]*3)
    z.forward(100)
    time.sleep(10)


from test_python import *
import A_start

def final_main_combine_A_start(ob_id=4,d=(0,1)):
    ob_list, path = init_obstacle_and_path(ob_id)
    for ob in ob_list:
        draw(ob.vertices, True)
    robot = init_robot_pen(path[d[0]], path[d[1]])

    dynamic_windows_follow(ob_list, path, robot, path_methond=[A_start.final_main,], draw_frequence=1, max_pen_list=1,method_frequence=10)
    time.sleep(5)

if __name__ == '__main__':
    final_main_combine_A_start()



