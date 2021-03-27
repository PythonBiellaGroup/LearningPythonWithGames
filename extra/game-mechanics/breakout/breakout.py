# https://github.com/Wireframe-Magazine/Wireframe-11
# Wireframe #11: Breakout's brick-breaking action

import pgzrun
import random
import colorsys
from math import copysign

WIDTH = 600
HEIGHT = 800
BALL_SIZE = 10
MARGIN = 50

BRICKS_X = 10
BRICKS_Y = 5
BRICK_W = (WIDTH - 2 * MARGIN) // BRICKS_X
BRICK_H = 25

ball = ZRect(WIDTH / 2, HEIGHT / 2, BALL_SIZE, BALL_SIZE)
bat = ZRect(WIDTH / 2, HEIGHT - 50, 80, 12)

bricks = []


def hsv_color(h, s, v):
    """Return an RGB color from HSV."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return r * 255, g * 255, b * 255


def reset():
    """Reset bricks and ball."""
    # First, let's do bricks
    del bricks[:]
    for x in range(BRICKS_X):
        for y in range(BRICKS_Y):
            brick = ZRect(
                (x * BRICK_W + MARGIN, y * BRICK_H + MARGIN),
                (BRICK_W - 1, BRICK_H - 1)
            )
            hue = (x + y) / BRICKS_X
            saturation = (y / BRICKS_Y) * 0.5 + 0.5
            brick.highlight = hsv_color(hue, saturation * 0.7, 1.0)
            brick.color = hsv_color(hue, saturation, 0.8)
            bricks.append(brick)

    # Now reset the ball
    ball.center = (WIDTH / 2, HEIGHT / 2)
    ball.vel = (random.uniform(-200, 200), 400)


# Reset bricks and ball at start
reset()


def draw():
    screen.clear()
    for brick in bricks:
        screen.draw.filled_rect(brick, brick.color)
        screen.draw.line(brick.bottomleft, brick.topleft, brick.highlight)
        screen.draw.line(brick.topleft, brick.topright, brick.highlight)

    screen.draw.filled_rect(bat, 'pink')
    screen.draw.filled_circle(ball.center, BALL_SIZE // 2, 'white')


def update():
    # When you have fast moving objects, like the ball, a good trick
    # is to run the update step several times per frame with tiny time steps.
    # This makes it more likely that collisions will be handled correctly.
    for _ in range(3):
        update_step(1 / 180)


def update_step(dt):
    x, y = ball.center
    vx, vy = ball.vel

    if ball.top > HEIGHT:
        reset()
        return

    # Update ball based on previous velocity
    x += vx * dt
    y += vy * dt
    ball.center = (x, y)

    # Check for and resolve collisions
    if ball.left < 0:
        vx = abs(vx)
        ball.left = -ball.left
    elif ball.right > WIDTH:
        vx = -abs(vx)
        ball.right -= 2 * (ball.right - WIDTH)

    if ball.top < 0:
        vy = abs(vy)
        ball.top *= -1

    if ball.colliderect(bat):
        vy = -abs(vy)
        # randomise the x velocity but keep the sign
        vx = copysign(random.uniform(50, 300), vx)
    else:
        # Find first collision
        idx = ball.collidelist(bricks)
        if idx != -1:
            brick = bricks[idx]
            # Work out what side we collided on
            dx = (ball.centerx - brick.centerx) / BRICK_W
            dy = (ball.centery - brick.centery) / BRICK_H
            if abs(dx) > abs(dy):
                vx = copysign(abs(vx), dx)
            else:
                vy = copysign(abs(vy), dy)
            del bricks[idx]

    # Write back updated position and velocity
    ball.center = (x, y)
    ball.vel = (vx, vy)


def on_mouse_move(pos):
    x, y = pos
    bat.centerx = x
    if bat.left < 0:
        bat.left = 0
    elif bat.right > WIDTH:
        bat.right = WIDTH

pgzrun.go()        