# Skate or Die
import pgzrun
from pygame import image

skater = Actor('skaterl',center=(700,230), anchor=('center','bottom'))
skater.direction = "l"
skater.speed = 0
skater.switch = 0
halfpipe = image.load('images/halfpipe.png')
score = 0

def draw():
    screen.blit("background", (0, 0))
    skater.draw()
    screen.draw.text("SKATE OR DIE", center = (400, 40),color=(255,255,255) , owidth=0.5, ocolor=(255,0,0), fontsize=50)
    screen.draw.text("SCORE: "+str(score), center = (400, 90),color=(255,255,255) , fontsize=38)

def update():
    if skater.y < 600:
        if keyboard.left and skater.angle  > -20 and skater.speed <= 0:
            skater.speed = limit(skater.speed - 0.2,-13,0)
            skater.y -= 0.2
        if keyboard.right and skater.angle < 20 and skater.speed >= 0:
            skater.speed = limit(skater.speed + 0.2,0,13)
            skater.y -= 0.2
        pixel = halfpipe.get_at((int(skater.x),int(skater.y)))
        if skater.switch > 0:
            skater.switch -= 1
            angle = skater.angle
            if skater.switch == 30:
                if skater.direction == "l":
                    skater.direction = "r"
                    skater.speed = 1
                    angle = -90
                else:
                    skater.direction = "l"
                    skater.speed = -1
                    angle = 90
                skater.image = "skater"+skater.direction
            skater.angle = angle
            if skater.switch > 30:
                if skater.direction == "l":
                    skater.x += 0.6
                else:
                    skater.x -= 0.6
                skater.y -= 4
            else:
                skater.y += 3
        else:
            skater.x = limit(skater.x+skater.speed,20,780)
            if skater.x <= 20 or skater.x >=780 and skater.speed > 0:
                skater.speed = 0
                if skater.x <= 20:
                    skater.direction = "r"
                else:
                    skater.direction = "l"
                skater.image = "skater"+skater.direction
            if skater.x > 400:
                offset = 255-pixel.b
            else:
                offset = pixel.b-255
            skater.angle = (offset)/3
            yinc = (offset*(-skater.speed)/100)
            skater.y += yinc
            skater.speed -= (skater.angle/100)
            skater.speed = skater.speed/1.005
    else:
        skater.image = "fallen"+skater.direction

def on_key_down(key):
    global score
    if key.name == "UP":
        if (skater.angle > 75 and skater.speed > 0) or (skater.angle < -75 and skater.speed < 0):
            skater.speed = 0
            skater.switch = 60
            score += 1000
    if key.name == "SPACE" and skater.y > 600:
        skater.direction = "l"
        skater.speed = 0
        skater.pos = (720,230)
        skater.image = "skaterl"
        skater.angle = 0
        skater.switch = 15
        score = 0
        
def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

pgzrun.go()
