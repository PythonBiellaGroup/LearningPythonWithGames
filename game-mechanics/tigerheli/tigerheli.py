# Tiger-Heli

WIDTH = 600
HEIGHT = 800
backgroundY = count = 0
heli = Actor('heli1', center=(300, 650))
bombActive = False
bombs = []
bombDirs = [(0,1),(1,1),(1,0),(0,0),(0,-1),(-1,-1),(-1,0),(-1,1),(1,-1),(-0.5,0),(0.5,0.5),(-0.5,-0.5),(0.5,-0.5),(0,-0.5),(-0.5,0.5),(-0.5,1),(1,-0.5),(-1,-0.5),(0.5,-1)]
for b in range(0, 18):
    bombs.append(Actor('bomb1', center=(0,0)))
    bombs[b].frame = 0
tankLocations = [(500,-250),(100,-250),(300,-500)]
tanks = []
for t in range(0,3):
    tanks.append(Actor('tank0', center=(tankLocations[t][0],tankLocations[t][1])))
    tanks[t].frame = 0

def draw():
    screen.blit('background',(0,backgroundY))
    screen.blit('background',(0,backgroundY-1400))
    screen.blit("helishadow"+str(count%2 + 1),(heli.x+10,heli.y+10))
    for t in range(0,3):
        if tanks[t].frame < 10:
            tanks[t].draw()
    if bombActive == True:
        for b in range(0, 18):
            bombs[b].draw()
    heli.draw()
    
def update():
    global backgroundY, count,bombActive
    backgroundY += 1
    if backgroundY > 1400: backgroundY = 0
    heli.image = "heli"+str(count%2 + 1)
    if keyboard.left and heli.x > 50 : heli.x -= 2
    if keyboard.right and heli.x < 550 : heli.x += 2
    if keyboard.up and heli.y > 50 : heli.y -= 2
    if keyboard.down and heli.y < 650 : heli.y += 2
    if keyboard.space : fireBomb()
    for t in range(0,3):
        tanks[t].y = (tankLocations[t][1] + backgroundY)
        if tanks[t].y > 850: tanks[t].frame = 0
        if tanks[t].frame > 0 and tanks[t].frame < 10 : tanks[t].frame += 0.2
        tanks[t].image = "tank"+str(int(tanks[t].frame))
    if bombActive == True:
        for b in range(0, 18):
            bombs[b].y += 1
            bombs[b].x += bombDirs[b][0]*5
            bombs[b].y += bombDirs[b][1]*5
            bombs[b].frame += 1
            if bombs[b].frame > 30:
                bombs[b].image = "bomb"+str(bombs[b].frame-30)
                for t in range(0,3):
                    if bombs[b].collidepoint(tanks[t].pos) and tanks[t].frame == 0:
                        tanks[t].frame = 1
                        sounds.explosion.play()
            if bombs[b].frame == 40:
                bombActive = False
    count += 1

def fireBomb():
    global bombActive
    if bombActive == False :
        bombActive = True
        sounds.launch.play()
        for b in range(0, 18):
            bombs[b].frame = 1
            bombs[b].pos = heli.pos
            bombs[b].image = "bomb1"
