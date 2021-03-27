# Pipe Mania
from math import floor
from pygame import image, Color, Surface
from random import randint

w, h = 10, 7
matrix = [[0 for x in range(w)] for y in range(h)]
tileSize = 68
panelPosition = (96, 96)
numberNextTiles = 5
nextTiles = [randint(2, 8) for y in range(numberNextTiles)]
nextTilesPosition = (16, 28)
tileMouse = (-1, -1)

waterWays = Surface((w*tileSize, h*tileSize))
waterWays.fill(Color('black'))

tiles = ['empty', 'start',
         'hori', 'vert', 'cross',
         'bottomleft', 'bottomright',
         'topleft', 'topright']

ways = [image.load('images/'+tiles[i]+'_way.png') for i in range(1,9)]

matrix[3][2] = 1 # start tile
waterWays.blit(ways[0], (2 * tileSize, 3 * tileSize))
currentPoint = (2 * tileSize + 43, 3 * tileSize + 34)
waterFlow = []
start = 60*30 # 30 seconds

playState = 1

pointsToCheck = [(2, 0),( 0,2),(-2, 0),( 0,-2),
                 (2, 1),( 1,2),(-2, 1),( 1,-2),
                 (2,-1),(-1,2),(-2,-1),(-1,-2),
                 (2,-2),( 2,2),(-2, 2),(-2,-2)]

def draw():
    screen.blit('background', (0,0))
    for x in range(w):
        for y in range(h):
            screen.blit(tiles[matrix[y][x]]+'_block', (panelPosition[0] + x * tileSize, panelPosition[1] + y * tileSize))
    for y in range(numberNextTiles):
        screen.blit(tiles[nextTiles[y]]+'_block', (nextTilesPosition[0], nextTilesPosition[1] + y * tileSize))
    for point in waterFlow:
        screen.blit('water', point)
    if playState == 1:
        if tileMouse[0] >= 0 and tileMouse[1] >= 0:
            screen.blit(tiles[nextTiles[-1]]+'_block', (panelPosition[0] + tileMouse[0] * tileSize, panelPosition[1] + tileMouse[1] * tileSize))
        if start > 0:
            screen.draw.text("Start in " + str(floor(start / 60)), center=(400, 50), fontsize=35)
    else:
        screen.draw.text("GAME OVER. Points: "+str(len(waterFlow)), center=(400, 50), fontsize=35)        

def update():
    global start, playState
    if start > 0:
        start -= 1
    elif playState == 1:
        if not CheckNextPointDeleteCurrent():
            playState = 0

def CheckNextPointDeleteCurrent():        
    global currentPoint
    for point in pointsToCheck:
        newPoint = (currentPoint[0] + point[0], currentPoint[1] + point[1])
        if newPoint[0] < 0 or newPoint[1] < 0 or newPoint[0] >= w*tileSize or newPoint[1] >= h*tileSize:
            return False # goes outside the screen
        if waterWays.get_at(newPoint) != Color('black'):
            waterWays.set_at(newPoint, Color('black'))
            waterFlow.append((newPoint[0] + panelPosition[0] - 4, newPoint[1] + panelPosition[1] - 4))
            currentPoint = newPoint
            return True
    return False # no next point found
    
def on_mouse_down(pos):
    if playState == 1 and tileMouse[0] >= 0 and tileMouse[1] >= 0:
        if matrix[tileMouse[1]][tileMouse[0]] != 1: # not start tile
            matrix[tileMouse[1]][tileMouse[0]] = nextTiles[-1]
            waterWays.fill(Color('black'), (tileMouse[0] * tileSize, tileMouse[1] * tileSize, tileSize, tileSize))
            waterWays.blit(ways[nextTiles[-1] - 1], (tileMouse[0] * tileSize, tileMouse[1] * tileSize))
            for i in reversed(range(numberNextTiles - 1)):
                nextTiles[i + 1] = nextTiles[i]
            nextTiles[0] = randint(2, 8)

def on_mouse_move(pos):
    global tileMouse
    if playState == 1:
        tileMouse = (int((pos[0] - panelPosition[0])/tileSize), int((pos[1] - panelPosition[1])/tileSize))
        if pos[0] < panelPosition[0] or pos[1] < panelPosition[1] or tileMouse[0] >= w or tileMouse[1] >= h:
            tileMouse = (-1, -1) # mouse outside panel

