import numpy as np
import time
import matplotlib.pyplot as plt
import random

class Snake:
    def __init__(self, coords, strategy=None):
        self.coords = coords
        self.strategy = strategy
        self.route = None
        self.alive = True

    def length(self):
        return len(self.coords)

    def die(self):
        self.alive = False
        print('snake die, length =', self.length())
        return self.length()

    def move(self, direction, rise=False):
        head_y, head_x = self.coords[0]
        if direction == 'top':
            head_y -= 1
        if direction == 'bottom':
            head_y += 1
        if direction == 'left':
            head_x -= 1
        if direction == 'right':
            head_x += 1

        if (head_y, head_x) in self.coords[1:]:
            print('self eat:', (head_y, head_x), self.coords[1:])
            self.die()

        if rise == True:
            self.coords = [(head_y, head_x)] + self.coords
        else:
            self.coords = [(head_y, head_x)] + self.coords[:-1]

    def set_route(self, field):

        pass

    def define_direction(self, head, step):
        step_y, step_x = step
        head_y, head_x = head
        if step_x == head_x + 1 and step_y == head_y:
            return 'right'
        elif step_x == head_x - 1 and step_y == head_y:
            return 'left'
        elif step_x == head_x and step_y == head_y - 1:
            return 'top'
        elif step_x == head_x and step_y == head_y + 1:
            return 'bottom'

    def make_step(self, field, route=False):
        head_y, head_x = self.coords[0]
        if route == True:
            self.set_route(field)
            step_y, step_x = self.route[0]
        else:
            #print(head_y, head_x)
            nearest_points = {(head_y+1, head_x), (head_y-1, head_x), (head_y, head_x+1), (head_y, head_x-1)}
            #print(nearest_points, end='  ---  ')
            nearest_points = nearest_points - field.walls - set(self.coords)
            #print(nearest_points)
            if len(nearest_points) == 0:
                self.die()
                return None
            else:
                random_step = random.choice(list(nearest_points))
                step_y, step_x = random_step

        if field.raw_matrix[step_y, step_x] == 4:
            rise = True
        else:
            rise = False
        self.move(self.define_direction(head=(head_y, head_x), step=(step_y, step_x)), rise=rise)


class Field:
    def __init__(self, size=None, walls=None, apples=None, apples_count=10, fp=None):
        self.size = size
        self.cells = None
        self.walls = walls
        self.raw_matrix = None
        if apples:
            self.apples = apples
        elif fp:
            self.read_from_file(fp)

    def read_from_file(self, fp):
        with open(fp) as f:
            rows = f.readlines()
            splited_rows = [list(r.strip()) for r in rows]
            matr = np.array(splited_rows).astype(int)
            self.raw_matrix = matr
            walls_array = np.argwhere(matr == 1)
            self.walls = set(tuple(wa) for wa in walls_array)
            apples_array = np.argwhere(matr == 4)
            self.apples = set(tuple(wa) for wa in apples_array)
            cells_array = np.argwhere(matr == 4)
            self.cells = set(tuple(wa) for wa in cells_array)


    def generate_apple(self, snakes):
        pass


class Playground:
    def __init__(self, size=None, snakes=None, fp=None):
        if fp:
            self.field = Field(fp=fp)
        if not snakes:
            walls = self.field.walls
            coords1 = [(4, 7), (5, 7), (6, 7), (6, 8), (6, 9)]
            coords2 = [(2, 5), (2, 4), (2, 3), (2, 1)]
            coords3 = [(2, 5)]
            self.snakes = [Snake(coords=coords3)]

        self.pg_fig = plt.figure()
        self.pg_ax = self.pg_fig.add_subplot()
        plt.ion()
        plt.show()

    def init_snakes(self, fp):
        pass

    def make_step(self):
        for snake in self.snakes:
            if snake.alive == True:
                snake.make_step(self.field)

    def count_alive_snakes(self):
        c = 0
        for snake in self.snakes:
            if snake.alive == True:
                c += 1
        return c

    def check_collisions(self):
        walls = self.field.walls
        for i, snake in enumerate(self.snakes):
            head = snake.coords[0]
            others_snakes = set()
            for enemy in self.snakes[:i]+self.snakes[i+1:]:
                others_snakes = others_snakes.union(set(enemy.coords))
            if head in walls.union(others_snakes):
                #print('collision', 'walls:', head in walls, 'snakes:', head in others_snakes)
                snake.die()
            if self.field.raw_matrix[head] == 4:
                self.field.raw_matrix[head] = 0

    def draw_pg(self, cool=False):
        pg_matrix = self.field.raw_matrix.copy()
        for snake in self.snakes:
            if snake.alive == True:
                for snake_piece in snake.coords:
                    pg_matrix[snake_piece] = 2

        #print(pg_matrix)
        self.pg_ax.matshow(pg_matrix)
        plt.draw()
        plt.pause(0.0000001)


    def run(self, delay=1, draw=False):
        self.draw_pg()
        i = 0
        while self.count_alive_snakes() > 0:
            print(i)
            self.make_step()
            self.check_collisions()
            time.sleep(delay)
            if draw == True:
                self.draw_pg()

        time.sleep(1)


if __name__ == '__main__':
    PG = Playground(fp='testmap.txt')
    PG.run(delay=0.000001, draw=True)































