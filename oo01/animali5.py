import pgzrun
import random, math#, time
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

        # Vettore direzione di default
        dx, dy = xy_from_angle_mag(self.direzione, self.velocita)

        # Cambia direzione e velocita in base all'altro animale
        if controlla_animali:
            for o in self.altri_animali():
                fx, fy = xy_from_angle_mag(self.angolo_da(o), self.attrazione_da(o))
                dx += fx
                dy += fy

        # Controlla zona interdetta
        if controlla_zone:
            for z in Zona.tutte:
                fx, fy = xy_from_angle_mag(self.angolo_da(z), z.attrazione_da(self))
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
        """tutti gli animali eccetto noi"""
        return [a for a in Animale.tutti if a != self]

    def distanza_da(self, altro):
        # Pitagora
        return math.sqrt((self.x - altro.x) ** 2 + (self.y - altro.y) ** 2)

    def angolo_da(self, altra):
        # 0 sinistra, pi/2 altro, pi detra, -pi/2 basso
        return math.atan2(altra.y - self.y, altra.x - self.x)

    def attrazione_da(self, altro):
        # Per default, nessuna attrazione
        return 0


class Zona():

    tutte = []
    SICURA = (150, 255, 150)
    INTERDETTA = (0, 171, 255) #Acqua

    def __init__(self, x, y, size, tipo_zona):
        self.x = x
        self.y = y
        self.size = size
        self.tipo_zona = tipo_zona

        Zona.tutte.append(self)

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.size // 2, self.tipo_zona)

    def attrazione_da(self, a):
        """Quanto è attrattiva questa zona agli animali?"""
        distanza = a.distanza_da(self)
        from_edge = distanza - self.size // 2

        if self.tipo_zona == Zona.INTERDETTA:
            if from_edge <= 0: return -100

        if self.tipo_zona == Zona.SICURA and isinstance(a, Lupo):
            if from_edge <= 0: return -100

        return 0

# ----------------------------------------------------------

class Pecora(Animale):
    def __init__(self):
        super().__init__('pecora.png')
        # Iniziano in alto a sinistra
        self.x = self.y = random.randint(5,40)
        self.max_vel = 1

    def attrazione_da(self, altro):
        """Numero positivo significa attrazione; negativo repulsione"""
        d = self.distanza_da(altro)

        # Attratte le une dalle altre (quelle vive) ma non sovrapposte
        if isinstance(altro, Pecora) and altro.stato == Stato.VIVO:
            return min(0.25, (-30/(d+0.001)) + 0.01*d)

        elif isinstance(altro, Lupo):
            # Un lupo, scappa!
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
        # L'attrazione diventa più forte all'avvicinarsi
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

    def attrazione_mouse(self, distanza):
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