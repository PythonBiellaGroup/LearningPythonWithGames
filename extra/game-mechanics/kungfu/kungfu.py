# Kung Fu Master
import random

HEIGHT = 450
gameState = count = 0
bloke = Actor('walkl_0001', center=(400, 250))
blokeDir = "l"
backPos = -500
dudes = []
action = ""
actioncount = 0

def draw():
    screen.fill((0,0,0))
    screen.blit("background", (backPos, 30))
    screen.draw.text("Pygame Zero Kung Fu Master", center = (400, 15), owidth=1, ocolor=(255,0,0), color=(255,255,0) , fontsize=30)
    if gameState != 1 or (gameState == 1 and count%2 == 0):bloke.draw()
    for d in dudes:
        d.draw()
        
def on_key_down(key):
    global action, actioncount
    actioncount = 10
    if gameState == 0:
        if key.name == "A": action = "punch"
        if key.name == "Q": action = "kick"
    
def update():
    global count, backPos, blokeDir, action, actioncount
    if gameState == 0:
        bloke.image = 'stand' + blokeDir
        if action == "punch": bloke.image = 'punch'+blokeDir
        if action == "kick": bloke.image = 'kick'+blokeDir
        if actioncount <= 0: action = ""
        if keyboard.left: moveBloke(3,"l")
        elif keyboard.right: moveBloke(-3,"r")
        if random.randint(0, 100) == 0: makeDude()
        updateDudes()
    count += 1
    actioncount -= 1

def moveBloke(x,d):
    global backPos, blokeDir
    frame = int((count%48)/8) + 1
    if backPos + x < -3 and backPos + x > -1197:
        backPos += x
        moveDudes(x)
        bloke.image = 'walk'+d+'_000'+str(frame)
        blokeDir = d
    
def makeDude():
    d = len(dudes)
    if random.randint(0, 1) == 0:
        dudes.append(Actor('duder_0001', center=(-50,250)))       
    else:
        dudes.append(Actor('dudel_0001', center=(850, 250)))
    dudes[d].status = 0

def updateDudes():
    global gameState
    frame = int((count%48)/8) + 1
    for d in dudes:
        if (bloke.image == 'punch'+blokeDir or bloke.image == 'kick'+blokeDir) and bloke.collidepoint((d.x, d.y)):
            d.status += 1
        if d.x <=400:
            if d.status > 10:
                d.image = 'dudefallr'
                d.y += 5
            else:
                d.x += 2
                d.image = 'duder_000'+str(frame)
        if d.x >400:
            if d.status > 10:
                d.image = 'dudefalll'
                d.y += 5
            else:
                d.x -= 2
                d.image = 'dudel_000'+str(frame)
        if d.x > 398 and d.x < 402 and d.status == 0: gameState = 1

def moveDudes(x):
    for d in dudes:
        d.x += x
