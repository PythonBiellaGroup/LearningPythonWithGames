# Guitar Hero
import pgzrun
import time

curTime = time.time()
deltaTime = 0
startTime = 0
score = 0
bps = 100.5
firstTime = True
counters = []
shine = [0,0,0,0,0]
counterPoints = [(2,9.3),(0,11.5),(3,13.8),(1,16.2),(2,18.5),(0,20.7),
                 (2,23),(0,25),(3,27.6),(1,29.8),(2,32.1),(0,34.5),
                 (4,36.6),(1,38.9),(3,41),(1,43.5),(2,44.6),(3,45.7),(0,48),
                 (4,50.3),(1,52.5),(1,53.5),(2,53.9),(3,54.5),
                 (4,54.8),(2,57.1),(4,59.4),(2,61.7),(4,64.1),(2,66.6),(0,69.8)
                 ]
for c in counterPoints:
    counters.append(Actor('counter'+str(c[0]), center=(300+(c[0]*50), (c[1]-9.9)*-50)))
    counters[len(counters)-1].state = 1

def draw():
    screen.blit("background", (0, 0))
    drawCounters()
    screen.blit("fade", (0, 0))
    for s in range(0,5):
        if shine[s] > 0:
            screen.blit("shine", (230+(s*50), 450))
            shine[s] -= 1
    screen.draw.text("SCORE:"+str(score), center= (400,575), owidth=0.5, ocolor=(255,255,255), color=(0,0,255) , fontsize=40)
    if curTime - startTime > 70:
        screen.draw.text("WELL DONE! YOU ARE A", center= (400,280), owidth=0.5, ocolor=(255,255,255), color=(255,0,0) , fontsize=40)
        screen.draw.text("PYGAME ZERO HERO", center= (400,320), owidth=0.5, ocolor=(255,255,255), color=(255,0,0) , fontsize=40)
    
def update():
    global deltaTime, curTime, firstTime, startTime
    if firstTime:
        music.play_once('themoment')
        startTime = time.time()
        firstTime = False
    deltaTime = time.time()-curTime
    curTime = time.time()
    updateCounters()
    
def on_key_down(key):
    if key.name == "SPACE":
        for c in counters:
            if c.y > 490 and c.y < 525:
                if c.x == 300 and keyboard.z: noteCorrect(0)
                if c.x == 350 and keyboard.x: noteCorrect(1)
                if c.x == 400 and keyboard.c: noteCorrect(2)
                if c.x == 450 and keyboard.v: noteCorrect(3)
                if c.x == 500 and keyboard.b: noteCorrect(4)

def drawCounters():
    for c in counters:
        if c.y < 520 and c.y > -20:
            c.draw()

def updateCounters():
    for c in counters:
        c.y += (bps/2)*deltaTime
        
def noteCorrect(column):
    global score
    shine[column] = 10
    score += 10

pgzrun.go()
