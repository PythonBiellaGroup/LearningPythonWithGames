# Artillery
from random import randint
from pygame import Surface, image
from pygame.locals import *
import math

landSurface = Surface((800,600),SRCALPHA)
landSurface.blit(image.load('images/landscape.png') ,(0,0))
gun1 = {"name": "Player 1", "actor": Actor('gunbody1', center=(700, 300)), "turret": Actor('gunbarrel1', center=(695, 280)), "angle": 30, "multiplier": 1, "color": (255,0,0)}
gun2 = {"name": "Player 2", "actor": Actor('gunbody2', center=(200, 400)), "turret": Actor('gunbarrel2', center=(210, 380)), "angle": 30, "multiplier": -1, "color": (0,0,255)}
bullet = {"active": False, "actor": Actor('bullet', center=(0, 0)), "angle": 0, "speed": 0, "count":0}
bang = {"actor": Actor('expl1', center=(0, 0)), "frame": 0}
activePlayer = gun1
gameState = 0

def draw():
    screen.blit('background',(0,0))
    screen.blit(landSurface, (0, 0))
    if bullet["active"] == True: bullet["actor"].draw()
    if gameState != 1:
        gun1["turret"].draw()
        gun1["actor"].draw()
    if gameState != 2:
        gun2["turret"].draw()
        gun2["actor"].draw()
    if gameState == 0: drawText(activePlayer["name"], activePlayer["color"])
    if gameState == 1: drawText("Player 2 Wins!", (0,255,0))
    if gameState == 2: drawText("Player 1 Wins!", (0,255,0))
    if bang["frame"] != 0: bang["actor"].draw()
    
def update():
    global activePlayer, gameState
    if gameState == 0:
        if keyboard.space and bullet["active"] == False: fireBullet()
        if keyboard.up: activePlayer["angle"] = limit(activePlayer["angle"]-1,5,90)
        if keyboard.down: activePlayer["angle"] = limit(activePlayer["angle"]+1,5,90)
        gun1["turret"].angle = gun1["angle"]
        gun2["turret"].angle = -gun2["angle"]
        if bullet["active"] == True:
            bullet["count"] += 1
            bullet["speed"] = bullet["speed"]*0.991
            bullet["actor"].pos = getNewPos(90-bullet["angle"])
            if checkBullet(bullet["actor"].pos) :
                explosion(bullet["actor"].pos)
                bullet["active"] = False
                if activePlayer == gun1: activePlayer = gun2
                else: activePlayer = gun1
        if bullet["actor"].y > 600: bullet["active"] = False
    if bang["frame"] > 0:
        bang["actor"].image = "expl"+str(int(bang["frame"]))
        bang["frame"] += 0.2
        if bang["frame"] > 6: bang["frame"] = 0

def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

def fireBullet():
    bullet["active"] = True
    bullet["actor"].pos = activePlayer["turret"].pos
    bullet["angle"] = activePlayer["angle"] * activePlayer["multiplier"]
    bullet["speed"] = 10
    bullet["count"] = 0
    sounds.canon.play()

def getNewPos(angle):
    newX = bullet["actor"].x - (bullet["speed"]*math.cos(math.radians(angle)))
    newY = bullet["actor"].y - (bullet["speed"]*math.sin(math.radians(angle)))
    newY += 10-bullet["speed"]
    if bullet["count"] == 60: sounds.whine.play()
    return newX, newY

def checkBullet(pos):
    global gameState
    if pos[0]>0 and pos[0]<800 and pos[1]>0 and pos[1]<600:
        pixel = landSurface.get_at((int(pos[0]),int(pos[1])))
        if pixel[3] > 0: return True
    if gun1["actor"].collidepoint(pos):
        gameState = 1
        explosion(gun1["actor"].pos)
    if gun2["actor"].collidepoint(pos):
        gameState = 2
        explosion(gun2["actor"].pos)
    return False

def explosion(pos):
    x = int(pos[0])
    y = int(pos[1])
    sounds.explosion.play()
    bullet["active"] = False
    bang["actor"].pos = pos
    bang["frame"] = 1
    for c in range(2000):
        landSurface.set_at((x+randint(0,100)-50,y+randint(0,100)-50), (0,0,0,0))
        if c < 1500: landSurface.set_at((x+randint(0,50)-25,y+randint(0,40)-20), (0,0,0,0))
        if c < 1000: landSurface.set_at((x+randint(0,20)-10,y+randint(0,30)-15), (0,0,0,0))

def drawText(t,col):
    screen.draw.text(t, center = (400, 60), owidth=0.5, ocolor=(0,0,0), color=col , fontsize=40)
