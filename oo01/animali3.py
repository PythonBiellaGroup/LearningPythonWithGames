import pgzrun
import random, math, time

WIDTH = 800
HEIGHT = 600
TITLE = "Animali (simulazione)"

class Animale(Actor):

    tutti = []

    def __init__(self, img):
        super(Animale, self).__init__(img)
        self.x = random.randint(WIDTH*1/5, WIDTH*4/5)
        self.y = random.randint(HEIGHT*1/5, HEIGHT*4/5)
        Animale.tutti.append(self)

    def muovi(self):
        for o in self.altri_animali():
            self.muovi_per_attrazione(o)
        self.rimani_in_finestra()

    def rimani_in_finestra(self):
        if self.x < 20:         self.x = 20
        elif self.x > WIDTH - 20:   self.x = WIDTH - 20
        if self.y < 20:         self.y = 20
        elif self.y > HEIGHT - 20:  self.y = HEIGHT - 20                

    def altri_animali(self):
        """All the animals except us"""
        return [a for a in Animale.tutti if a != self]

    def muovi_per_attrazione(self, other):
        angle = self.angolo_da(other)
        fx = math.cos(angle) * self.attrazione_da(other)
        fy = math.sin(angle) * self.attrazione_da(other)
        self.x += fx
        self.y += fy

    def distanza_da(self, other):
        # Distances
        dx = self.x - other.x
        dy = self.y - other.y
        # Pythagoras
        return math.sqrt(dx**2 + dy**2)

    def angolo_da(self, other):
        # 0 is left, pi/2 is up, pi is right, -pi/2 down
        return math.atan2(other.y - self.y, other.x - self.x)

    def attrazione_da(self, other):
        # Attraction until we get too close
        d = self.distanza_da(other)
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
    for a in Animale.tutti: a.muovi()

pgzrun.go()    