# https://github.com/Wireframe-Magazine/Wireframe-29
# Wireframe #29
# Recreate Flappy Bird's flight mechanic, pages 40-41, by Rik Cross

import pgzrun
from random import randint

# define screen size
WIDTH = 1000
HEIGHT = 600

# pipes are dark dreen, move 2 pixels per frame and
# have a gap of 150 pixels between top and bottom pipes
PIPE_COLOUR = (38,155,29)
PIPE_SPEED = 2
PIPE_GAP = 150

# vertical acceleration
GRAVITY = 0.2

# create top and bottom pipes, with a gap in between
top_pipes = [
    Rect((500,0),(50,200)),
    Rect((1000,0),(50,300))
]

bottom_pipes = [
    Rect((500,200 + PIPE_GAP), (50,HEIGHT - 200 - PIPE_GAP)),
    Rect((1000,300 + PIPE_GAP), (50,HEIGHT - 300 - PIPE_GAP))
]

player = Actor('player-down',(100,400))
# define initial and flap velocities
player.y_velocity = 0
player.flap_velocity = -5
player.score = 0

playing = True

def update():

    global playing
    if playing:

        # space key to flap
        if keyboard.space and player.y_velocity > 0:
            player.y_velocity = player.flap_velocity

        # acceleration is rate of change of velocity
        player.y_velocity += GRAVITY
        # velocity is rate of change of position
        player.y += player.y_velocity

        # player image depends on velocity
        if player.y_velocity > 0:
            player.image = 'player-down'
        else:
            player.image = 'player-up'

        # move pipes
        for pipe_list in top_pipes, bottom_pipes:
            for pipe in pipe_list:
                pipe.x -= PIPE_SPEED
                if pipe.x < -50:
                    pipe_list.remove(pipe)

        # create new pipes
        if len(top_pipes) < 2:
            player.score += 1
            # height of gap between new top and bottom pipes
            h = randint(150,350)
            top_pipes.append(Rect((1000,0),(50,h)))
            bottom_pipes.append(Rect((1000,h + PIPE_GAP),(50, HEIGHT - h - PIPE_GAP)))

        # game over if player collides with a pipe...
        for p in top_pipes + bottom_pipes:
            if player.colliderect(p):
                playing = False

        # ...or touches the ground
        if player.y > (HEIGHT - 20):
            playing = False

def draw():

    if playing:

        screen.clear()

        # draw background
        screen.blit('background', (0,0))

        # draw pipes
        for pipe in top_pipes + bottom_pipes:
            screen.draw.filled_rect(pipe, PIPE_COLOUR)

        # draw score
        screen.draw.text(str(player.score), (20, 20), fontsize=40, color="white")

        # draw player
        player.draw()

    else:

        screen.draw.text('Game Over!', (420, 200), fontsize=40, color="white")

pgzrun.go()        