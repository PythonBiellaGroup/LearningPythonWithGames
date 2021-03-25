import math
from random import randint
from pygame import image, Color
controlimage1 = image.load('images/guide1.png')
controlimage2 = image.load('images/guide2.png')
cars = []
for c in range(4):
    cars.append(Actor('car'+str(c), center=(400, 70+(30*c))))
    cars[c].speed = 0

def draw():
    screen.blit("track", (0, 0))
    for c in range(4):
        cars[c].draw()
    
def update():
    if keyboard.up: cars[0].speed += .15
    if keyboard.down: cars[0].speed -= .15
    if(cars[0].speed != 0):
        if keyboard.left: cars[0].angle += 2
        if keyboard.right: cars[0].angle -= 2
    for c in range(4):
        crash = False
        for i in range(4):
            if cars[c].collidepoint(cars[i].center) and c != i:
                crash = True
                cars[c].speed = -(randint(0,1)/10)
        if crash:
            newPos = calcNewXY(cars[c].center, 2, math.radians(randint(0,360)-cars[c].angle))
        else:
            newPos = calcNewXY(cars[c].center, cars[c].speed*2, math.radians(180-cars[c].angle))
        if c == 0:
            ccol = controlimage1.get_at((int(newPos[0]),int(newPos[1])))
        else:
            ccol = controlimage2.get_at((int(newPos[0]),int(newPos[1])))
        if cars[c].speed != 0:
            if ccol != Color('blue') and ccol != Color('red'):
                cars[c].center = newPos
            else:
                if c > 0:
                    if ccol == Color('blue'):
                        cars[c].angle += 5
                    if ccol == Color('red'):
                        cars[c].angle -= 5
                cars[c].speed = cars[c].speed/1.1
        if c > 0 and cars[c].speed < 1.8+(c/10):
            cars[c].speed += randint(0,1)/10
            if crash:
                cars[c].angle += ((ccol[1]-136)/136)*(2.8*cars[c].speed)
            else:
                cars[c].angle -= ((ccol[1]-136)/136)*(2.8*cars[c].speed)
        else:
            cars[c].speed = cars[c].speed/1.1
            

def calcNewXY(xy,speed,ang):
    newx = xy[0] - (speed*math.cos(ang))
    newy = xy[1] - (speed*math.sin(ang))
    return newx, newy
