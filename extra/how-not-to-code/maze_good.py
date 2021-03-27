import pgzrun, pygame
from shared import *
from player import Player
from controls import KeyboardControls, JoystickControls

WIDTH,HEIGHT = 576,320

controls = JoystickControls(0) if pygame.joystick.get_count() > 0 else KeyboardControls()
player = Player( (64,64), controls )

def update():
    player.update()

def draw():
    screen.clear()

    for row_index in range(len(GRID)):
        for column_index in range(len(GRID[row_index])):
            if GRID[row_index][column_index] != ' ':
                x, y = column_index * GRID_SQ_SIZE, row_index * GRID_SQ_SIZE
                screen.blit('gridblock',(x,y))

    player.draw()

pgzrun.go()
