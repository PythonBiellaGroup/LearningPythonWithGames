# Pygame Stardust
import pgzrun
import math

ship = Actor('ship', center=(400, 300))
count = gameover = 0
asteroids = []
bullets = []
for a in range(0, 4):
    asteroids.append(Actor('ast1_'+str((a+1)*3), center=(100+(a*200),100+((a%2)*400))))
    asteroids[a].angle = (80*a) + 20
    asteroids[a].status = 0

def draw():
    screen.blit("background", (0, 0))
    for b in range(0, len(bullets)):
        bullets[b].draw()
    drawAsteroids()
    if gameover != 1 or (gameover == 1 and count%2 == 0): ship.draw()
    if gameover == 1 : screen.draw.text("YOU CLEARED ALL THE ASTEROIDS", center = (400, 300), owidth=0.5, ocolor=(255,255,0), color=(255,0,0) , fontsize=50)
    
def update():
    global count
    count += 1
    if gameover == 0:
        if keyboard.left : ship.angle += 2
        if keyboard.right : ship.angle -= 2
        updateBullets()
        updateAsteroids()

def on_key_down(key):
    if gameover == 0:
        if key.name == "SPACE": makeBullet()

def drawAsteroids():
    for a in range(0, len(asteroids)):
        if asteroids[a].status == 0: asteroids[a].draw()

def updateAsteroids():
    global gameover
    asteroidsLeft = False
    for a in range(0, len(asteroids)):
        if asteroids[a].status == 0 : asteroidsLeft = True
        i = int(asteroids[a].image[5:])
        if count%5 == 0: i += 1
        if i > 12: i = 1
        imagebase = asteroids[a].image[0:5]
        angle = asteroids[a].angle
        asteroids[a].x += math.sin(math.radians(angle))
        asteroids[a].y += math.cos(math.radians(angle))
        if asteroids[a].x > 850 : asteroids[a].x -= 850
        if asteroids[a].x < -50 : asteroids[a].x += 850
        if asteroids[a].y > 650 : asteroids[a].y -= 650
        if asteroids[a].y < -50 : asteroids[a].y += 650
        asteroids[a].image = imagebase + str(i)
        asteroids[a].angle = angle
    if asteroidsLeft == False : gameover = 1

def updateBullets():
    global bullets
    bulletsTemp = []
    tb = 0
    for b in range(0, len(bullets)):
        if isOnScreen(bullets[b]) and not hitAsteroid(bullets[b]) :
            bulletsTemp.append(Actor('bullet'))
            bulletsTemp[tb].x = bullets[b].x + 5 * math.sin(math.radians(bullets[b].angle))
            bulletsTemp[tb].y = bullets[b].y + 5 * math.cos(math.radians(bullets[b].angle))
            bulletsTemp[tb].angle = bullets[b].angle
            tb += 1
    bullets = bulletsTemp
    
def hitAsteroid(b):
    for a in range(0, len(asteroids)):
        if asteroids[a].collidepoint(b.pos) and asteroids[a].status == 0:
            breakAsteroid(a,b.angle)
            return True
    return False

def breakAsteroid(a,angle):
    acount = len(asteroids)
    anum = int(asteroids[a].image[3])
    if anum < 3:
        anum += 1
        asteroids.append(Actor('ast'+str(anum)+'_1', center=(asteroids[a].pos)))
        asteroids[acount].angle = (angle + 90) % 360
        asteroids[acount].status = 0
        acount += 1
        asteroids.append(Actor('ast'+str(anum)+'_6', center=(asteroids[a].pos)))
        asteroids[acount].angle = (angle - 90) % 360
        asteroids[acount].status = 0
    asteroids[a].status = 1

def makeBullet():
    a = len(bullets)
    bullets.append(Actor('bullet', center=(400,300)))
    bullets[a].angle = (ship.angle + 180) % 360
    
def isOnScreen(b):
    if b.x > 0 and b.x < 800 and b.y >0 and b.y < 600 :
        return True
    else :
        return False
        
pgzrun.go()
