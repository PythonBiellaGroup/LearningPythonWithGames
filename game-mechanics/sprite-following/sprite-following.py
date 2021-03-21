# https://github.com/Wireframe-Magazine/Wireframe16
# Gradius' ship-following Options, pages 40-41
import pgzrun
# set screen width and height
WIDTH = 800
HEIGHT = 800

# create spaceship and a list of 3 powerups
spaceship = Actor('spaceship',pos=(400,400))
spaceship.speed = 4
powerups = [Actor('powerup') for p in range(3)]

# create a list of previous positions
# initially containing values to the left of the spaceship
previouspositions = [(spaceship.x - i*spaceship.speed,spaceship.y) for i in range(100)]

def update():

    global previouspositions

    # store spaceship previous position
    previousposition = (spaceship.x,spaceship.y)

    # use arrow keys to move the spaceship
    if keyboard.up:
        spaceship.y -= spaceship.speed
    if keyboard.down:
        spaceship.y += spaceship.speed
    if keyboard.left:
        spaceship.x -= spaceship.speed
    if keyboard.right:
        spaceship.x += spaceship.speed

    # add new position to list if the spaceship has moved
    # and ensure the list contains at most 100 positions
    if previousposition != spaceship.pos:
        previouspositions = [(spaceship.x,spaceship.y)] + previouspositions[:99]

    # set the new position of each powerup
    for i,p in enumerate(powerups):
        newposition = previouspositions[(i+1)*20]
        p.pos = (newposition[0],newposition[1])

def draw():
    screen.clear()
    spaceship.draw()
    for p in powerups:
        p.draw()

pgzrun.go()