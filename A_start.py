__author__ = 'dys'
import heapq
import main
import time
from basic_draw_class.basic_draw import *


class Grid(object):
    size = 25
    def __init__(self, obstacle_list):
        self.obstacle_grid = self.get_obstacle_point_by_obstacle_list(obstacle_list)
        pass

    def get_obstacle_point_by_obstacle_list(self, obstacle_list):
        size = self.size
        ans = list()
        for ob in obstacle_list:
            for segment in ob.sides:
                length = segment.length
                unit = segment.unit_length()
                for i in range(int(length/(size/1.5))+1):
                    ob_point = segment.start+unit*i*(size/1.5)
                    if isinstance(ob_point, Point):
                        center = Point(int((ob_point.x)/size), int((ob_point.y)/size))
                        ans += [center + Point(* tran) for tran in [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]]
        return ans


    def find_a_root(self, start, end):
        size = self.size
        global target_point
        target_point = end
        has_reach_p = set()
        heap = []
        heapq.heappush(heap, start)
        while heap:

            now_p = heapq.heappop(heap)
            has_reach_p.add(now_p)
            next_p_list = now_p.get_next_grid_point_list()
            if target_point in next_p_list:
                print 'got it'
                ans = [Point(target_point.x, target_point.y)]
                print ans
                while True:
                    ans.append(Point(now_p.x, now_p.y))
                    if now_p.father:
                        now_p = now_p.father
                        continue
                    else:
                        ans.reverse()
                        return [p*size for p in ans]
            else:
                for p in next_p_list:
                    if Point(p.x, p.y) not in self.obstacle_grid and p not in has_reach_p:
                        heapq.heappush(heap, p)
        else:
            print 'not find'


total_direct = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']

class Grid_point(Point):

    def __init__(self, x, y, direction, father=None):
        Point.__init__(self, x, y)
        self.direction = direction
        self.father = father
        self.index_direct = total_direct.index(self.direction)

    def __lt__(self, other):
        return self.distance(target_point) < other.distance(target_point)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def get_next_grid_point_list(self):
        index = total_direct.index(self.direction)
        index = [(index+i) % 8 for i in (-1, 0, 1)]
        direct_can_reach = [total_direct[i] for i in index]
        move = [self.get_one_move(d) for d in direct_can_reach]
        ans = [Grid_point(m.x+self.x, m.y+self.y, d, self) for (m, d) in zip(move, direct_can_reach)]
        return ans

    def get_one_move(self, direct):
        ans = Point(0, 0)
        if 'N' in direct:
            ans += Point(0, 1)
        if 'S' in direct:
            ans += Point(0, -1)
        if 'W' in direct:
            ans += Point(-1, 0)
        if 'E' in direct:
            ans += Point(1, 0)
        return ans


target_point = Grid_point(0, 0, 'N')


def final_main(ob_list, path, direction='N'):
    grid = Grid(ob_list)
    start = path[0]
    end = path[-1]
    size = Grid.size
    root = grid.find_a_root(Grid_point(int((start.x+size/4)/size), int((start.y+size/4)/size), direction),
                            Grid_point(int((end.x+size/4)/size), int((end.y+size/4)/size), direction))
    return root


def dynamic_windows_follow(ob_list, path, robot, draw_frequence=1, max_pen_list=1):
    draw_time = draw_frequence
    pen_list = []
    while len(path) >= 2:
        head = robot.heading()
        index = int(((head+22.5) % 360)/45)
        direction = total_direct[index]
        path = final_main(ob_list, path, direction)
        draw_time += 1
        if draw_time >= draw_frequence:
            pen = main.draw(path, draw_circle=True, point_color='blue')
            pen_list.append(pen)
            if len(pen_list) > max_pen_list:
                first_pen = pen_list.pop(0)
                first_pen.clear()
            draw_time -= draw_frequence
        start_point = path.pop(0)
        target_point = path[0]
        rhead = robot.heading()
        phead = Point(target_point.x - start_point.x, target_point.y - start_point.y).get_angle_from_zero_zero()
        angle = main.get_turn_left_angle(phead, rhead)
        max_turn_angle = 10
        if abs(abs(angle)-360) % 360 > 3 and abs(angle) > 3:
            if abs(angle) > max_turn_angle:
                robot.left(max_turn_angle * angle / abs(angle))
            else:
                robot.left(angle)
        robot.forward(3)
        start_point = robot.pos()
        start_point = Point(start_point[0], start_point[1])
        if start_point.distance(target_point) < 10:
            path.pop(0)
        path.insert(0, Circle(start_point, 0))
    print 'end'


def test_dynamic_mode():

    ob_list, path = main.init_obstacle_and_path(3)
    for ob in ob_list:
        main.draw(ob.vertices, True)
    size = Grid.size

    # grid = Grid(ob_list)
    # main.draw(list(grid.obstacle_grid),point_color='', basic_mul=size)

    robot = main.init_robot_pen(path[0], path[1])
    dynamic_windows_follow(ob_list, path, robot, draw_frequence=30)
    time.sleep(60)

if __name__ == '__main__':
    test_dynamic_mode()


