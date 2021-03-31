import pgzrun
from random import randint

TITLE = "Flappy Bird"
WIDTH = 800
HEIGHT = 700

GAP = 100 # change to 100 instead of 130
FLAP_STRENGTH = 5
SPEED = 5  # change to 4 instead of 2
GRAVITY = 0.5  # change to 0.5 instead of 0.3
PIPE_DIST = 400

bird = Actor("bird0", (80,300))
bird.dead = False
bird.hit = False
bird.score = 0
bird.vy = 0

pipe_top1 = Actor("up", anchor=("left", "bottom"))
pipe_bottom1 = Actor("bottom", anchor=("left", "top"))

pipe_top2 = Actor("up", anchor=("left", "bottom"))
pipe_bottom2 = Actor("bottom", anchor=("left", "top"))

storage = {"highscore":0}
game_start = False

def draw():
    screen.blit("background", (0,0))
    pipe_top1.draw()
    pipe_bottom1.draw()
    pipe_top2.draw()
    pipe_bottom2.draw()
    bird.draw()

    screen.draw.text(
        str(bird.score),
        color = "red",
        midtop = (WIDTH/2, 10),
        fontsize = 70,
        shadow = (1,1)
    )
    screen.draw.text(
        "Best: " + str(storage["highscore"]),
        color = (200, 170, 0),
        midbottom = (WIDTH/2, HEIGHT - 10),
        fontsize = 30,
        shadow = (1,1)
    )
    if not game_start:
        screen.draw.text(
            "Press any key to start", color = "yellow",
            center = (WIDTH/2, HEIGHT/2),
            fontsize = 60, owidth = 0.5, ocolor = "black"
        )

def set_pipe():
    pipe_gap_y1 = randint(200, HEIGHT-200)
    pipe_top1.pos = (WIDTH/2, pipe_gap_y1 - GAP/2)
    pipe_bottom1.pos = (WIDTH/2, pipe_gap_y1 + GAP/2)
    
    pipe_gap_y2 = randint(200, HEIGHT-200)
    pipe_top2.pos = (WIDTH/2 + PIPE_DIST, pipe_gap_y2 - GAP/2)
    pipe_bottom2.pos = (WIDTH/2 + PIPE_DIST, pipe_gap_y2 + GAP/2)

def reset_pipe():
    if pipe_top1.right < 0:
        pipe_gap_y1 = randint(200, HEIGHT-200)
        pipe_top1.pos = (WIDTH, pipe_gap_y1 - GAP/2)
        pipe_bottom1.pos = (WIDTH, pipe_gap_y1 + GAP/2)

    if pipe_top2.right < 0:
        pipe_gap_y2 = randint(200, HEIGHT-200)
        pipe_top2.pos = (WIDTH, pipe_gap_y2 - GAP/2)
        pipe_bottom2.pos = (WIDTH, pipe_gap_y2 + GAP/2)


def update_pipe():
    global storage
    pipe_top1.left -= SPEED
    pipe_bottom1.left -= SPEED
    pipe_top2.left -= SPEED
    pipe_bottom2.left -= SPEED

    if pipe_top1.right < 0 or pipe_top2.right < 0:
        if not bird.dead:
            bird.score += 1
        reset_pipe()
    
    if bird.score > storage["highscore"]:
        storage["highscore"] = bird.score


def update_bird():
    global game_start
    uy = bird.vy
    bird.vy += GRAVITY
    bird.y += (uy + bird.vy)/2
    bird.x = 80

    if not bird.dead:
        if bird.vy < -3:
            bird.image = "bird2"
        else:
            bird.image = "bird1"

    if bird.colliderect(pipe_top1) or bird.colliderect(pipe_bottom1) or \
        bird.colliderect(pipe_top2) or bird.colliderect(pipe_bottom2):
        bird.dead = True
        if bird.dead and not bird.hit:
            sounds.bang.play()
            bird.image = "birdhit"
            bird.hit = True
            clock.schedule(set_bird_dead, 0.1)

    if not 0 < bird.y < 740:
        bird.image = "bird0"
        bird.y = 200
        bird.dead = False
        bird.hit = False
        bird.score = 0
        bird.vy = 0
        set_pipe()
        game_start = False
    

def set_bird_dead():
    if bird.dead:
        bird.image = "birddead"

def on_key_down():
    global game_start
    game_start = True

    if not bird.dead:
        bird.vy = -FLAP_STRENGTH

def update():
    if game_start:
        update_pipe()
        update_bird()

set_pipe()
music.play("electroman")
pgzrun.go()