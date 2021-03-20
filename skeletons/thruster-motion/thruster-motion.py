# TODO Splittare l'immagine, premere LEFT/RIGHT per girare, UP per accelerare
# https://github.com/Wireframe-Magazine/Wireframe-4
# Wireframe #4: Asteroids' thruster motion, pages 32-35

import math

# set screen width and height
WIDTH = 800
HEIGHT = 800

# create a new spaceship, using the 'spaceship.png' image
spaceship = Actor('spaceship')
# place the spaceship in the centre of the screen, facing right
spaceship.center = (WIDTH/2, HEIGHT/2)
spaceship.angle = 0
# set an acceleration for the spaceship
spaceship.ACCELERATION = 0.02
# initially the spaceship is stationary
spaceship.x_speed = 0
spaceship.y_speed = 0

def update():
    # save the spaceship's current angle,
    # as changing the actor's image resets the angle to 0
    new_angle = spaceship.angle

    # rotate left on left arrow press
    if keyboard.left:
        new_angle += 2

    # rotate right on right arrow press
    if keyboard.right:
        new_angle -= 2

    # accelerate forwards on up arrow press
    # and change displayed image
    if keyboard.up:
        spaceship.image = 'spaceship_thrust'
        spaceship.x_speed += math.cos(math.radians(new_angle)) * spaceship.ACCELERATION
        spaceship.y_speed += math.sin(math.radians(new_angle)) * spaceship.ACCELERATION
    else:
        spaceship.image = 'spaceship'

    # set the new angle
    spaceship.angle = new_angle

    # use the x and y speed to update the spaceship position
    # subtract the y speed as coordinates go from top to bottom
    spaceship.x += spaceship.x_speed
    spaceship.y -= spaceship.y_speed

def draw():
    screen.clear()
    spaceship.draw()
