# https://github.com/Wireframe-Magazine/Wireframe17
# Wireframe #17: path-following Lemmings, pages 38-39
import pgzrun
from time import sleep
from PIL import Image

# screen size
HEIGHT=800
WIDTH=800

# level information
level_image = 'level'
BACKGROUND_COLOUR = (114,114,201,255)

# store the colour of each pixel in the level image
img = Image.open('images/level.png')
pixels = [[img.getpixel((x, y)) for y in range(HEIGHT)] for x in range(WIDTH)]

# a list to keep track of the lemmings
lemmings = []
max_lemmings = 10
start_position = (100,100)
# a timer and interval for creating new lemmings
timer = 0
interval = 10

# returns 'True' if the pixel specified is 'ground'
# (i.e. anything except BACKGROUND_COLOUR)
def groundatposition(pos):
    # ensure position contains integer values
    pos = (int(pos[0]),int(pos[1]))
    # get the colour from the 'pixels' list
    if pixels[pos[0]][pos[1]] != BACKGROUND_COLOUR:
        return True
    else:
        return False

class Lemming(Actor):
    def __init__(self, **kwargs):
        super().__init__(image='lemming', pos=start_position, anchor=('left','top'), **kwargs)
        self.direction = 1
        self.climbheight = 4
        self.width = 10
        self.height = 20
    # update a lemming's position in the level
    def update(self):
        # if there's no ground below a lemming (check both corners), it is falling
        bottomleft = groundatposition((self.pos[0], self.pos[1]+self.height))
        bottomright = groundatposition((self.pos[0]+(self.width-1), self.pos[1]+self.height))
        if not bottomleft and not bottomright:
            self.y += 1
        # if not falling, a lemming is walking
        else:
            height = 0
            found = False
            # find the height of the ground in front of a lemming
            # up to the maximum height a lemming can climb
            while (found == False) and (height <= self.climbheight):
                # the pixel 'in front' of a lemming will depend on
                # the direction it's traveling
                if self.direction == 1:
                    positioninfront = (self.pos[0]+self.width, self.pos[1]+(self.height-1)-height)
                else:
                    positioninfront = (self.pos[0]-1, self.pos[1]+(self.height-1)-height)
                if not groundatposition(positioninfront):
                    self.x += self.direction
                    # rise up to new ground level
                    self.y -= height
                    found = True

                height += 1
            # turn the lemming around if the ground in front
            # is too high to climb
            if not found:
                    self.direction *= -1

def update():
    global timer
    # increment the timer and create a new
    # lemming if the interval has passed
    timer += 0.1
    if timer > interval and len(lemmings) < max_lemmings:
        timer = 0
        lemmings.append(Lemming())
    # update each lemming's position in the level
    for i in lemmings:
        i.update()

def draw():
    screen.clear()
    # draw the level
    screen.blit(level_image,(0,0))
    # draw lemmings
    for i in lemmings:
        i.draw()

pgzrun.go()        