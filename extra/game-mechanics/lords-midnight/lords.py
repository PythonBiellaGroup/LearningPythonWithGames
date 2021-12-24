# https://github.com/Wireframe-Magazine/Wireframe57
# Wireframe #57: 
import pgzrun
from pygame import transform, image, Color

playerx = 50
playery = 50
playerdir = 0
myDirs = [(0,1, "North"),(-1,1, "North East"),(-1,0, "East"),(-1,-1, "South East"),(0,-1, "South"),(1,-1, "South West"),(1,0, "West"),(1,1, "North West")]
landscape = image.load('images/landscape.png')
tree = image.load('images/tree1.png')
mountain = image.load('images/mountain1.png')
tower = image.load('images/tower1.png')
    
def draw():
    screen.blit("background", (0, 0))
    drawLandscape()
    d = int(playerdir/45)
    if d > 7: d -= 8
    screen.draw.text("You are facing "+myDirs[d][2], center = (400, 50), owidth=0.5, ocolor=(255,255,255), color=(0,0,0) , fontsize=60, fontname="blackchancery" )
    
def update():
    pass

def on_key_down(key):
    global playerdir
    if key.name == "RIGHT":
        playerdir += 45
        if playerdir > 360: playerdir -= 360
    if key.name == "LEFT":
        playerdir -= 45
        if playerdir < 0: playerdir += 360
    if key.name == "UP":
        movePlayer()
    
def drawLandscape():
    global gameStatus
    rotatedLand = rotatedLandscape()
    playerpos = getPlayerPos(rotatedLand)
    x = playerpos[0]
    y = playerpos[1]
    for r in range(9,0,-1):
        for c in range(-5*int(r/2),5*int(r/2),1):
            pixel = rotatedLand.get_at((x-c,y-r))
            s = r*10
            d = (10-r)*20
            if pixel == Color('blue'):
                i = transform.scale(mountain, ((10-r)*50, (10-r)*40))
                screen.blit(i,(200+s-(d*c),180+(r*5)))
            if pixel == Color('green'):
                i = transform.scale(tree, ((10-r)*20, (10-r)*20))
                screen.blit(i,(290+s-(d*c),310-(r*8)))
            if pixel == Color('red'):
                i = transform.scale(tower, ((10-r)*20, (10-r)*20))
                screen.blit(i,(290+s-(d*c),310-(r*8)))
        
def rotatedLandscape():
    land = landscape.copy()
    land.set_at((playerx,playery),Color("black"))
    land.set_at((playerx+1,playery),Color("black"))
    rotated_image = transform.rotate(land, playerdir)
    return rotated_image

def getPlayerPos(i):
    s = i.get_size()
    for x in range(s[0]):
        for y in range(s[1]):
            if i.get_at((x,y)) == Color("black"): return (x,y)
            
def movePlayer():
    global playerx, playery
    d = int(playerdir/45)
    if d > 7: d -= 8
    if playerx - myDirs[d][0] > 25 and playerx - myDirs[d][0] < 75 and playery - myDirs[d][1] > 25 and playery - myDirs[d][1] <75:
        playerx -= myDirs[d][0]
        playery -= myDirs[d][1]

pgzrun.go()
