import pgzrun
import random, math, time
from enum import Enum
import pygame
from animali_lib import *

WIDTH = 800
HEIGHT = 600
TITLE = "Animali (simulazione)"
MAX_VEL = 2

class Stato(Enum):
    MORTO = 0
    VIVO = 1

class Animale(Actor):

    tutti = []

    def __init__(self, img):
        super(Animale, self).__init__(img)
        self.stato = Stato.VIVO
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.direzione = random.uniform(0, math.pi * 2)
        self.max_vel = MAX_VEL
        self.velocita = random.uniform(0.05, self.max_vel)

        Animale.tutti.append(self)

    def muovi(self, controlla_animali=True, controlla_zone=True, controlla_mouse=False):
        if self.stato == Stato.MORTO:
            return

        # Our default direzione vector
        dx, dy = xy_from_angle_mag(self.direzione, self.velocita)

        # Change our direzione and velocita according to altro animals
        if controlla_animali:
            for o in self.altri_animali():
                fx, fy = xy_from_angle_mag(self.angle_to(o), self.attrazione_da(o))
                dx += fx
                dy += fy

        # Check no-go zones
        if controlla_zone:
            for z in Zona.tutte:
                fx, fy = xy_from_angle_mag(self.angle_to(z), z.attrazione_da(self))
                dx += fx
                dy += fy

        if controlla_mouse:
            mx, my = pygame.mouse.get_pos()
            angle, mag = angle_mag_from_xy(mx - self.x, my - self.y)
            fx, fy = xy_from_angle_mag(angle, self.attrazione_mouse(mag))
            dx += fx
            dy += fy

        # Uptdate direzione with attractions above
        self.direzione, self.velocita = angle_mag_from_xy(dx, dy)
        # Don't muovi too fast
        self.velocita = min(self.max_vel, self.velocita)
        # Create the actual muoviment vector given that we might have reduced velocita
        dx, dy = xy_from_angle_mag(self.direzione, self.velocita)

        # muovi
        self.x += dx
        self.y += dy

        self.rimani_in_finestra()

    def rimani_in_finestra(self):
        if self.x < 20:         self.x = 20
        elif self.x > WIDTH - 20:   self.x = WIDTH - 20
        if self.y < 20:         self.y = 20
        elif self.y > HEIGHT - 20:  self.y = HEIGHT - 20   

    def altri_animali(self):
        """tutti the animals except us"""
        return [a for a in Animale.tutti if a != self]

    def distanza_da(self, altro):
        # Pythagoras
        return math.sqrt((self.x - altro.x) ** 2 + (self.y - altro.y) ** 2)

    def angle_to(self, altro):
        # 0 is left, pi/2 is up, pi is right, -pi/2 down
        return math.atan2(altro.y - self.y, altro.x - self.x)

    def attrazione_da(self, altro):
        # No attraction by default
        return 0


class Zona():

    tutte = []
    SICURA = (150, 255, 150)
    INTERDETTA = (0, 171, 255) #Acqua

    def __init__(self, x, y, size, ztype):
        self.x = x
        self.y = y
        self.size = size
        self.ztype = ztype

        Zona.tutte.append(self)

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.size // 2, self.ztype)

    def attrazione_da(self, a):
        """How attractive is this zone to this animal?"""
        distance = a.distanza_da(self)
        from_edge = distance - self.size // 2

        if self.ztype == Zona.INTERDETTA:
            if from_edge <= 0: return -100

        if self.ztype == Zona.SICURA and isinstance(a, Lupo):
            if from_edge <= 0: return -100

        return 0

# ----------------------------------------------------------

class Pecora(Animale):
    def __init__(self):
        super().__init__('pecora.png')
        # Start top left
        self.x = self.y = random.randint(5,40)
        self.max_vel = 1

    def attrazione_da(self, altro):
        """Positive number means attraction, negative repulsion"""
        d = self.distanza_da(altro)

        # Attratte le une dalle altre (quelle vive) ma non sovrapposte
        if isinstance(altro, Pecora) and altro.stato == Stato.VIVO:
            return min(0.25, (-30/(d+0.001)) + 0.01*d)

        elif isinstance(altro, Lupo):
            # A Lupo, run away!
            return -100/d

        elif isinstance(altro, Cane):
            return -20 / (d+0.001 / 5) ** 2

        return 0

class Lupo(Animale):
    def __init__(self):
        super().__init__('lupo.png')
        self.max_vel = MAX_VEL*1.1

    def muovi(self):
        super().muovi()
        altri = self.altri_animali()

        # Catturata una Pecora?
        i = self.collidelist(altri)
        if i != -1 and isinstance(altri[i], Pecora):
            altri[i].stato = Stato.MORTO

    def attrazione_da(self, altro):
        # Attraction gets stronger the closer the altro gets
        d = self.distanza_da(altro)
        if isinstance(altro, Pecora):
            if altro.stato == Stato.MORTO:
                return 0
            else:
                return 15 / (d / 10) ** 2

        if isinstance(altro, Cane):
            return -15 / (d/20) ** 2

class Cane(Animale):
    def __init__(self):
        super().__init__('cane.png')
        self.max_vel = MAX_VEL*2

    def muovi(self):
        super().muovi(controlla_animali=False, controlla_zone=True, controlla_mouse=True)

    def attrazione_mouse(self, distance):
        return 1


# Crea animali
for i in range(20):
    Pecora()
Lupo()
Cane()

# Crea zone
Zona(50, 50, 300, Zona.SICURA)
Zona(WIDTH-50, HEIGHT-50, 300, Zona.SICURA)

Zona(WIDTH/2, HEIGHT/2, 100, Zona.INTERDETTA)
Zona(WIDTH/2 + 75, HEIGHT/2 - 75, 50, Zona.INTERDETTA)
Zona(WIDTH/2 + 150, HEIGHT/2 - 150, 50, Zona.INTERDETTA)
Zona(WIDTH/2 - 75, HEIGHT/2 + 75, 50, Zona.INTERDETTA)

def draw():
    screen.fill((55,80,40))
    for z in Zona.tutte: z.draw()
    for a in Animale.tutti: a.draw()

def update():
    for a in Animale.tutti: a.muovi()
pgzrun.go()