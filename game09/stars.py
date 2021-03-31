import pgzrun
from random import randint
import math

WIDTH = 1000
HEIGHT = 700
TITLE = "Star Collector"
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
CENTER = (CENTER_X, CENTER_Y)
ROCKET_SPEED = 5
COLLISION_DISTANCE = 50

happy_star_list = []
hot_star_list = []
score = 0

rocket = Actor("rocket", pos=CENTER)
rocket.images = ["explosion1","explosion2","explosion3","explosion4"]
rocket.state = 0
rocket.lives = 3
rocket.hit = False

def draw():
    screen.clear()
    screen.blit("background", (0,0))
    draw_score()
    draw_life()
    for happy_star in happy_star_list:
        happy_star.draw()
    for hot_star in hot_star_list:
        hot_star.draw()
    rocket.draw()

    if rocket.hit:
        if rocket.lives > 0:
            screen.draw.text(
                "YOU ARE HIT!\nPress ENTER to re-spawn",
                center=CENTER, owidth = 0.5, ocolor = "white",
                color = (255,64,0), fontsize=60
            )
        else:
            screen.draw.text(
                "GAME OVER!\nPress ENTER to continue playing",
                center = CENTER, owidth=0.5, ocolor="white",
                color=(255,64,0), fontsize=60
            )


def update():
    global score

    check_keys()
    update_star()
    check_happy_star_collision()
    check_hot_star_collision()

    if rocket.hit:
        rocket_explode()
        if keyboard.RETURN:
            if rocket.lives is 0:
                rocket.lives = 3
                score = 0
            init_game()

def draw_life():
    for lv in range(rocket.lives):
        screen.blit("life", (10+(lv*32),10))

def draw_score():
    global score
    screen.draw.text(
        str(score),
        pos=(CENTER_X,10), color="red",
        fontsize=60, owidth=0.5, ocolor="black",
        shadow=(1,1), scolor="black"
    )    

def check_keys():
    if not rocket.hit:
        if keyboard.right and rocket.x < WIDTH:
            rocket.angle = -90
            rocket.x += ROCKET_SPEED
        elif keyboard.left and rocket.x > 0:
            rocket.angle = 90
            rocket.x -= ROCKET_SPEED
        elif keyboard.up and rocket.y > 0:
            rocket.angle = 0
            rocket.y -= ROCKET_SPEED
        elif keyboard.down and rocket.y < HEIGHT:
            rocket.angle = 180
            rocket.y += ROCKET_SPEED

def add_star():
    global happy_star_list
    if not rocket.hit:
        new_happy_star = Actor("star")
        new_happy_star.pos = randint(50, WIDTH-50), randint(50, HEIGHT-50)
        happy_star_list.append(new_happy_star)

def update_star():
    if not rocket.hit:
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
    if not rocket.hit and happy_star_list:
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
    if not rocket.hit:
        for index in range(0, len(happy_star_list)-1):
            if happy_star_list[index].colliderect(rocket):
                score += 1
                sounds.eep.play()
                del happy_star_list[index]

def check_hot_star_collision():
    global hot_star_list
    if not rocket.hit:
        for index in range(0, len(hot_star_list)-1):
            distance = rocket.distance_to(hot_star_list[index])
            if not rocket.hit and distance < COLLISION_DISTANCE:
                rocket.lives -= 1
                del hot_star_list[index]
                rocket.hit = True

def rocket_explode():
    if rocket.hit:
        if rocket.state is 0:
            sounds.explosion.play()
        
        if rocket.state < 90:
            rocket.state += 1
            rocket.image = rocket.images[math.floor(rocket.state/30)]

def init_game():
    global happy_star_list, hot_star_list
    happy_star_list = []
    hot_star_list = []
    rocket.image = "rocket"
    rocket.pos = CENTER
    rocket.state = 0
    rocket.hit = False


clock.schedule_interval(add_star, 2)
clock.schedule_interval(mutate_star, 5)
pgzrun.go()