# https://github.com/Wireframe-Magazine/Wireframe55
# Wireframe #55: 
import pgzrun
from pygame import image, Color
import math

car = Actor('car', center=(500, 300))
car.angle = 180
car.speed = 0
car.fuel = 130
car.temp = 60
mapx = 100*50
mapy = 70*50
cups = 0
miles = 0
count = gameStatus = 0
noisemap = image.load('images/noisemap.png')
    
def draw():
    drawMainMap()
    car.draw()
    screen.blit("sidepanel",(0,0))   
    drawMiniMap()
    screen.draw.filled_rect(Rect((60, 400), (car.fuel, 20)),(0,255,0))
    screen.draw.filled_rect(Rect((60, 349), (car.speed*26, 20)),(255,0,0))
    screen.draw.filled_rect(Rect((60, 450), (car.temp, 20)),(255,128,0))
    screen.draw.text(str(cups), center = (140, 548), owidth=0.5, ocolor=(255,255,255), color=(0,0,255) , fontsize=130)
    screen.draw.text(str(int(count/50)), center = (100, 108), color=(255,255,255) , fontsize=30)
    screen.draw.text(str(int(miles)), center = (100, 150), color=(255,255,255) , fontsize=30)
    if gameStatus == 1 : screen.draw.text("YOU GOT ALL THE CUPS!", center = (400, 300), owidth=0.5, ocolor=(255,255,255), color=(0,0,255) , fontsize=80)
    
def update():
    global mapx,mapy,miles, count,gameStatus
    if gameStatus == 0 :
        checkInput()
        if car.fuel > 0:
            mapx += -car.speed * math.sin(math.radians(car.angle))
            mapy += -car.speed * math.cos(math.radians(car.angle))
            car.fuel -= car.speed/100
            car.temp = limit(car.temp+((car.speed-3)/100),60,130)
            if car.temp > 120:
                car.speed -= 0.1
            miles += car.speed/500
        flagCount = 0
        count += 1

def checkInput():
    if keyboard.left: car.angle = (car.angle + 5)%360
    if keyboard.right: car.angle = (car.angle - 5)%360
    if keyboard.up: car.speed = limit(car.speed + 0.1, 0, 5)
    if keyboard.down: car.speed = limit(car.speed - 0.1, 0, 5)
    
def drawMainMap():
    global cups, gameStatus
    screen.draw.filled_rect(Rect((200, 0), (600, 600)),(255,255,0))
    xoff = mapx%50
    yoff = mapy%50
    for x in range(-1,13):
        for y in range(-1,13):
            pixel = noisemap.get_at((int((mapx/50)+x),int(mapy/50)+y))
            if pixel == Color('white'):
                screen.blit("boundary",(200+(x*50)-xoff,(y*50)-yoff))
                if x == 6 and y == 6: car.angle = (car.angle + 180)%360
            elif pixel == Color('green'):
                if x == 6 and y == 6: car.fuel = limit(car.fuel+1,0,130)
                screen.blit("fuel",(200+(x*50)-xoff,(y*50)-yoff))
            elif pixel == Color('red'):
                if x == 6 and y == 6:
                    noisemap.set_at((int((mapx/50)+x),int(mapy/50)+y), Color('black'))
                    cups += 1
                    if cups == 8: gameStatus = 1
                else: screen.blit("cup",(200+(x*50)-xoff,(y*50)-yoff))
            elif pixel.b > 200: screen.blit("dot",(200+(x*50)-xoff,(y*50)-yoff))
    
def drawMiniMap():
    carRect = Rect((5+(mapx/50),198+(mapy/50)),(4,4))
    if count%10 > 5: screen.draw.filled_rect(carRect,(0,0,0))
    else: screen.draw.filled_rect(carRect,(100,100,100))

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

pgzrun.go()
