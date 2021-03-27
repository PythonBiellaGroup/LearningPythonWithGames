# Time Pilot
import pgzrun
from random import randint
import math

gameState = 0
ship = Actor('ship0',(400,300))
biplane = Actor('biplane0',(200,0))
explosion = Actor('explosion1',(0,0))
ship.dir = ship.canfire = biplane.dir = explosion.frame = 0
clouds = []
dirs = [[0,1],[-0.7,0.7],[-1,0],[-0.7,-0.7],[0,-1],[0.7,-0.7],[1,0],[0.7,0.7]]
for c in range(0, 20):
    clouds.append(Actor('cloud'+str(randint(1,3)), center=(randint(0,1000)-100, randint(0,800)-100)))
    clouds[c].level = (c+5)/8
bullets = []

def draw():
    screen.fill((0,150,255))
    for b in range(len(bullets)):
        bullets[b].draw()
    ship.draw()
    biplane.draw()
    for c in range(0, 20):
        clouds[c].draw()
    if explosion.frame > 0 and explosion.frame < 10:
        explosion.draw()
    
    
def update():
    global gameState
    if gameState == 0:
        if keyboard.left:
            ship.dir -= 0.1
            if ship.dir < 0: ship.dir = 7.9
        if keyboard.right:
            ship.dir += 0.1
            if ship.dir > 7.9: ship.dir = 0
        if keyboard.space:
            if ship.canfire <= 0: fireBullet()
        ship.canfire -= 1
        ship.image = "ship"+str(int(ship.dir))
        myradians = math.atan2(ship.x-biplane.x, ship.y-biplane.y)
        mydegrees = math.degrees(myradians)
        biplane.dir = (180-mydegrees)/45

        biplane.x += (dirs[int(ship.dir)][0]) - ((dirs[int(biplane.dir)][0])/2)
        biplane.y += (dirs[int(ship.dir)][1]) - ((dirs[int(biplane.dir)][1])/2)
        biplane.image = "biplane"+str(int(biplane.dir))
        if explosion.frame > 0:
            explosion.frame += 1
            explosion.x += (dirs[int(ship.dir)][0])
            explosion.y += (dirs[int(ship.dir)][1])
            if explosion.frame < 10 : explosion.image = "explosion"+str(math.ceil(explosion.frame/3))
        for c in range(0, 20):
            clouds[c].x += dirs[int(ship.dir)][0]*clouds[c].level
            if clouds[c].x > 900: clouds[c].x = -100
            if clouds[c].x < -100: clouds[c].x = 900
            clouds[c].y += dirs[int(ship.dir)][1]*clouds[c].level
            if clouds[c].y > 700: clouds[c].y = -100
            if clouds[c].y < -100: clouds[c].y = 700
        for b in range(len(bullets)):
            bullets[b].x -= (dirs[bullets[b].dir][0]*5) + (dirs[int(ship.dir)][0])
            bullets[b].y -= (dirs[bullets[b].dir][1]*5) + (dirs[int(ship.dir)][1])
            if biplane.collidepoint(bullets[b].pos) == True:
                byplaneHit()
            
def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

def fireBullet():
    bullets.append(Actor('bullet', center=(400, 300)))
    bullets[len(bullets)-1].dir = int(ship.dir)
    ship.canfire = 5
    
def byplaneHit():
    explosion.frame = 1
    explosion.pos = biplane.pos
    biplane.pos = (randint(0,800),0)
    
pgzrun.go()
