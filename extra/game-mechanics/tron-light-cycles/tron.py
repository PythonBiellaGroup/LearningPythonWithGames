# Tron
import pgzrun

speed = 3
dirs = [0,90,180,270]
moves = [(0,-1),(-1,0),(0,1),(1,0)]

def draw():
    screen.blit("background", (0, 0))
    for x in range(0, 79):
        for y in range(0, 59):
            if matrix[x][y] > 0:
                matrix[x][y] += 1
                screen.blit("dot",((x*10)-5,(y*10)-5))
    bike.draw()
    screen.draw.text("SCORE : "+ str(score), center=(400, 588), owidth=0.5, ocolor=(0,255,255), color=(0,0,255) , fontsize=28)
    
def update():
    global matrix,gamestate,score
    if gamestate == 0:
        bike.angle = dirs[bike.direction]
        bike.x += moves[bike.direction][0]*speed
        bike.y += moves[bike.direction][1]*speed
        score += 10
        if matrix[int(bike.x/10)][int(bike.y/10)] < 15 :
            matrix[int(bike.x/10)][int(bike.y/10)] += 1
        else:
            gamestate = 1
        if bike.x < 60 or bike.x > 750 or bike.y < 110 or bike.y > 525:
            gamestate = 1
    else:
        if gamestate < 18:
            bike.image = "bike"+str(int(gamestate/2))
            bike.angle = dirs[bike.direction]
            gamestate += 1
    
def on_key_down(key):
    if key == keys.LEFT:
        bike.direction += 1
        snapBike()
        if bike.direction == 4 : bike.direction = 0
    if key == keys.RIGHT:
        bike.direction -= 1
        snapBike()
        if bike.direction == -1 : bike.direction = 3
    if key == keys.SPACE and gamestate == 18:
        init()
    
def snapBike():
    bike.x = int(bike.x/10)*10
    bike.y = int(bike.y/10)*10
    
def init():
    global bike,matrix,gamestate,score
    bike = Actor('bike1', center=(400, 500))
    bike.direction = 0
    matrix = [[0 for y in range(60)] for x in range(80)]
    gamestate = score = 0
    
init()
    
pgzrun.go()
