# Phoenix Mothership
WIDTH = 600
HEIGHT = 800

mothership = Actor('mothership', center=(300, 100))
bullet = Actor('bullet', center=(0, -10))
alien = Actor('aliendude', center=(300, 110))
ship = Actor('ship', center=(300, 700))
barShield = []
lowerShield = []
backY = count = mothership.frame = gameover = 0
for b in range(0, 14):
    barShield.append(Actor('bar1'+str(b%2), center=(310+((b-7)*20), 140)))
    lowerShield.append(Actor('shield1', center=(310+((b-7)*20), 160)))
    barShield[b].frame = lowerShield[b].frame = 1
for b in range(0, 10):
    lowerShield.append(Actor('shield1', center=(310+((b-5)*20), 180)))
    lowerShield[b + 14].frame = 1
for b in range(0, 4):
    lowerShield.append(Actor('shield1', center=(310+((b-2)*20), 200)))
    lowerShield[b + 24].frame = 1   

def draw():
    screen.blit("background", (0, 0))
    screen.blit("stars", (0, backY))
    screen.blit("stars", (0, backY-800))
    mothership.draw()
    if gameover != 1 or (gameover == 1 and count%2 == 0): alien.draw()
    for b in range(0, 28):
        if b < 14:
            if barShield[b].frame < 5:
                barShield[b].draw()
        if lowerShield[b].frame < 5:
            lowerShield[b].draw()
    bullet.draw()
    if gameover != 2 or (gameover == 2 and count%2 == 0): ship.draw()
    
def update():
    global backY, count, gameover
    count += 1
    if gameover == False:
        backY += 0.2
        if backY > 800: backY = 0
        mothership.y += 0.1
        mothership.frame = int(count/10)%14
        alien.y = mothership.y + 10
        for b in range(0, 28):
            if b < 14:
                x = (((mothership.frame+b)-7)*20)
                if x >= 140: x -= 280
                barShield[b].y += 0.1
                barShield[b].x = (mothership.x+10)+ x
                if barShield[b].frame < 5 and barShield[b].colliderect(bullet):
                    barShield[b].frame += 1
                    if barShield[b].frame < 5:
                        barShield[b].image = "bar"+str(barShield[b].frame)
                    bullet.y = -10
            lowerShield[b].y += 0.1
            if lowerShield[b].frame < 5 and lowerShield[b].colliderect(bullet):
                lowerShield[b].frame += 1
                if lowerShield[b].frame < 5:
                    lowerShield[b].image = "shield"+str(lowerShield[b].frame)
                bullet.y = -10
        if alien.colliderect(bullet): gameover = 1
        if ship.colliderect(mothership): gameover = 2
        if bullet.y > -10: bullet.y -= 5
        
def on_mouse_down(pos):
    if bullet.y < 0: bullet.pos = (ship.x,700)

def on_mouse_move(pos):
    ship.x = pos[0]
