import pgzrun
import random, math, time

'''
Le pecore si radunano
'''

WIDTH = 800
HEIGHT = 600

class Animale(Actor):

    tutti = []

    def __init__(self):
        super(Animale, self).__init__('pecora.png')
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        Animale.tutti.append(self)

    def move(self):
        for o in self.other_animals():
            self.move_by_attraction(o)

    def other_animals(self):
        """All the animals except us"""
        return [a for a in Animale.tutti if a != self]

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
        # Attraction gets stronger the closer the other gets
        d = self.distance_to(other)
        return min(2, 30 / d)

# Crea un po' di animali
Animale()
Animale()
Animale()
Animale()
Animale()
Animale()

def draw():
    screen.blit('southdowns.jpeg', (0,0))
    for a in Animale.tutti: a.draw()

def update():
    for a in Animale.tutti: a.move()

pgzrun.go()   