# Gradius
import pgzrun
from random import randint

jet = Actor('jet',(400,300))
bullet = Actor('bullet', center=(850, 0))
rocks = []

def draw():
    screen.blit("background", (0, 0))
    drawRocks()
    screen.blit("foreground", (0, 0))
    bullet.draw()
    jet.draw()
    
def update():
    if keyboard.up: jet.y = limit(jet.y-5,50,550)
    if keyboard.down: jet.y = limit(jet.y+5,50,550)
    if keyboard.left: jet.x = limit(jet.x-5,10,790)
    if keyboard.right: jet.x = limit(jet.x+5,10,790)
    if keyboard.space :
        if bullet.x >= 850 : bullet.pos = (jet.x,jet.y+5)
    if bullet.x < 850: bullet.x += 20
    updateRocks()

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

def drawRocks():
    for r in range(0, len(rocks)):
        rocks[r].draw()

def makeRock(pos):
    r = len(rocks)
    if r < 100:
        rocks.append(Actor('rock'+str(randint(1,3)), center=pos))
    else:
        r = getOldRock()
        rocks[r].pos = pos
    rocks[r].speed = randint(6,12)
    rocks[r].dir = (randint(0,60)-30)/10
    
def updateRocks():
    if randint(0,10) == 1: makeRock((215,480))
    if randint(0,10) == 1: makeRock((540,480))
    shieldsUp = False
    for r in range(0, len(rocks)):
        if rocks[r].y < 800:
            rocks[r].y -= rocks[r].speed
            rocks[r].x += rocks[r].dir
            rocks[r].speed -= 0.2
            if jet.colliderect(rocks[r]):
                shieldsUp = True
            if bullet.colliderect(rocks[r]):
                rocks[r].y = 800
                bullet.x = 850
    if shieldsUp == True:
        jet.image = "jet2"
    else:
        jet.image = "jet"

def getOldRock():
    for r in range(0, len(rocks)):
        if rocks[r].y >= 800:
            return r

pgzrun.go()
