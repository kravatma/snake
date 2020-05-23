import numpy as np
import itertools

class Snake:
    def __init__(self, coords, length=2, strategy=None):
        self.length = length
        self.coords = coords
        self.strategy = strategy
        self.route = None
        self.alive = True

    def die(self):
        self.alive = False

    def move(self, direction):
        head_x, head_y = self.coords[0]
        if direction == 'top':
            head_y += 1
        if direction == 'bottom':
            head_y -= 1
        if direction == 'left':
            head_x -= 1
        if direction == 'right':
            head_x += 1
        self.coords = [(head_x, head_y)] + self.coords[:-1]

    def rise(self):
        self.length += 1

    def set_route(self, field):

        pass

    def make_step(self):
        step_x, step_y = self.route[0]
        head_x, head_y = self.coords[0]
        if step_x == head_x + 1 and step_y == head_y:
            self.move('right')
        elif step_x == head_x - 1 and step_y == head_y:
            self.move('left')
        elif step_x == head_x and step_y == head_y + 1:
            self.move('top')
        elif step_x == head_x and step_y == head_y - 1:
            self.move('bottom')
        else:
            self.die()


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
            coords = [(7, 7), (8, 7)]
            self.snakes = [Snake(coords=coords)]

    def init_snakes(self, fp):
        pass

    def make_step(self):
        for snake in self.snakes:
            snake.set_route(self.field)
            snake.make_step()


if __name__ == '__main__':
    PG = Playground(fp='D:/Gitfiles/snake/testmap.txt')
    print(PG.field.raw_matrix)






























