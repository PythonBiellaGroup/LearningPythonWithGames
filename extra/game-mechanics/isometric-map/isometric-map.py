# https://github.com/Wireframe-Magazine/Wireframe-15
# Wireframe #15: Make an isometric game map, pages 38-39
import pgzrun
import numpy as np # easy handling of three dimensional lists
WIDTH = 600 # Width of window
HEIGHT = 400 # Height of window
mapPositionX = 268 # start displaying the map from 
mapPositionY = -100 # these window co-ordinates
mapWidth = mapHeight = 20 # the width and height of the map
mapBlocks = np.zeros((mapWidth,mapHeight,3)) # make a blank map in a 3 dimensional list
# draw the window
def draw():
    screen.fill((150, 255, 255))
    drawMap()
# Move the map with the arrow keys
def update():
    global mapPositionX, mapPositionY
    if keyboard.left: mapPositionX -= 4
    if keyboard.right: mapPositionX += 4
    if keyboard.up: mapPositionY -= 4
    if keyboard.down: mapPositionY += 4
# Draw the map to the window by drawing the blocks layer by layer
def drawMap():
    for z in range(0, 3):
        for x in range(0, mapWidth):
            for y in range(0, mapHeight):
                bx = (x*32) - (y*32) + mapPositionX
                by = (y*16) + (x*16) - (z*32) + mapPositionY
                # Only display blocks that are in the window
                if -64 <= bx < WIDTH + 32 and -64 <= by < HEIGHT + 32:
                    if mapBlocks[x][y][z] == 1: # 1 means a block is in this position
                        # The next line needs an image called "block.png" to be in
                        # a subdirectory called "images"
                        screen.blit("block", (bx, by))
# Make a three layer arch
def makeArch(x,y):
    for z in range(0, 3):
        mapBlocks[x][y][z] = 1
        mapBlocks[x][y+2][z] = 1
    mapBlocks[x][y+1][2] = 1
# Make a three layer pyramid
def makePyramid(x,y):
    for px in range(0, 5):
        for py in range(0,5):
            mapBlocks[px+x][py+y][0] = 1
    for px in range(1, 4):
        for py in range(1,4):
            mapBlocks[px+x][py+y][1] = 1
    mapBlocks[x+2][y+2][2] = 1
# Map building section - make a border, some arches and some pyramids
for x in range(0, mapWidth):
    for y in range(0, mapHeight):
        if x == 0 or x == mapWidth-1 or y == 0 or y == mapHeight-1:
            mapBlocks[x][y][0] = 1
        if x == 5 and (y == 4 or y == 13):
            makeArch(x,y)
        if x == 12 and y == 14:
            makeArch(x,y)
        if (x == 4 or x == 12) and y == 7:
            makePyramid(x,y)
# Let's get this party started
pgzrun.go()