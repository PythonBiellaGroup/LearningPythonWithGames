# Fire
import pgzrun
count = catcherPos = moveCatcher = gameState = score = 0
catchers = []
jumpers = []
jumperPositions = [(130,220),(190,260),(210,320),(220,360),(240,410),(260,360),
                   (270,320),(290,250),(320,220),(340,250),(360,300),(380,360),
                   (390,410),(420,360),(430,300),(470,250),(500,300),(520,360),
                   (538,410),(580,360),(600,320),(620,350)]
for c in range(3):
    catchers.append(Actor('catcher'+str(c), center=(240+(c*150), 425)))

def draw():
    screen.blit("background",(0,0))
    for c in range(3):
        if catcherPos == c: catchers[c].draw()
    for j in jumpers:
        if j.state == 0: j.draw()
        if j.state == -1 and count%2 == 0: j.draw()
    screen.draw.text("SAVED: "+str(score), topleft = (580, 120), color=(0,0,0) , fontsize=25)
    
def update():
    global count
    count += 1
    if(count%30 == 0) : doUpdate()
    if(count%2000 == 0) : makeJumper()

def doUpdate():
    global catcherPos, moveCatcher, gameState, score
    if gameState == 0:
        catcherPos = limit(catcherPos+moveCatcher, 0, 2)
        moveCatcher = 0
        for j in jumpers:
            if (j.frame < 21 and j.state == 0):
                j.frame += 1
                j.image = "jumper"+str(j.frame)
                j.pos = jumperPositions[j.frame]
            else:
                if j.state == 0:
                    j.state = 1
                    score += 1
                    makeJumper()
            if (j.frame == 4 and catcherPos != 0) or (j.frame == 12 and catcherPos != 1) or (j.frame == 18 and catcherPos != 2):
                j.state = -1
                j.image = "jumperdropped"
                j.y += 50
                gameState = 1

def on_key_down(key):
    global moveCatcher
    if key.name == "LEFT":
        moveCatcher = -1
    if key.name == "RIGHT":
        moveCatcher = 1
        
def makeJumper():
    if len(jumpers)%5 == 4:
        jumpers.append(Actor('jumper0', center=(130, 270)))
        jumpers[len(jumpers)-1].frame = 1
    else:
        jumpers.append(Actor('jumper0', center=(130, 220)))
        jumpers[len(jumpers)-1].frame = 0
    jumpers[len(jumpers)-1].state = 0

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

makeJumper()

pgzrun.go()
