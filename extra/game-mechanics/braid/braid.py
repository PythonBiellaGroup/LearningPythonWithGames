# Braid
import pgzrun
from pygame import image

tim = Actor('timr1',(220,400))
tim.dir = "r"
tim.frame = 1
tim.ystore = tim.xstore = tim.jumping = 0
collisionMap = image.load('images/backgroundcol.png')
levelx = backx = count = 0
gameData = []

def draw():
    screen.blit("backgroundl1", (backx, 0))
    screen.blit("backgroundl2", (levelx, -50))
    tim.draw()
    screen.draw.text("Game Time: "+str(int(count/60)), topleft = (20, 5),color=(255,255,255) , fontsize=28)
    
def update():
    global levelx,backx,count
    if keyboard.backspace:
        playGameData()
        tim.image = "tim"+tim.dir+str(tim.frame)
    else:
        rgbtop = collisionMap.get_at((int(tim.x - levelx),int(tim.y+30)))
        rgbbottom = collisionMap.get_at((int(tim.x - levelx),int(tim.y+50)))
        tim.ystore = tim.y
        tim.xstore = tim.x
        if keyboard.left:
            if levelx < 0 and checkMove(-2):
                levelx += 2
                backx += 1
                tim.x -= 2
                tim.y -= 1
                tim.dir = "l"
                if count%7 == 0:
                    tim.frame += 1
                    if tim.frame > 5: tim.frame = 2
        if keyboard.right:
            if levelx > -480 and checkMove(2):
                levelx -= 2
                backx -= 1
                tim.x += 2
                tim.y -= 1
                tim.dir = "r"
                if count%7 == 0:
                    tim.frame += 1
                    if tim.frame > 5: tim.frame = 2
        if keyboard.up:
            if rgbtop == (0,0,255) or rgbbottom == (0,0,255):
                tim.y -= 5
                if tim.frame < 9 : tim.frame = 9
                if count%7 == 0:
                    tim.frame += 1
                    if tim.frame > 10: tim.frame = 9
        if keyboard.down:
            if rgbtop == (0,0,255) or rgbbottom == (0,0,255):
                if tim.frame < 9 : tim.frame = 9
                if count%7 == 0:
                    tim.frame += 1
                    if tim.frame > 10: tim.frame = 9
                if rgbbottom != (0,0,0): tim.y += 1
        if tim.jumping == 0: doGravity()
        else:
            if rgbtop == (255,255,255): tim.y -= tim.jumping/3
            tim.frame = 7
            tim.jumping -= 1
        if tim.y > tim.ystore+2: tim.frame = 8
        if tim.x == tim.xstore and tim.y == tim.ystore: tim.frame = 1
        tim.image = "tim"+tim.dir+str(tim.frame)
        count += 1
        storeGameData()
    
def storeGameData():
    newData = [tim.x,tim.y,tim.dir,tim.frame,levelx,backx]
    gameData.append(newData)

def playGameData():
    global count,levelx,backx,gameData
    if count > 2:
        tim.x = gameData[-1][0]
        tim.y = gameData[-1][1]
        tim.dir = gameData[-1][2]
        tim.frame = gameData[-1][3]
        levelx = gameData[-1][4]
        backx = gameData[-1][5]
        for i in range(2): del gameData[-1]
        count = len(gameData)
    
def on_key_down(key):
    if key.name == "SPACE":
        rgb = collisionMap.get_at((int(tim.x - levelx),int(tim.y+100)))
        if rgb == (0,0,0):
            tim.frame = 6
            tim.jumping = 12

def doGravity():
    rgb = collisionMap.get_at((int(tim.x - levelx),int(tim.y+25+50)))
    if rgb[0] > 100 or rgb == (0,0,255): tim.y += 3
    
def checkMove(xinc):
    rgb = collisionMap.get_at((int(tim.x - levelx + xinc),int(tim.y + 50)))
    if rgb == (255,255,255) or rgb == (0,0,255): return True
    return False

pgzrun.go()
