# Gauntlet
import pgzrun
import math
from pygame import image, Color, joystick

myChars = []
myDirs = [(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1)]
collisionmap = image.load('images/collisionmap.png')
joystick.init()
joyin0 = joyin1 = False
if(joystick.get_count() > 0):
    joyin0 = joystick.Joystick(0)
    joyin0.init()
if(joystick.get_count() > 1):
    joyin1 = joystick.Joystick(1)
    joyin1.init()
    
def makeChar(name,x,y):
    c = len(myChars)
    myChars.append(Actor(name+"_1",(x, y)))
    myChars[c].name = name
    myChars[c].frame = myChars[c].movex = myChars[c].movey = myChars[c].dir = 0

def draw():
    screen.blit("colourmap",(0,0))
    drawChars()
    
def drawChars():
    for c in range(len(myChars)):
        myChars[c].image = myChars[c].name+"_"+str(((myChars[c].dir*3)+1)+math.floor(myChars[c].frame/10))
        myChars[c].draw()
    
def update():
    checkInput()
    moveChars()

def checkInput():
    if keyboard.left: myChars[0].movex = -1
    if keyboard.right: myChars[0].movex = 1
    if keyboard.up: myChars[0].movey = -1
    if keyboard.down: myChars[0].movey = 1
    if keyboard.a: myChars[1].movex = -1
    if keyboard.d: myChars[1].movex = 1
    if keyboard.w: myChars[1].movey = -1
    if keyboard.s: myChars[1].movey = 1
    if joyin0:
        myChars[2].movex = round(joyin0.get_axis(0))
        myChars[2].movey = round(joyin0.get_axis(1))
    if joyin1:
        myChars[3].movex = round(joyin1.get_axis(0))
        myChars[3].movey = round(joyin1.get_axis(1))

def moveChars():
    for c in range(len(myChars)):
        getCharDir(myChars[c])
        if myChars[c].movex or myChars[c].movey:
            myChars[c].frame += 1
            if myChars[c].frame >= 30: myChars[c].frame = 0
            testmove = (int(myChars[c].x + (myChars[c].movex *20)),int(myChars[c].y + (myChars[c].movey *20)))
            if collisionmap.get_at(testmove) == Color('black') and collideChars(c,testmove) == False:
                myChars[c].x += myChars[c].movex
                myChars[c].y += myChars[c].movey
            myChars[c].movex = 0
            myChars[c].movey = 0

def getCharDir(ch):
    for d in range(len(myDirs)):
        if myDirs[d] == (ch.movex,ch.movey):
            ch.dir = d

def collideChars(c,xy):
    for ch in range(len(myChars)):
         if myChars[ch].collidepoint(xy) and ch != c:
             return True
    return False

makeChar("warrior",60,60)
makeChar("valkyrie",500,450)
makeChar("wizard",460,180)
makeChar("elf",100,400)
pgzrun.go()
