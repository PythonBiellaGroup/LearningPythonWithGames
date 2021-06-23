import pgzrun
import random, math, time

'''
Ravvicinamento a gruppi
'''

WIDTH = 800
HEIGHT = 600

class Pecora(Actor):

    tutte = []

    def __init__(self):
        super(Pecora, self).__init__('pecora.png')
        self.x = random.randint(WIDTH*1/5, WIDTH*4/5)
        self.y = random.randint(HEIGHT*1/5, HEIGHT*4/5)
        Pecora.tutte.append(self)

    def muovi(self):
        for a in self.altre_pecore():
            self.muovi_per_attrazione(a)

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
        # --> cambio la funzione matematica
        return 0.2 * -math.cos(d/40)


# Creo un po' di pecore
for i in range(15):
    Pecora()

def draw():
    screen.blit('praterie.jpeg', (0,0))
    for p in Pecora.tutte: p.draw()

def update():
    for p in Pecora.tutte: p.muovi()

pgzrun.go()    