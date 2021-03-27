# https://github.com/Wireframe-Magazine/Wireframe-30
# Wireframe #30
# Code a Boulder Dash mining game, pages 40-41, by Mark Vanstone
import pgzrun
import random

rockford = Actor('rockford-1', center=(60, 100))
gameState = count = 0
items = [[] for _ in range(14)]
gems = collected = 0
for r in range(0, 14):
    for c in range(0, 20):
        itype = "soil"
        if(r == 0 or r == 13 or c == 0 or c == 19): itype = "wall"
        elif random.randint(0, 4) == 1: itype = "rock"
        elif random.randint(0, 20) == 1:
            itype = "gem"
            gems += 1
        items[r].append(itype)
items[1][1] = "rockford"

def draw():
    screen.fill((0,0,0))
    if gems == collected: infoText("YOU COLLECTED ALL THE GEMS!")
    else: infoText("GEMS : "+ str(collected))
    for r in range(0, 14):
        for c in range(0, 20):
            if items[r][c] != "" and items[r][c] != "rockford":
                screen.blit(items[r][c], ((c*40), 40+(r*40)))
    if gameState == 0 or (gameState == 1 and count%4 == 0): rockford.draw()
    
def update():
    global count
    mx = my = 0
    if count%10 == 0:
        for r in range(13, -1, -1):
            for c in range(19, -1, -1):
                if items[r][c] == "rockford":
                    if keyboard.left: mx = -1
                    if keyboard.right: mx = 1
                    if keyboard.up: my = -1
                    if keyboard.down: my = 1
                if items[r][c] == "rock": testRock(r,c)
        rockford.image = "rockford"+str(mx)
        if gameState == 0: moveRockford(mx,my)
    count += 1

def infoText(t):
    screen.draw.text(t, center = (400, 20), owidth=0.5, ocolor=(255,255,255), color=(255,0,255) , fontsize=40)

def moveRockford(x,y):
    global collected
    rx, ry = int((rockford.x-20)/40), int((rockford.y-40)/40)
    if items[ry+y][rx+x] != "rock" and items[ry+y][rx+x] != "wall":
        if items[ry+y][rx+x] == "gem": collected +=1
        items[ry][rx], items[ry+y][rx+x] = "", "rockford"
        rockford.pos = (rockford.x + (x*40), rockford.y + (y*40))
    if items[ry+y][rx+x] == "rock" and y == 0:
        if items[ry][rx+(x*2)] == "":
            items[ry][rx], items[ry][rx+(x*2)], items[ry+y][rx+x] = "", "rock", "rockford"
            rockford.x += x*40

def testRock(r,c):
    if items[r+1][c] == "":
        moveRock(r,c,r+1,c)
    elif items[r+1][c] == "rock" and items[r+1][c-1] == "" and items[r][c-1] == "":
        moveRock(r,c,r+1,c-1)
    elif items[r+1][c] == "rock" and items[r+1][c+1] == "" and items[r][c+1] == "":
        moveRock(r,c,r+1,c+1)

def moveRock(r1,c1,r2,c2):
    global gameState
    items[r1][c1], items[r2][c2] = "", items[r1][c1]
    if items[r2+1][c2] == "rockford": gameState = 1
        
pgzrun.go()
