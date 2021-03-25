# Donkey Kong Barrels
from random import randint
from pygame import image, Color
import math

barrels = []
platformMap = image.load('images/map.png')
spacer = 0

def draw():
    screen.blit("background", (0, 0))
    for b in range(len(barrels)):
        if onScreen(barrels[b].x, barrels[b].y):
            barrels[b].draw()
    
def update():
    global spacer
    if randint(0,100) == 1 and spacer < 0:
        makeBarrel()
        spacer = 100
    spacer -= 1
    for b in range(len(barrels)):
        x = int(barrels[b].x)
        y = int(barrels[b].y)
        if onScreen(x,y):
            testcol1 = testPlatform(x-16,y+16,0)
            testcol2 = testPlatform(x,y+16,0)
            testcol3 = testPlatform(x+16,y+16,0)
            move = 0
            if testcol1 > testcol3: move = 1
            if testcol3 > testcol1: move = -1
            barrels[b].x += move
            if move != 0: barrels[b].frame += move * 0.1
            else: barrels[b].frame += 0.1
            if barrels[b].frame >= 4: barrels[b].frame = 1
            if barrels[b].frame < 1: barrels[b].frame = 3.9
            testladder = platformMap.get_at((x,y+32))
            if testladder[2] == 255:
                if randint(0,150) == 1:
                    barrels[b].y += 20
            if testcol2 == 0: barrels[b].y += 1
            frame = str(math.floor(barrels[b].frame))
            if testPlatform(x,y+16,2) > 0:
                barrels[b].image = "bfrfront" + frame
            else:
                barrels[b].image = "bfrside" + frame

def onScreen(x,y):
    return x in range(16,784) and y in range(16,584)

def makeBarrel():
    barrels.append(Actor('bfrfront1', center=(200, 30)))
    barrels[len(barrels)-1].frame = 1
    
def testPlatform(x,y,col):
    c = 0
    for z in range(3):
        rgb = platformMap.get_at((x,y+z))
        c += rgb[col]
    return c
  
