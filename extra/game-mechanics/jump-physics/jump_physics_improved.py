# https://github.com/Wireframe-Magazine/Wireframe-7
# Wireframe #7: Super Mario-style jumping physics, pages 32-33
import pgzrun

# define screen size
WIDTH = 800
HEIGHT = 800
# define a colour
MAROON = 128,0,0
# vertical acceleration
GRAVITY = 0.2

# a list of platforms, each is a rectangle
# in the form ((x,y)(w,h))
platforms = [
    Rect((0,780),(800,20)),
    Rect((200,700),(100,100)),
    Rect((400,650),(100,20)),
    Rect((600,600),(100,20))
]

# create a player and define initial vertical velocity
player = Actor('player',(50,450), anchor=('left','top'))
player.w = 20
player.h = 20
# define initial and jump velocities
player.y_velocity = 0
player.jump_velocity = -7

def update():

    #
    # horizontal movement
    #

    # temporary variable to store new x position
    newx = player.x
    # calculate new horizontal position if
    # arrow keys are pressed
    if keyboard.left and player.x > 0:
        newx -= 2
    if keyboard.right and player.x < 780:
        newx += 2

    # create a rectangle for the new x position
    newpositionx = Rect((newx,player.y),(player.w,player.h))

    # check whether the new player position
    # collides with any platform
    x_collision = False
    for p in platforms:
        x_collision = newpositionx.colliderect(p) or x_collision

    # only allow the player to move if it
    # doesn't collide with any platforms
    if not x_collision:
        player.x = newx

    #
    # vertical movement
    #

    # temporary variable to store new y position
    newy = player.y

    # acceleration is rate of change of velocity
    player.y_velocity += GRAVITY
    # velocity is rate of change of position
    newy += player.y_velocity

    # create a rectangle for the new y position
    newplayerpositiony = Rect((player.x,newy),(player.w,player.h))

    # check whether the new player position
    # collides with any platform
    y_collision = False
    # also check whether the player is on the ground
    playeronground = False
    # distance from colliding platform (used if on ground)
    ydist = 0
    for p in platforms:
        y_collision = newplayerpositiony.colliderect(p) or y_collision
        # player collided with ground if player's y position is
        # lower than the y position of the platform
        if newplayerpositiony.colliderect(p) and (player.y < p.y):
            playeronground = True or playeronground
            # stick the player to the ground
            player.y = p.y - player.h

    # player no longer has vertical velocity
    # if colliding with a platform
    if y_collision:
        player.y_velocity = 0
    # only allow the player to move if it
    # doesn't collide with any platforms
    else:
        player.y = newy

    # pressing space sets a negative vertical velocity
    # only if player is on the ground
    if keyboard.space and playeronground:
        player.y_velocity = player.jump_velocity

def draw():

    screen.clear()

    # draw platforms
    for p in platforms:
        screen.draw.filled_rect(p,MAROON)

    # draw player
    player.draw()

pgzrun.go()