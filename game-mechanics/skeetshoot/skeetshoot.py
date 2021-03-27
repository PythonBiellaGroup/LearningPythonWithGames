# Skeet Shoot
from random import randint
gameState = shootTimer = score = 0
shooter = Actor('shooter', center=(400, 450))
frameLeft = Actor('frame', center=(320, 350))
frameRight = Actor('frame', center=(480, 350))
skeets = []

def draw():
    screen.blit("background", (0, 0))
    if gameState == 0:
        for s in range(len(skeets)):
            if skeets[s].x > 0 and skeets[s].x < 800 and skeets[s].frame < 4:
                skeets[s].draw()
                screen.blit("shadow", (skeets[s].x-20, 400-(skeets[s].life/2)))
        shooter.draw()
        frameLeft.draw()
        frameRight.draw()
    else:
        screen.draw.text("ROUND OVER", center = (400, 300), owidth=0.5, ocolor=(255,255,255), color=(0,255,0) , fontsize=80)
    screen.blit("overlay", (0, 0))
    screen.draw.text("SCORE:"+str(score), center = (400, 550), owidth=0.5, ocolor=(255,255,255), color=(0,0,255) , fontsize=80)
    screen.draw.text("PYGAME ZERO SKEET SHOOT", center = (400, 55), owidth=0.5, ocolor=(255,255,255), color=(255,0,0) , fontsize=60)
    

def update():
    global shootTimer, gameState
    if gameState == 0: 
        if len(skeets) == 100: gameState = 1
        if randint(0,100) == 1: makeSkeet(700)
        if randint(0,100) == 2: makeSkeet(100)
        if shootTimer == 0:
            shooter.image = "shooter"
        else: shootTimer -= 1
        for s in range(len(skeets)):
            skeets[s].life += 1
            if skeets[s].frame > 0 and skeets[s].frame < 4:
                skeets[s].image = "skeet"+str(skeets[s].frame)
                skeets[s].frame += 1
            if skeets[s].x < 320 and skeets[s].dir == "right":
                skeets[s].distToLeftTarget = 320 - skeets[s].x
            else: skeets[s].distToLeftTarget = 999
            if skeets[s].x > 480 and skeets[s].dir == "left":
                skeets[s].distToRightTarget = skeets[s].x - 480
            else: skeets[s].distToRightTarget = 999
        targetLeft = getNearestSkeetY("left")
        if targetLeft > 0: frameLeft.y += (targetLeft-frameLeft.y)/2
        targetRight = getNearestSkeetY("right")
        if targetRight > 0: frameRight.y += (targetRight-frameRight.y)/2

def on_key_down(key):
    global shootTimer
    if (shootTimer == 0):
        if key.name == "LEFT":
            shooter.image = "shooter_l"
            shootTimer = 10
            checkShot("left")
        if key.name == "RIGHT":
            shooter.image = "shooter_r"
            shootTimer = 10
            checkShot("right")

def makeSkeet(st):
    skeets.append(Actor('skeet', center=(st, 370)))
    s = len(skeets)-1
    skeets[s].frame = 0
    skeets[s].life = 0
    skeets[s].distToLeftTarget = 999
    skeets[s].distToRightTarget = 999
    endpoint = 800
    skeets[s].dir = "right"
    if st > 400:
        endpoint = 0
        skeets[s].dir = "left"
    animate(skeets[len(skeets)-1], duration=3, pos=(endpoint, randint(-200,250)))

def getNearestSkeetY(leftorright):
    y = 0
    dist = 999
    for s in range(len(skeets)):
        if leftorright == "right":
            if(skeets[s].distToRightTarget < dist):
                dist = skeets[s].distToRightTarget
                y = skeets[s].y
        if leftorright == "left":
            if(skeets[s].distToLeftTarget < dist):
                dist = skeets[s].distToLeftTarget
                y = skeets[s].y
    return y

def checkShot(leftorright):
    global score
    sounds.shot.play()
    for s in range(len(skeets)):
        if leftorright == "right":
            if skeets[s].collidepoint((frameRight.x, frameRight.y)) and skeets[s].frame == 0:
                score += 1000
                skeets[s].frame = 1
        if leftorright == "left":
            if skeets[s].collidepoint((frameLeft.x, frameLeft.y)) and skeets[s].frame == 0:
                score += 1000
                skeets[s].frame = 1
