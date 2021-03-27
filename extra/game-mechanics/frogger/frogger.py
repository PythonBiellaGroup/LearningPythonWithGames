# Frogger

frog = Actor('frog1', center=(400, 580))
frog.direction = frog.delay = 0
frog.onBoard = -1
cars = []
floats = []
gameState = count = 0
for r in range(0, 6):
    for c in range(0, 4):
        cars.append(Actor('car'+str(r+1), center=((r*20)+(c*(240-(r*10))), 540-(r*40))))
        if r < 5: floats.append(Actor('float'+str(r+1), center=((r*20)+(c*(240-(r*10))), 260-(r*40))))

def draw():
    global count
    screen.blit("background", (0, 0))
    for c in range(0, 20):
        floats[c].draw()
    if gameState == 0 or (gameState == 1 and count%2 == 0): frog.draw()
    for c in range(0, 24):
        cars[c].draw()
    count += 1
    
def update():
    global gameState
    if gameState == 0:
        frog.onBoard = -1
        for r in range(0, 6):
            s = -1
            if r%2 == 0: s = 1
            for c in range(0, 4):
                i = (r*4)+c
                cars[i].x += s
                if cars[i].x > 840: cars[i].x = -40
                if cars[i].x < -40: cars[i].x = 840
                if cars[i].colliderect(frog): gameState = 1
                if r < 5:
                    floats[i].x -= s
                    if floats[i].x > 880: floats[i].x = -80
                    if floats[i].x < -80: floats[i].x = 880
                    if floats[i].colliderect(frog):
                        frog.onBoard = i
                        frog.x -= s
        if frog.delay > 0:
            frog.delay += 1
            if frog.delay > 10:
                frog.image = "frog1"
                frog.angle = frog.direction
        if frog.y > 60 and frog.y < 270 and frog.onBoard == -1: gameState = 1
    
def on_key_down(key):
    if gameState == 0:
        if key.name == "UP": frogMove(0,-40,0)
        if key.name == "DOWN": frogMove(0,40,180)
        if key.name == "LEFT": frogMove(-40,0,90)
        if key.name == "RIGHT": frogMove(40,0,270)

def frogMove(x,y,d):
    if 800 > frog.x+x > 0: frog.x += x
    if 600 > frog.y+y > 0: frog.y += y
    frog.image = "frog2"
    frog.delay = 1
    frog.angle = frog.direction = d
