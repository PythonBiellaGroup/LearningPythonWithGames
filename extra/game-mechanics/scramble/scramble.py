# Scramble
from random import randint
from pygame import Surface
from pygame.locals import *
import math

scrambleSurface = Surface((800,600),SRCALPHA)
landLevel = 600
roofLevel = 10
landChange = -3
roofChange = 3
jet = Actor('jet',(400,300))
speed = 3
crash = False

def draw():
    if crash: # remove the next line if you are affected by flashing lights
        screen.fill((randint(100,200),0,0))
        screen.blit(scrambleSurface, (0, 0))
        jet.draw()
    else:
        screen.blit('space',(0,0))
        screen.blit(scrambleSurface, (0, 0))
        jet.draw()
    
def update():
    global speed, crash
    if crash == False:
        if keyboard.up: jet.y -= speed
        if keyboard.down: jet.y += speed
        if keyboard.left: speed = limit(speed-0.1,1,10)
        if keyboard.right: speed = limit(speed+0.1,1,10)
        jet.x = 310 + (speed * 30)
        for _ in range(math.ceil(speed)):
            updateLand()
        if scrambleSurface.get_at((math.ceil(jet.x+32),math.ceil(jet.y))) != (0,0,0,0):
            crash = True;
    
def updateLand():
    global landLevel, landChange, roofLevel, roofChange
    if randint(0,10) == 3: roofChange = randint(0,6) - 3
    if randint(0,10) == 3: landChange = randint(0,6) - 3
    roofLevel += roofChange
    landLevel += landChange
    landLevel = limit(landLevel,200,590)
    roofLevel = limit(roofLevel,10,400)
    if roofLevel > landLevel-200: roofLevel = landLevel-200
    scrambleSurface.scroll(-1,0)
    drawLand()

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)
    
def drawLand():
    for i in range(0, 600):
        c = (0,0,0,0)
        if i > landLevel:
            g = limit(i-landLevel,0,255)
            c = (255,g,0)
        else:
            if i < roofLevel:
                r = limit(roofLevel-i,0,255)
                c = (255,r,0)
        scrambleSurface.set_at((799,i),c)
      
