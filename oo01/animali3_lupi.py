import pgzrun
import random, math, time
from enum import Enum
from animali_lib import *

WIDTH = 800
HEIGHT = 600
MAX_SPEED = 1.5

class Status(Enum):
    DEAD = 0
    ALIVE = 1

class Animal(Actor):

    all = []

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

        self.stay_on_screen()

    def stay_on_screen(self):
        if self.x < 0:         self.x = 0
        elif self.x > WIDTH:   self.x = WIDTH
        if self.y < 0:         self.y = 0
        elif self.y > HEIGHT:  self.y = HEIGHT

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

    def attraction_to(self, other):
        """Positive number means attraction, negative repulsion"""
        d = self.distance_to(other)

        if other.what == 'pecora':
            # Attraction until we get too close
            d = self.distance_to(other)
            return (-30/d) + 0.01*d

        elif other.what == 'lupo':
            # A wolf, run away!
            return -400 / d

class Wolf(Animal):
    def __init__(self):
        super().__init__('lupo')
        self.max_speed = MAX_SPEED

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
for i in range(5):
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