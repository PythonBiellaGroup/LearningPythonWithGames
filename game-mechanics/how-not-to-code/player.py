from pgzero.actor import Actor
from shared import *

def move_towards(n, target, speed):
    if n < target:
        return min(n + speed, target)
    else:
        return max(n - speed, target)

class Player(Actor):
    def __init__(self, pos, controls):
        super().__init__('player', pos, anchor=('left', 'top'))
        self.controls = controls

    def update(self):
        x_dir = self.controls.get_x_dir()
        if x_dir == 0:
            y_dir = self.controls.get_y_dir()
        else:
            y_dir = 0

        if x_dir != 0 or y_dir != 0:
            self.move(x_dir, y_dir)

    def move(self, x_dir, y_dir):
        horizontal = x_dir != 0

        centre_x = int(self.x) + HALF_GRID_SQ_SIZE
        centre_y = int(self.y) + HALF_GRID_SQ_SIZE

        # Determine leading edge
        if horizontal:
            new_leading_edge_x = int(self.x) - SPEED if x_dir < 0 else int(self.x) + GRID_SQ_SIZE + SPEED - 1
            new_grid_x, new_grid_y = get_grid_pos(new_leading_edge_x, centre_y)
        else:
            new_leading_edge_y = int(self.y) - SPEED if y_dir < 0 else int(self.y) + GRID_SQ_SIZE + SPEED - 1
            new_grid_x, new_grid_y = get_grid_pos(centre_x, new_leading_edge_y)

        if GRID[new_grid_y][new_grid_x] == ' ':
            # The square ahead does not have a wall
            self.x += x_dir * SPEED
            self.y += y_dir * SPEED

            # Lane alignment
            # If we're going horizontally, we want to align on the Y axis and vice versa
            grid_x, grid_y = get_grid_pos(centre_x, centre_y)
            if horizontal:
                self.y = move_towards(self.y, grid_y * GRID_SQ_SIZE, 1)
            else:
                self.x = move_towards(self.x, grid_x * GRID_SQ_SIZE, 1)
