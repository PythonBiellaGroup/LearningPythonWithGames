import pgzrun
from random import randint

WIDTH,HEIGHT = 1200,448
MAX_DEPTH = 20
GRID_SQ_SIZE = 64
TILE_SPRITES = {'X': 'gridblock', '.': 'wall'}
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

GRID = ['XXXXXXXXXXXXXXXXXXX',
        'X..  .   ..       X',
        'X.X X.X X X X X X X',
        'X .. ..  . ..     X',
        'X X X X X X X X X X',
        'X  .   . ..   .   X',
        'XXXXXXXXXXXXXXXXXXX']

def snake_step_score(score, depth, snake):
   head_pos = snake[0]
   square = GRID[head_pos[1]][head_pos[0]]
   if square == ' ':
       snake = snake[:-1]
   if square == 'X' or head_pos in snake[1:]:
      return score/2
   elif square == '.':
      score += 2
   else:
      score += 1

   if depth <= 0:
      return score

   best_score = 0
   for dir in DIRECTIONS:
      new_head_pos = (head_pos[0]+dir[0],
                      head_pos[1]+dir[1])
      result = snake_step_score(score, depth-1,
                          [new_head_pos]+snake)
      best_score = max(result, best_score)

   return best_score

snake = [(1,1)]

def change_grid_pos(row,col,char):
   grid_row = GRID[row]
   new_row = grid_row[:col] + char + grid_row[col+1:]
   GRID[row] = new_row

def update_snake():
   global snake
   head_pos = snake[0]
   best_score, best_snake = 0, None
   new_pos_eats_wall = False
   for dir in DIRECTIONS:
      new_head_pos = (head_pos[0] + dir[0],
                      head_pos[1] + dir[1])
      new_snake = [new_head_pos] + snake
      result = snake_step_score(0, MAX_DEPTH, new_snake)
      if result > best_score:
         best_score = result
         best_snake = new_snake
         new_pos_eats_wall = GRID[new_head_pos[1]][new_head_pos[0]] == '.'

   if best_snake != None:
      snake = best_snake
      if not new_pos_eats_wall:
         snake = snake[:-1]
      else:
         new_head_pos = snake[0]
         change_grid_pos(new_head_pos[1],
                         new_head_pos[0], ' ')

def update():
   update_snake()

def draw():
   screen.clear()
   for row in range(len(GRID)):
      for col in range(len(GRID[row])):
         square = GRID[row][col]
         if square in TILE_SPRITES:
            x = col * GRID_SQ_SIZE
            y = row * GRID_SQ_SIZE
            screen.blit(TILE_SPRITES[square], (x, y))
         pos = (col, row)
         if pos in snake:
            if pos == snake[0]:
                image = 'snakehead'
            else:
                image = 'snakebody2'
            screen.blit(image, (col * GRID_SQ_SIZE,
                                row * GRID_SQ_SIZE))

pgzrun.go()
