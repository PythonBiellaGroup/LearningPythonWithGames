import pgzrun
import random, math, time
from enum import Enum
from animali_lib import *

WIDTH = 800
HEIGHT = 600
TITLE = "Animali (simulazione)"
MAX_SPEED = 2

class Stato(Enum):
    MORTO = 0
    VIVO = 1

class Animale(Actor):

    tutti = []

    def __init__(self, what):
        super(Animal, self).__init__('%s.png' % what)
        self.what = what
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.direction = random.uniform(0, math.pi * 2)
        self.max_speed = MAX_SPEED
        self.speed = random.uniform(2,self.max_speed)
        self.status = Status.ALIVE

        Animal.all.append(self)

    def move(self):
        if self.status == Status.DEAD:
            return

        # Our default direction vector
        dx, dy = xy_from_angle_mag(self.direction, self.speed)

        # Change our direction and speed according to other animals
        for o in self.other_animals():
            fx, fy = xy_from_angle_mag(self.angle_to(o), self.attraction_to(o))
            dx += fx
            dy += fy

        # Uptdate direction with attractions above
        self.direction, self.speed = angle_mag_from_xy(dx, dy)
        # Don't move too fast
        self.speed = min(self.max_speed, self.speed)
        # Create the actual movement vector given that we might have reduced speed
        dx, dy = xy_from_angle_mag(self.direction, self.speed)

        # Move
        self.x += dx
        self.y += dy

        # Wrap around
        if self.x < 0:         self.x = WIDTH
        elif self.x > WIDTH:   self.x = 0
        if self.y < 0:         self.y = HEIGHT
        elif self.y > HEIGHT:  self.y = 0

    def other_animals(self):
        """All the animals except us"""
        return [a for a in Animal.all if a != self]

    def distance_to(self, other):
        # Pythagoras
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle_to(self, other):
        # 0 is left, pi/2 is up, pi is right, -pi/2 down
        return math.atan2(other.y - self.y, other.x - self.x)

    def attraction_to(self, other):
        # No attraction by default
        return 0

class Sheep(Animal):
    def __init__(self):
        super().__init__('pecora')

    def draw(self):
        if self.status == Status.DEAD:
            self.image = 'pecora_colpita.png'
        super().draw()

    def attraction_to(self, other):
        """Positive number means attraction, negative repulsion"""
        d = self.distance_to(other)

        # Attratte le une dalle altre ma non sovrapposte
        if other.what == 'pecora':
            if d > 50: return 5 / (d / 5) ** 2
            else:      return -5 / d

        elif other.what == 'lupo':
            # A wolf, run away!
            return -15 / (d / 10) ** 2

class Wolf(Animal):
    def __init__(self):
        super().__init__('lupo')
        self.max_speed = MAX_SPEED*1.5

    def move(self):
        super().move()
        others = self.other_animals()

        # Caught a sheep?
        i = self.collidelist(others)
        if i != -1 and others[i].what == 'pecora':
            others[i].status = Status.DEAD

    def attraction_to(self, other):
        # Attraction gets stronger the closer the other gets
        d = self.distance_to(other)
        if other.what == 'pecora':
            if other.status == Status.DEAD:
                return 0
            else:
                return 15 / (d / 10) ** 2
        return 0

# Make animals
for i in range(20):
    Sheep()
Wolf()
Wolf()

def draw():
    screen.blit('southdowns.jpeg', (0,0))
    for a in Animal.all: a.draw()
    #time.sleep(2)

def update():
    for a in Animal.all: a.move()

pgzrun.go()    