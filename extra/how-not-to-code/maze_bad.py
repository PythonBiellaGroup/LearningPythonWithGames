import pgzero, pgzrun

WIDTH,HEIGHT = 576,320

GRID = ['XXXXXXXXX',
        'X       X',
        'X X X X X',
        'X       X',
        'XXXXXXXXX']

class Player(Actor):
    def __init__(self,pos):
        super().__init__('player', pos, anchor=('left', 'top'))

    def update(self):
        if keyboard.left:
            x = int(self.x) - 2
            y = int(self.y) + 64 // 2
            grid_x = x // 64
            grid_y = y // 64

            # The square ahead does not have a wall
            if GRID[grid_y][grid_x] == ' ':
                # Apply movement
                self.x -= 2

                # Lane alignment
                if y % 64 < 64 // 2:
                    self.y += 1
                elif y % 64 > 64 // 2:
                    self.y -= 1

        if keyboard.right:
            x = int(self.x) + 64 + 2 - 1
            y = int(self.y) + 64 // 2
            grid_x = x // 64
            grid_y = y // 64
            if GRID[grid_y][grid_x] == ' ':
                self.x += 2
                if y % 64 < 64 // 2:
                    self.y += 1
                elif y % 64 > 64 // 2:
                    self.y -= 1

        if keyboard.up:
            x = int(self.x) + 64 // 2
            y = int(self.y) - 2
            grid_x = x // 64
            grid_y = y // 64
            if GRID[grid_y][grid_x] == ' ':
                self.y -= 2
                if x % 64 < 64 // 2:
                    self.x += 1
                elif x % 64 > 64 // 2:
                    self.x -= 1

        if keyboard.down:
            x = int(self.x) + 64 // 2
            y = int(self.y) + 64 + 2 - 1
            grid_x = x // 64
            grid_y = y // 64
            if GRID[grid_y][grid_x] == ' ':
                self.y += 2
                if x % 64 < 64 // 2:
                    self.x += 1
                elif x % 64 > 64 // 2:
                    self.x -= 1

player = Player( (64,64) )

def update():
    player.update()

def draw():
    screen.clear()

    for row_index in range(len(GRID)):
        for column_index in range(len(GRID[row_index])):
            if GRID[row_index][column_index] != ' ':
                x, y = column_index * 64, row_index * 64
                screen.blit('gridblock',(x,y))

    player.draw()

pgzrun.go()
