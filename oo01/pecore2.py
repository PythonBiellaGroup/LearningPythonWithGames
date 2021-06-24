import pgzrun
import random, math, time

'''
Simuliamo il gregge
Le pecore si radunano utilizzando funzioni matematiche!
https://pygamezero-animals.readthedocs.io/en/latest/part2.html
'''

WIDTH = 800
HEIGHT = 600
TITLE = "Pecore (simulazione)"

class Pecora(Actor):

    tutte = []

    def __init__(self):
        super(Pecora, self).__init__('pecora.png')
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        Pecora.tutte.append(self)

    def muovi(self):
        for a in self.altre_pecore():
            self.muovi_per_attrazione(a)
        self.rimani_in_finestra()

    def rimani_in_finestra(self):
        if self.x < 20:         self.x = 20
        elif self.x > WIDTH - 20:   self.x = WIDTH - 20
        if self.y < 20:         self.y = 20
        elif self.y > HEIGHT - 20:  self.y = HEIGHT - 20                

    def altre_pecore(self):
        """Tutte le pecore eccetto se stessa"""
        return [a for a in Pecora.tutte if a != self]

    def muovi_per_attrazione(self, altra):
        angle = self.angolo_da(altra)
        fx = math.cos(angle) * self.attrazione_da(altra)
        fy = math.sin(angle) * self.attrazione_da(altra)
        self.x += fx
        self.y += fy

    def distanza_da(self, altra):
        # Distanze
        dx = self.x - altra.x
        dy = self.y - altra.y
        # Pitagora
        return math.sqrt(dx**2 + dy**2)

    def angolo_da(self, altra):
        # 0 sinistra, pi/2 altro, pi detra, -pi/2 basso
        return math.atan2(altra.y - self.y, altra.x - self.x)

    def attrazione_da(self, altra):
        # L'attrazione aumenta al diminuire della distanza
        d = self.distanza_da(altra)
        return min(2, 30 / d)

# Crea un po' di pecore
Pecora()
Pecora()
Pecora()
Pecora()
Pecora()
Pecora()

def draw():
    screen.blit('praterie.jpeg', (0,0))
    for a in Pecora.tutte: a.draw()

def update():
    for a in Pecora.tutte: a.muovi()

pgzrun.go()   