# Pitfall!
import pgzrun
import math

rope = Actor('rope',midtop=(400,110), anchor=('center', 'top'))
harry = Actor('harry', (80,290))
harry.attached = False
harry.jump = 0
harry.onground = True
swing = -1

def draw():
    screen.blit("background", (0, 0))
    rope.draw()
    screen.blit("trees", (0, 0))
    harry.draw()
    screen.blit("platform", (0, 335))
    if harry.x > 550 and harry.y < 300: screen.draw.text("You made it over!", center=(400, 560), owidth=0.5, ocolor=(0,0,255), color=(255,255,255) , fontsize=40)
    
def update():
    global swing
    if rope.angle < -45:
        rope.angle = -45
        swing = 1
    if rope.angle > 45:
        rope.angle = 45
        swing = -1
    easing = (7-(math.sqrt(abs(rope.angle))))/3
    rope.angle += swing*easing
    oldx = harry.x
    harry.onground = False
    if (harry.y > 289 and harry.y < 293) or (harry.y > 468 and harry.y < 471): harry.onground = True
    if harry.x > 260 and harry.x < 540 and harry.y > 290 and harry.y < 470 : harry.onground = False
    if keyboard.right and (harry.onground == True or harry.jump > 0):
        harry.x += 2
        harry.image = "harry"+str(int((harry.x/20)%4))
    if keyboard.left and (harry.onground == True or harry.jump > 0):
        harry.x -= 2
        harry.image = "harry"+str(int((harry.x/20)%4))+"r"  
    if harry.jump > 0:
        harry.y -= 2
        harry.jump -=1
        harry.image = "harry0"
    else:
        if harry.y < 290 and harry.jump == 0 and harry.attached == False:
            harry.y += 2
        elif harry.jump == 0 and harry.x > 255 and harry.x < 540 and harry.y < 470:
            harry.y += 2
            
    if oldx == harry.x and harry.jump == 0 : harry.image = "harry"
    if harry.collidepoint (rope.left, rope.bottom) and rope.angle < 25:
        harry.attached = True
    if harry.attached == True:
        harry.image = "harryrope"
        harry.y = rope.bottom + 32
        harry.x = rope.x + (rope.angle * 2.7) - 12
    
def on_key_down(key):
    if key == keys.SPACE:
        if harry.y == 290 or harry.attached == True:
            harry.jump = 30
            harry.attached = False
        if harry.y > 450: harry.pos = (80,290)  
    
pgzrun.go()
