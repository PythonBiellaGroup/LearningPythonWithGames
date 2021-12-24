# https://github.com/Wireframe-Magazine/Wireframe53
# Wireframe #53: 
import pgzrun
import math
import random
from pygame import image, Color
WIDTH = 600
HEIGHT = 800
collisionMap = image.load('images/background.png')
flipperLeft = Actor('flipperl',center=(210,660), anchor=(20, 20))
flipperLeft.angle = -30
flipperRight = Actor('flipperr',center=(390,660), anchor=(112, 20))
flipperRight.angle = 30

def init():
    global gamestate, ball
    ball = Actor('ball', center=(560,310))
    ball.speed = 5 + random.randint(0, 7)
    ball.dir = 4 + ((random.randint(0, 10)/10)-0.5)
    gamestate = 0

def draw():
    screen.blit("background", (0, 0))
    flipperLeft.draw()
    flipperRight.draw()
    if gamestate == 0 or random.randint(0,1) == 1: ball.draw()
   
def update():
    if gamestate == 0:
        if keyboard.left:
            flipperLeft.angle = limit(flipperLeft.angle+20, -30, 30)
        else:
            flipperLeft.angle = limit(flipperLeft.angle-20, -30, 30)
        if keyboard.right:
            flipperRight.angle = limit(flipperRight.angle-20, -30, 30)
        else:
            flipperRight.angle = limit(flipperRight.angle+20, -30, 30)
        moveBall()
        checkBounce()
    else:
        if keyboard.space: init()       

def moveBall():
    global gamestate
    ball.x += ball.speed * math.sin(ball.dir)
    ball.y += ball.speed * math.cos(ball.dir)
    if ball.x > 570 or ball.y > 760: gamestate = 1

def checkBounce():
    global score
    d = math.degrees(ball.dir)%360
    inc = -1.5
    if d > 90 and d < 270:
        inc = 1.5
        ball.speed -= 0.03
        if ball.speed < 0: ball.dir = 0
    else:
        if ball.speed < 10: ball.speed += 0.04
    if flipperRight.collidepoint(ball.pos):
        ball.dir = 4 + (flipperRight.angle/50)
        if keyboard.right :
            ball.speed += 0.3
            moveBall()
        if inc == 1.5:
            ball.dir = 0
        moveBall()
    if flipperLeft.collidepoint(ball.pos):
        ball.dir = 3 +(flipperLeft.angle/50)
        if keyboard.left :
            ball.speed += 0.3
            moveBall()
        if inc == 1.5:
            ball.dir = 0
        moveBall()
    rgb = collisionCheck()
    while rgb != Color("black"):
        ball.dir += inc
        moveBall()
        rgb = collisionCheck()
        
def collisionCheck():
    r = 22
    cl = [(0,-r),(r,0),(0,r),(-r,0)]
    for t in range(4):
        rgb = collisionMap.get_at((int(ball.x)+cl[t][0],int(ball.y)+cl[t][1]))
        if rgb != Color("black"):
            return rgb
    return rgb

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

init()
pgzrun.go()
