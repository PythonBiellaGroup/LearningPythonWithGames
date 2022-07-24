# Bomb Jack
import pgzrun
WIDTH = 600
HEIGHT = 650
jack = Actor('jackf',(300,300))
ground = Actor('ground',(300,640))
roof = Actor('roof',(300,61))
platform1 = Actor('platform1',(400,180))
platform2 = Actor('platform2',(420,580))
platform3 = Actor('platform3',(320,440))
platform4 = Actor('platform4',(180,250))
platform5 = Actor('platform5',(120,510))
platformList = [roof,ground,platform1,platform2,platform3,platform4,platform5]
jack.thrust = gameState = count = frame = score = 0
jack.dir = "l"
bombs = []
bombXY = [(110,95),(170,95),(230,95),(430,95),(490,95),(550,95),(40,290),(40,350),(40,410),(40,470),(560,290),(560,350),(560,410),(560,470),(110,605),(170,605),(230,605),(360,545),(420,545),(480,545)]
for b in bombXY:
    bombs.append(Actor('bomb1', center=(b[0], b[1])))
    bombs[len(bombs)-1].state = 1

def draw():
    screen.blit("background",(0,0))
    for p in platformList: p.draw()
    for b in bombs :
        if b.state > 0 :
            b.image = "bomb"+str(int(b.state))
            b.draw()
    jack.draw()
    screen.draw.text("SCORE:"+str(score), center= (300, 28), owidth=0.5, ocolor=(255,255,255), color=(255,0,0) , fontsize=40)
    if gameState == 1: screen.draw.text("LEVEL CLEARED", center = (300, 300), owidth=0.5, ocolor=(255,255,255), color=(0,255,255) , fontsize=50)
    
def update():
    global count, frame
    if gameState == 0:
        jack.dir = "f"
        ytest = jack.y
        if keyboard.up:
            jack.dir = "u"
        if checkCollisions(platformList,(jack.x,jack.y+(jack.height/2))) == False : jack.y += 4
        if checkCollisions(platformList,(jack.x,jack.y-32)) == False : jack.y -= jack.thrust
        jack.thrust = limit(jack.thrust-0.4,0,20)
        if jack.y > ytest+1: jack.dir = "d"
        if jack.y < ytest-1: jack.dir = "u"
        if keyboard.left and jack.x > 40:
            if jack.y != ytest:
                jack.dir = "lf"
                jack.y -= 2
            else:
                jack.dir = "l" + str(frame%2+1)
            jack.x -= 2
        if keyboard.right and jack.x < 560:
            if jack.y != ytest:
                jack.dir = "rf"
                jack.y -= 2
            else:
                jack.dir = "r" + str(frame%2+1)
            jack.x += 2
        jack.image = "jack" + jack.dir
        checkBombs()
        count += 1
        if(count%5 == 0) : frame += 1

def on_key_down(key):
    global gameState
    if gameState == 0:
        if key.name == "UP" and jack.dir == "f":
            jack.thrust = 20
            jack.dir = "u"

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

def checkCollisions(cList, point):
    for i in range(0, len(cList)):
        if cList[i].collidepoint(point):
            return True
    return False

def checkBombs():
    global gameState, score
    bombsCollected = 0
    for b in bombs:
        if b.state > 1: b.state += 0.4
        if b.state == 0 : bombsCollected += 1
        if b.collidepoint((jack.x,jack.y)) and b.state == 1:
            b.state = 1.4
        if int(b.state) > 4 :
            b.state = 0
            score += 100
    if bombsCollected == len(bombs): gameState = 1
            
pgzrun.go()
