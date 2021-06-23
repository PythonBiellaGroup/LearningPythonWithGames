import pgzrun
import random, math, time
from enum import Enum
from animali_lib import xy_from_angle_mag, angle_mag_from_xy

WIDTH = 800
HEIGHT = 600
MAX_VEL = 1.5

class Stato(Enum):
    MORTO = 0
    VIVO = 1

class Animale(Actor):

    tutti = []

    def __init__(self, quale):
        # L'immagine la prende dall'attributo quale passato in input
        super(Animale, self).__init__('%s.png' % quale)
        self.quale = quale
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.direzione = random.uniform(0, math.pi * 2)
        self.max_vel = MAX_VEL
        self.velocita = random.uniform(2,self.max_vel)
        self.stato = Stato.VIVO

        Animale.tutti.append(self)


    def muovi(self):
        # Animale morto non si muove
        if self.stato == Stato.MORTO:
            return

        # Vettore direzione di default
        dx, dy = xy_from_angle_mag(self.direzione, self.velocita)

        # Change our direction and speed according to other animals
        for a in self.altri_animali():
            fx, fy = xy_from_angle_mag(self.angolo_da(a), self.attrazione_da(a))
            dx += fx
            dy += fy

        # Uptdate direction with attractions above
        self.direzione, self.velocita = angle_mag_from_xy(dx, dy)
        # Non troppo veloce
        self.velocita = min(self.max_vel, self.velocita)
        # Create the actual movement vector given that we might have reduced speed
        dx, dy = xy_from_angle_mag(self.direzione, self.velocita)

        # Move
        self.x += dx
        self.y += dy

        self.rimani_in_finestra()

        for a in self.altri_animali():
            self.muovi_per_attrazione(a)

    def rimani_in_finestra(self):
        if self.x < 20:         self.x = 20
        elif self.x > WIDTH - 20:   self.x = WIDTH - 20
        if self.y < 20:         self.y = 20
        elif self.y > HEIGHT - 20:  self.y = HEIGHT - 20


    def altri_animali(self):
        """Tutte le pecore eccetto se stessa"""
        return [a for a in Animale.tutti if a != self]

    def muovi_per_attrazione(self, altra):
        angle = self.angolo_da(altra)
        fx = math.cos(angle) * self.attrazione_da(altra)
        fy = math.sin(angle) * self.attrazione_da(altra)
        self.x += fx
        self.y += fy

    def distanza_da(self, altro):
        return math.sqrt((self.x - altro.x) ** 2 + (self.y - altro.y) ** 2)        

    def angolo_da(self, altra):
        # 0 sinistra, pi/2 altro, pi detra, -pi/2 basso
        return math.atan2(altra.y - self.y, altra.x - self.x)

    def attrazione_da(self, altra):
        # Nessuna attrazione di default
        return 0


class Pecora(Animale):
    def __init__(self):
        super().__init__('pecora')

    def attrazione_da(self, altra):
        """Positive number means attraction, negative repulsion"""
        d = self.distanza_da(altra)

        if altra.quale == 'pecora':
            # Attraction until we get too close
            d = self.distanza_da(altra)
            return (-30/d) + 0.01*d

        elif altra.quale == 'lupo':
            # A wolf, run away!
            return -400 / d

class Lupo(Animale):
    def __init__(self):
        super().__init__('lupo')
        self.max_vel = MAX_VEL

    def muovi(self):
        super().muovi()
        altri = self.altri_animali()

        # Presa una pecora?
        i = self.collidelist(altri)
        if i != -1 and altri[i].quale == 'pecora':
            altri[i].stato = Stato.MORTO

    def attrazione_da(self, altro):
        # Attraction gets stronger the closer the other gets
        d = self.distanza_da(altro)
        if altro.quale == 'pecora':
            if altro.stato == Stato.MORTO:
                return 0
            else:
                return 15 / (d / 10) ** 2
        return 0

# Crea gli animali
for i in range(10):
    Pecora()
Lupo()

def draw():
    screen.blit('praterie.jpeg', (0,0))
    for a in Animale.tutti: a.draw()

def update():
    for a in Animale.tutti: a.muovi()

pgzrun.go()