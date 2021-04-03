# Manic Miner

HEIGHT = 400
willy = Actor('willyr0',(400,300))
willy.direction = "r"
willy.jump = 0
willy.onground = False
count = 0
platforms = [[1,1,0,0,0,0,1,1,0,0,2,2,2,1,1,1,1,0,0,0,0,0,0],
             [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1],
             [1,1,1,0,0,0,2,2,2,2,2,0,0,0,0,1,1,1,0,0,0,0,0],
             [0,0,1,1,0,0,0,0,0,0,0,0,1,1,2,2,0,0,1,1,1,0,0],
             [1,1,0,0,1,1,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,1,1],
             [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
platformActors = []
for r in range(len(platforms)):
    for c in range(len(platforms[r])):
        if(platforms[r][c] != 0 ): platformActors.append(Actor('platform'+str(platforms[r][c])+"1",(70+(c*30),120+(r*40))))
        platformActors[len(platformActors)-1].status = 0

def draw():
    screen.blit("background", (0, 0))
    willy.draw()
    drawPlatforms()
    
def update():
    global count
    willy.image = "willy"+ willy.direction + "0"
    if keyboard.left:
        moveWilly(-1,0)
        willy.direction = "l"
        willy.image = "willyl"+ str(int(count/8)%3)
        pass
    if keyboard.right:
        moveWilly(1,0)
        willy.direction = "r"
        willy.image = "willyr"+ str(int(count/8)%3)
        pass   
    checkGravity()
    count += 1
    
def on_key_down(key):
    if key.name == "SPACE":
        if willy.onground == True:
            willy.jump = 40

def drawPlatforms():
    for p in range(len(platformActors)):
        if platformActors[p].status != -1:
            platformActors[p].draw()
    
def moveWilly(x,y):
    if willy.x+x < 730 and willy.x+x > 70:
        willy.x += x

def checkGravity():
    if willy.jump > 0:
        willy.y -=2
        willy.jump -=1
    if willy.y < 320:
        willy.onground = False
        for p in range(len(platformActors)):
            frame = int(platformActors[p].image[-1])+1
            if platformActors[p].status > 0 :
                platformActors[p].status -= 1
                if platformActors[p].status == 0 :
                    platformActors[p].y += 1
                    if frame > 8 :
                        platformActors[p].status = -1
                    else:
                        platformActors[p].image = "platform2"+str(frame)
                        platformActors[p].status = 30
            if((willy.x > platformActors[p].x-20 and willy.x < platformActors[p].x+20) and willy.y+20 == platformActors[p].y-14+(frame-1) and platformActors[p].status != -1):
                willy.onground = True
                if platformActors[p].image[8] == "2":
                    if platformActors[p].status == 0 : platformActors[p].status = 30
        if willy.onground == False:
            willy.y += 1
    else:
        willy.onground = True