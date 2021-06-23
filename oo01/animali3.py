import pgzrun
import random, math, time

WIDTH = 800
HEIGHT = 600

class Animale(Actor):

    tutti = []

    def __init__(self, img):
        super(Animale, self).__init__(img)
        self.x = random.randint(WIDTH*1/5, WIDTH*4/5)
        self.y = random.randint(HEIGHT*1/5, HEIGHT*4/5)
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
        # Attraction until we get too close
        d = self.distance_to(other)
        return 0.2 * -math.cos(d/40)


class Pecora(Animale):

    def __init__(self):
        super().__init__('pecora.png')


class PecoraNera(Animale):

    def __init__(self):
        super().__init__('pecora_nera.png')


class Cane(Animale):

    def __init__(self):
        super().__init__('cane.png')



# Make some animals
for i in range(10):
    Pecora()
    PecoraNera()

Cane()

def draw():
    screen.blit('praterie.jpeg', (0,0))
    for a in Animale.tutti: a.draw()

def update():
    for a in Animale.tutti: a.move()

pgzrun.go()    