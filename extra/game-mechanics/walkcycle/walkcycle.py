# https://github.com/Wireframe-Magazine/Wireframe-14
# Wireframe #14: Create a Donkey Kong-style walk cycle, pages 40-41
import pgzrun
# the Player() class is a subclass of Actor()
class Player(Actor):
    def __init__(self, **kwargs):
        super().__init__(pos = (200,100), image='stand1', **kwargs)
        self.state = 'stand'
        self.animationdelay = 10
        self.animationtimer = 0
        # a list of image for each player state
        self.images = { 'stand'     : ['stand1'],
                        'walkleft'  : ['walkleft1','walkleft2'],
                        'walkright' : ['walkright1','walkright2']
                      }
        # the index of the current image in the image list
        self.animationindex = 0

    def update(self):

        # update position and state based on keyboard input
        if keyboard.left:
            self.x -= 1
            self.state = 'walkleft'
        elif keyboard.right:
            self.x += 1
            self.state = 'walkright'
        else:
            self.state = 'stand'

        # update animation by incrementing timer
        # and updating sprite image if timer limit reached
        self.animationtimer += 1
        if self.animationtimer >= self.animationdelay:
            self.animationtimer = 0
            self.animationindex += 1
            if self.animationindex > len(self.images[self.state]) - 1:
                self.animationindex = 0
            self.image = self.images[self.state][self.animationindex]

# create a new player
p = Player()

def update():
    p.update()

def draw():
    screen.clear()
    p.draw()

pgzrun.go()