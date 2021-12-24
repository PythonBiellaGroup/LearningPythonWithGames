# https://github.com/Wireframe-Magazine/Wireframe54
# Wireframe #54: 
import pgzrun
import math
from pygame import image, Color

collisionMap = image.load('images/collision.png')
pointer = Actor('pointer',center=(90,85))
pointer.angle = 0
ball = Actor('ball', center=(100,150))
ball.speed = ball.dir = 0
gamestate = shots = 0
shotrange = 300

def draw():
    screen.blit("background", (0, 0))
    ball.draw()
    pointer.draw()
    screen.draw.filled_rect(Rect((180,5),(shotrange,10)),(255,0,0))
    screen.draw.text("SHOT RANGE:", topleft = (20, 2),color=(0,0,0) , fontsize=28)
    if gamestate == 1 : screen.draw.text("YOU SUNK THE BALL IN " + str(shots) + " STROKES", center = (400, 300), owidth=0.5, ocolor=(255,255,0), color=(255,0,0) , fontsize=50)
   
def update():
    global shotrange
    if gamestate == 0:
        if keyboard.left:
            pointer.angle += 5
        if keyboard.right:
            pointer.angle -= 5
        if keyboard.up:
            shotrange = limit(shotrange + 10, 0, 600)
        if keyboard.down:
            shotrange = limit(shotrange - 10, 0, 600)
        checkBounce()
        moveBall()
        ball.speed = limit(ball.speed-0.01, 0, 10)
        
def on_key_down(key):
    if gamestate == 0:
        if key.name == "RETURN": hitBall(pointer.angle,shotrange/100)

def hitBall(a,s):
    global shots
    ball.speed = s
    ball.dir = math.radians(a)
    shots += 1

def moveBall():
    ball.x += ball.speed * math.sin(ball.dir)
    ball.y += ball.speed * math.cos(ball.dir)

def checkBounce():
    global gamestate
    rgb = collisionCheck()
    if rgb == Color("black"):
        gamestate = 1
        
def collisionCheck():
    r = 4
    cl = [(0,-r),(r,0),(0,r),(-r,0)]
    for t in range(4):
        rgb = collisionMap.get_at((int(ball.x)+cl[t][0],int(ball.y)+cl[t][1]))
        if rgb != Color("white"):
            if rgb == Color("blue"):
                ball.dir = (2*math.pi - ball.dir)%(2*math.pi)
            if rgb == Color("red"):
                ball.dir = (3*math.pi - ball.dir)%(2*math.pi)   
    return rgb

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

pgzrun.go()
