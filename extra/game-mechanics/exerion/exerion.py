# Exerion
import pgzrun
WIDTH = 600
HEIGHT = 800
ship = Actor('ship', center=(300, 700))
count = 0
startcol = 0
stripes = []
for s in range(0, 20):
    stripes.append((s+1)*4)
landscape = []
landitems = [1,2,3,3,2,1,2,3,2,3,1]
landindexes = [-5,-8,-10,-13,-14,-20,-22,-26,-28,-30,-31]
for l in range(0, 10):
    landscape.append(Actor('landscape'+str(landitems[l]), center=(300,1000)))
    landscape[l].index = landindexes[l]
    landscape[l].yoff = 0

def draw():
    drawLand()
    screen.draw.text("EXERION ZERO", center = (300, 60), owidth=0.5, ocolor=(255,255,0), color=(255,0,0) , fontsize=80)
    ship.draw()
    
def update():
    global count,startcol
    count += 1
    if keyboard.left and ship.x > 100:
        if ship.angle < 30: ship.angle +=2
        ship.x -= ship.angle/6
    if keyboard.right and ship.x < 500:
        if ship.angle > -30: ship.angle -=2
        ship.x -= ship.angle/6
    if keyboard.up and ship.y > 400 : ship.y -= 4
    if keyboard.down and ship.y < 750 : ship.y += 4
    if not keyboard.left and not keyboard.right:
        if ship.angle > 0: ship.angle -= 2
        if ship.angle < 0: ship.angle += 2
    for s in range(0, 20):
        stripes[s] += 0.2
    if stripes[0] > 10:
        stripes.insert(0, stripes.pop())
        stripes[0] = 1
        if startcol == 0:
            startcol = 40
        else:
            startcol = 0
        updateLandscape()
        
def drawLand():
    sh = (800-ship.y)/2
    screen.blit("background", (0, sh/2))
    y = 300 + sh
    col = startcol
    for l in range(0, 10):
        if landscape[l].index < 0:
            landscape[l].x = parallax(y)
            landscape[l].y = y - landscape[l].yoff -(landscape[l].index*23)-30
            landscape[l].yoff += 0.5
            landscape[l].draw()
    for s in range(0, 20):
        col = col + 40
        if col > 40: col = 0
        screen.draw.filled_rect(Rect((0, y), (600, stripes[s])),(200,col,0))
        for l in range(0, 10):
            if landscape[l].index == s:
                landscape[l].y = y-stripes[s]-30
                landscape[l].x = parallax(y)
                landscape[l].draw()
        y += stripes[s]-1
        
def updateLandscape():
    for l in range(0, 10):
        landscape[l].index += 1
        landscape[l].yoff = 0
        if landscape[l].index > 20:
            landscape[l].index = -10
            
def parallax(y):
    sh = (800-ship.y)/2
    return ((300-ship.x) * ((y-sh)/500))+300
    
pgzrun.go()
