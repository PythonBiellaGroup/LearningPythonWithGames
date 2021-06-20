import pgzrun
import random, math, time

'''
Ravvicinamento a gruppi
'''

WIDTH = 800
HEIGHT = 600

class Animal(Actor):

    all = []

    def __init__(self):
        super(Animal, self).__init__('pecora.png')
        self.x = random.randint(WIDTH*1/5, WIDTH*4/5)
        self.y = random.randint(HEIGHT*1/5, HEIGHT*4/5)
        Animal.all.append(self)

    def move(self):
        for o in self.other_animals():
            self.move_by_attraction(o)

    def other_animals(self):
        """All the animals except us"""
        return [a for a in Animal.all if a != self]

    def move_by_attraction(self, other):
        angle = self.angle_to(other)
        fx = math.cos(angle) * self.attraction_to(other)
        fy = math.sin(angle) * self.attraction_to(other)
        self.x += fx
        self.y += fy

    def distance_to(self, other):
        # Distances
        dx = self.x - other.x
        dy = self.y - other.y
        # Pythagoras
        return math.sqrt(dx**2 + dy**2)

    def angle_to(self, other):
        # 0 is left, pi/2 is up, pi is right, -pi/2 down
        return math.atan2(other.y - self.y, other.x - self.x)

    def attraction_to(self, other):
        # Attraction until we get too close
        d = self.distance_to(other)
        return 0.2 * -math.cos(d/40)

# Make some animals
for i in range(15):
    Animal()

def draw():
    screen.blit('southdowns.jpeg', (0,0))
    for a in Animal.all: a.draw()

def update():
    for a in Animal.all: a.move()

pgzrun.go()    