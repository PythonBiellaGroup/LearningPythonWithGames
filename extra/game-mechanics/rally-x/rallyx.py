# Rally X
from pygame import image, Color

car = Actor('car', center=(300, 300))
car.angle = 180
mapx = -100
mapy = 0
directionMap = {0:(0,1), 90:(1,0), 180:(0,-1), 270:(-1,0)}
speed = 5
collisionmap = image.load('images/collisionmap.png')
count = gameStatus = 0
flagsXY=[(200,1900),(300,1100),(300,300),(400,600),(600,1600),(800,350)]
flags = []
for f in range(0, 6):
    flags.append(Actor('flag', center=(0, 0)))
    flags[len(flags)-1].collected = False
    
def draw():
    screen.blit("colourmap",(mapx,mapy))
    car.draw()
    for f in range(0, 6):
        if not flags[f].collected: flags[f].draw()
    screen.blit("sidepanel",(600,0))   
    drawMiniMap()
    if gameStatus == 1 : screen.draw.text("YOU GOT ALL THE FLAGS!", center = (400, 300), owidth=0.5, ocolor=(255,255,255), color=(0,0,255) , fontsize=80)
    
def update():
    global mapx,mapy,count,gameStatus
    if gameStatus == 0 :
        checkInput()
        testmove = (int((-mapx+300) - ((directionMap[car.angle][0]*8) * speed)),int((-mapy+300) - ((directionMap[car.angle][1]*8) * speed)))
        if collisionmap.get_at(testmove) == Color('black'):
            mapx += directionMap[car.angle][0] * speed
            mapy += directionMap[car.angle][1] * speed
        else:
            car.angle += 90
            if car.angle == 360: car.angle = 0
        if collisionmap.get_at((int(-mapx+330), int(-mapy+300))) == Color('white'): mapx += 1
        if collisionmap.get_at((int(-mapx+270), int(-mapy+300))) == Color('white'): mapx -= 1
        if collisionmap.get_at((int(-mapx+300), int(-mapy+330))) == Color('white'): mapy += 1
        if collisionmap.get_at((int(-mapx+300), int(-mapy+270))) == Color('white'): mapy -= 1
        flagCount = 0
        for f in range(0, 6):
            flags[f].x = flagsXY[f][0]+mapx
            flags[f].y = flagsXY[f][1]+mapy
            if flags[f].collidepoint(car.pos):
                flags[f].collected = True
            if flags[f].collected == True: flagCount += 1
        count += 1
        if flagCount == 6: gameStatus = 1

def checkInput():
    if keyboard.left: car.angle = 90
    if keyboard.right: car.angle = 270
    if keyboard.up: car.angle = 0
    if keyboard.down: car.angle = 180
    
def drawMiniMap():
    carRect = Rect((658+(-mapx/5),208+(-mapy/5)),(4,4))
    if count%10 > 5:
        screen.draw.filled_rect(carRect,(0,0,0))
    else:
        screen.draw.filled_rect(carRect,(100,100,100))
    for f in range(0, 6):
        if not flags[f].collected:
            flagRect = Rect((600+(flagsXY[f][0]/5),150+(flagsXY[f][1]/5)),(4,4))
            screen.draw.filled_rect(flagRect,(255,255,0))
