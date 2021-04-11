import pgzrun
from random import randint
import math

WIDTH = 1000
HEIGHT = 700
TITLE = "Stelle"
CENTRO_X = WIDTH/2
CENTRO_Y = HEIGHT/2
CENTRO = (CENTRO_X, CENTRO_Y)
VEL_RAZZO = 5
DISTANZA_DI_COLLISIONE = 50

happy_star_list = []
hot_star_list = []
score = 0

razzo = Actor("razzo", pos=CENTRO)
razzo.images = ["explosion1","explosion2","explosion3","explosion4"]
razzo.state = 0
razzo.lives = 3
razzo.hit = False

def draw():
    screen.clear()
    screen.blit("background", (0,0))
    draw_score()
    draw_life()
    for happy_star in happy_star_list:
        happy_star.draw()
    for hot_star in hot_star_list:
        hot_star.draw()
    razzo.draw()

    if razzo.hit:
        if razzo.lives > 0:
            screen.draw.text(
                "YOU ARE HIT!\nPress ENTER to re-spawn",
                center=CENTRO, owidth = 0.5, ocolor = "white",
                color = (255,64,0), fontsize=60
            )
        else:
            screen.draw.text(
                "GAME OVER!\nPress ENTER to continue playing",
                center = CENTRO, owidth=0.5, ocolor="white",
                color=(255,64,0), fontsize=60
            )


def update():
    global score

    check_keys()
    update_star()
    check_happy_star_collision()
    check_hot_star_collision()

    if razzo.hit:
        rocket_explode()
        if keyboard.RETURN:
            if razzo.lives is 0:
                razzo.lives = 3
                score = 0
            init_game()

def draw_life():
    for lv in range(razzo.lives):
        screen.blit("life", (10+(lv*32),10))

def draw_score():
    global score
    screen.draw.text(
        str(score),
        pos=(CENTRO_X,10), color="red",
        fontsize=60, owidth=0.5, ocolor="black",
        shadow=(1,1), scolor="black"
    )    

def check_keys():
    if not razzo.hit:
        if keyboard.right and razzo.x < WIDTH:
            razzo.angle = -90
            razzo.x += VEL_RAZZO
        elif keyboard.left and razzo.x > 0:
            razzo.angle = 90
            razzo.x -= VEL_RAZZO
        elif keyboard.up and razzo.y > 0:
            razzo.angle = 0
            razzo.y -= VEL_RAZZO
        elif keyboard.down and razzo.y < HEIGHT:
            razzo.angle = 180
            razzo.y += VEL_RAZZO

def add_star():
    global happy_star_list
    if not razzo.hit:
        new_happy_star = Actor("stella")
        new_happy_star.pos = randint(50, WIDTH-50), randint(50, HEIGHT-50)
        happy_star_list.append(new_happy_star)

def update_star():
    if not razzo.hit:
        for hot_star in hot_star_list:
            hot_star.x += hot_star.vx 
            hot_star.y += hot_star.vy

            if hot_star.left < 0:
                hot_star.vx = -hot_star.vx
            if hot_star.right > WIDTH:
                hot_star.vx = -hot_star.vx
            if hot_star.top < 0:
                hot_star.vy = -hot_star.vy
            if hot_star.bottom > HEIGHT:
                hot_star.vy = -hot_star.vy

def mutate_star():
    global happy_star_list, hot_star_list
    if not razzo.hit and happy_star_list:
        rand_star = randint(0, len(happy_star_list)-1)
        hot_star_pos_x = happy_star_list[rand_star].x 
        hot_star_pos_y = happy_star_list[rand_star].y 

        del happy_star_list[rand_star]

        hot_star = Actor("hot-star")
        hot_star.pos = hot_star_pos_x, hot_star_pos_y
        hot_star.vx = star_velocity()
        hot_star.vy = star_velocity()
        hot_star_list.append(hot_star)

def star_velocity():
    random_dir = randint(0,1)
    random_velocity = randint(1,2)
    if random_dir is 0:
        return -random_velocity
    else:
        return random_velocity

def check_happy_star_collision():
    global score, happy_star_list
    if not razzo.hit:
        for index in range(0, len(happy_star_list)-1):
            if happy_star_list[index].colliderect(razzo):
                score += 1
                sounds.eep.play()
                del happy_star_list[index]

def check_hot_star_collision():
    global hot_star_list
    if not razzo.hit:
        for index in range(0, len(hot_star_list)-1):
            distance = razzo.distance_to(hot_star_list[index])
            if not razzo.hit and distance < DISTANZA_DI_COLLISIONE:
                razzo.lives -= 1
                del hot_star_list[index]
                razzo.hit = True

def rocket_explode():
    if razzo.hit:
        if razzo.state is 0:
            sounds.explosion.play()
        
        if razzo.state < 90:
            razzo.state += 1
            razzo.image = razzo.images[math.floor(razzo.state/30)]

def init_game():
    global happy_star_list, hot_star_list
    happy_star_list = []
    hot_star_list = []
    razzo.image = "razzo"
    razzo.pos = CENTRO
    razzo.state = 0
    razzo.hit = False


clock.schedule_interval(add_star, 2)
clock.schedule_interval(mutate_star, 5)
pgzrun.go()