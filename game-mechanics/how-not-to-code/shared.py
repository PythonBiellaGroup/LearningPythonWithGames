GRID = ['XXXXXXXXX',
        'X       X',
        'X X X X X',
        'X       X',
        'XXXXXXXXX']

GRID_SQ_SIZE = 64
HALF_GRID_SQ_SIZE = 64 // 2
SPEED = 2

# Convert pixel coordinates to grid coordinates
def get_grid_pos(x, y):
    return x // GRID_SQ_SIZE, y // GRID_SQ_SIZE
