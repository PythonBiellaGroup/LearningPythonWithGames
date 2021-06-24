import pgzrun
import random, math, time
from enum import Enum
import pygame
from animali_lib import *

WIDTH = 800
HEIGHT = 800
TITLE = "Animali (simulazione)"
MAX_SPEED = 2

class Stato(Enum):
    MORTO = 0
    VIVO = 1

class Animale(Actor):

    tutti = []

    def __init__(self, img):
        super(Animale, self).__init__(img)
        self.status = Stato.VIVO
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.direction = random.uniform(0, math.pi * 2)
        self.max_speed = MAX_SPEED
        self.speed = random.uniform(0.05, self.max_speed)

        Animale.tutti.append(self)

    def muovi(self):
        if self.status == Stato.MORTO:
            return

        # Our default direction vector
        dx, dy = xy_from_angle_mag(self.direction, self.speed)

        # Change our direction and speed according to other animals
        for o in self.altri_animali():
            fx, fy = xy_from_angle_mag(self.angolo_da(o), self.attrazione_da(o))
            dx += fx
            dy += fy

        # Uptdate direction with attractions above
        self.direction, self.speed = angle_mag_from_xy(dx, dy)
        # Don't muovi too fast
        self.speed = min(self.max_speed, self.speed)
        # Create the actual muoviment vector given that we might have reduced speed
        dx, dy = xy_from_angle_mag(self.direction, self.speed)

        # muovi
        self.x += dx
        self.y += dy

        # Wrap around
        if self.x < 0:         self.x = WIDTH
        elif self.x > WIDTH:   self.x = 0
        if self.y < 0:         self.y = HEIGHT
        elif self.y > HEIGHT:  self.y = 0

    def altri_animali(self):
        """tutti the animals except us"""
        return [a for a in Animale.tutti if a != self]

    def distanza_da(self, other):
        # Pythagoras
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angolo_da(self, other):
        # 0 is left, pi/2 is up, pi is right, -pi/2 down
        return math.atan2(other.y - self.y, other.x - self.x)

    def attrazione_da(self, other):
        # No attraction by default
        return 0

class Pecora(Animale):
    def __init__(self):
        super().__init__('pecora.png')

    def attrazione_da(self, other):
        """Positive number means attraction, negative repulsion"""
        d = self.distanza_da(other)

        # Attratte le une dtuttie altre ma non sovrapposte
        if isinstance(other, Pecora):
            if d > 50: return 5 / (d / 5) ** 2
            else:      return -5 / d

        elif isinstance(other, Lupo):
            # A Lupo, run away!
            return -15 / (d / 10) ** 2

        elif isinstance(other, Cane):
            return -10 / (d / 5) ** 2

class Lupo(Animale):
    def __init__(self):
        super().__init__('lupo.png')
        self.max_speed = MAX_SPEED*1.5

    def muovi(self):
        super().muovi()
        altri = self.altri_animali()

        # Caught a Pecora?
        i = self.collidelist(altri)
        if i != -1 and isinstance(altri[i], Pecora):
            altri[i].status = Stato.MORTO

    def attrazione_da(self, other):
        # Attraction gets stronger the closer the other gets
        d = self.distanza_da(other)
        if isinstance(other, Pecora):
            if other.status == Stato.MORTO:
                return 0
            else:
                return 15 / (d / 10) ** 2

        if isinstance(other, Cane):
            return -15 / (d/10) ** 2

class Cane(Animale):
    def __init__(self):
        super().__init__('cane.png')
        self.max_speed = MAX_SPEED*1.4

    def muovi(self):
        mx, my = pygame.mouse.get_pos()
        angle, mag = angle_mag_from_xy(mx - self.x, my - self.y)
        mag = min(mag, self.max_speed)
        dx, dy = xy_from_angle_mag(angle, mag)

        self.x += dx
        self.y += dy


# Make animals
for i in range(20):
    Pecora()
Lupo()
Cane()

def draw():
    screen.clear()
    for a in Animale.tutti: a.draw()

def update():
    for a in Animale.tutti: a.muovi()

pgzrun.go()