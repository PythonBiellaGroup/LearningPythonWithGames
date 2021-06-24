import pgzrun
import random, math, time
import pygame
WIDTH = 800
HEIGHT = 600
TITLE = "Animali (simulazione)"

class Animal(Actor):

    all = []

    def __init__(self, img):
        super(Animal, self).__init__(img)
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
        return 0


class Sheep(Animal):

    def __init__(self, black=False):
        if black:
            super().__init__('pecora_nera.png')
        else:
            super().__init__('pecora.png')

    def attraction_to(self, other):
        d = self.distance_to(other)
        if isinstance(other, Sheep):
            # Attratte le une dalle altre ma non sovrapposte
            return 0.1 * -math.cos(d/40)
        elif isinstance(other, SheepDog):
            # Move away
            return -100/d+0.001


class SheepDog(Animal):

    def __init__(self):
        super().__init__('cane.png')

    def move(self):
        self.x, self.y = pygame.mouse.get_pos()

# Make some animals
for i in range(15):
    Sheep(random.choice([True, False]))

SheepDog()

def draw():
    screen.blit('southdowns.jpeg', (0,0))
    for a in Animal.all: a.draw()

def update():
    for a in Animal.all: a.move()

pgzrun.go()