WIDTH = 800
HEIGHT = 800

crosshair = Actor('crosshair')

# creating a new enemy
def newEnemy(pos):
    e = Actor('enemy', pos=pos)
    e.hit = False
    e.timer = 50
    e.hits = []
    return e

# creating a bullet that has hit an enemy
def newHit(pos):
    h = Actor('bullet', pos=pos)
    return h

# create 3 enemies at various positions
enemies = []
for p in [(0,200),(-200,400),(-400,600)]:
    enemies.append(newEnemy(p))

numberofbullets = 8
MAXBULLETS = 8

def on_mouse_move(pos, rel, buttons):
    crosshair.pos = pos

def on_mouse_down(pos,button):
    global numberofbullets
    # left to fire
    if button == mouse.LEFT and numberofbullets > 0:
        # check whether an enemy has been hit
        for e in enemies:
            if crosshair.colliderect(e):
                # if hit, add position to 'hits' list
                e.hits.append(newHit(pos))
                e.hit = True
                break
        numberofbullets = max(0, numberofbullets -1)
    # right to reload
    if button == mouse.RIGHT:
        numberofbullets = MAXBULLETS

def update():
    for e in enemies:
        # hit enemies continue to display
        # until timer reaches 0
        if e.hit:
            e.timer -= 1
            if e.timer <= 0:
                enemies.remove(e)
        # move enemies if not hit
        else:
            e.x = min (e.x+2, WIDTH)

def draw():
    screen.clear()
    # draw enemies
    for e in enemies:
        e.draw()
        # draw enemy hits
        for h in e.hits:
            h.draw()
    crosshair.draw()
    # draw remaining bullets
    for n in range(numberofbullets):
        screen.blit('bullet',(10+(n*30),10))