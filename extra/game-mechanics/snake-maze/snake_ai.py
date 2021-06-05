import pgzrun
from random import randint

# It doesn't eat up the last two walls because it takes paths which COULD lead to eating those walls, but it can
# put it off indefinitely? esp with high max depth?

WIDTH,HEIGHT = 1200,704

MAX_DEPTH = 20

TILE_SPRITES = {'X': 'gridblock', '.': 'wall'}

# GRID = ['XXXXX',
#         'X.X.X',
#         'X.  X',
#         'X X.X',
#         'XXXXX']

GRID = ['XXXXXXXXXXXXXXXXXXX',
        'X..  .    ..      X',
        'X.X X.X X X X X X X',
        'X .. ..  . ..     X',
        'X X X X X X X X X X',
        'X  .  .   .  .    X',
        'X X X X X X X X X X',
        'X...  .   .       X',
        'X X X X X X X X X X',
        'X  .   . ..    .  X',
        'XXXXXXXXXXXXXXXXXXX']

# GRID = ['XXXXXXXXXXXXXXX',
#         'X.............X',
#         'X.X X.X X X X X',
#         'X.....   .....X',
#         'X X X X X X X X',
#         'X ...     ... X',
#         'X X X X X X X X',
#         'X...  .   ... X',
#         'X X X X X X X X',
#         'X  .   .   .  X',
#         'XXXXXXXXXXXXXXX']

GRID_SQ_SIZE = 64

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def snake_step_score(score, depth, snake):
    head_pos = snake[0]
    square = GRID[head_pos[1]][head_pos[0]]

    # Get shorter if this square is an empty space
    if square == ' ':
        snake = snake[:-1]

    # Are we hitting either an impassable wall or part of our own tail? (Exclude head)
    if square == 'X' or head_pos in snake[1:]:
        return score/100
    elif square == '.':
        score += 2  # Possible flaw: simulated snake could eat from this square multiple times
    else:
        score += 1

    if depth <= 1:
        return score

    best_score = 0

    # Check each direction
    for dir in DIRECTIONS:
        new_head_pos = (head_pos[0]+dir[0], head_pos[1]+dir[1])
        result = snake_step_score(score, depth-1, [new_head_pos] + snake)
        best_score = max(result, best_score)

    return best_score

snake = [(1,1)]

def change_grid_pos(row,col,char):
    # Replace a character in the grid. Strings in Python are immutable (i.e.
    # can't be changed) so we have to replace the whole row with a new row
    # which is the same as the old row but with that one character changed
    grid_row = GRID[row]
    new_row = grid_row[:col] + char + grid_row[col + 1:]
    GRID[row] = new_row

def update_snake():
    global snake
    head_pos = snake[0]
    best_score = 0
    best_snake = None
    new_pos_eats_wall = False
    for dir in DIRECTIONS:
        new_head_pos = (head_pos[0] + dir[0], head_pos[1] + dir[1])
        new_snake = [new_head_pos] + snake
        result = snake_step_score(0, MAX_DEPTH, new_snake)
        if result > best_score:
            best_score = result
            best_snake = new_snake
            new_pos_eats_wall = GRID[new_head_pos[1]][new_head_pos[0]] == '.'

    if best_snake != None:
        snake = best_snake
        if not new_pos_eats_wall:
            snake = snake[:-1]  # Remove last tail piece
        else:
            new_head_pos = snake[0]
            change_grid_pos(new_head_pos[1], new_head_pos[0], ' ')

def update():
    # Update snake
    update_snake()

    # 1/20 chance each update of adding a new edible wall (which might replace
    # an inedible wall)
    if randint(0,19) == 0:
        change_grid_pos(randint(1,len(GRID)-2), randint(1,len(GRID[0])-2), '.')

def draw():
    screen.clear()

    for row_index in range(len(GRID)):
        for column_index in range(len(GRID[row_index])):
            # Get the character at this grid position
            square = GRID[row_index][column_index]
            if square in TILE_SPRITES:
                x, y = column_index * GRID_SQ_SIZE, row_index * GRID_SQ_SIZE
                screen.blit(TILE_SPRITES[square], (x, y))
            pos = (column_index, row_index)
            if pos in snake:
                image = 'snakehead' if pos == snake[0] else 'snakebody2'
                screen.blit(image, (column_index * GRID_SQ_SIZE,row_index * GRID_SQ_SIZE))

pgzrun.go()
