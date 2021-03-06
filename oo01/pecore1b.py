import pgzrun
import random

WIDTH = 500
HEIGHT = 400
TITLE = "Pecore (simulazione)"

'''
Creo più oggetti dello stesso tipo
e una variabile di classe: tutte

Movimento casuale

Rimane in finestra
'''

class Pecora(Actor):
    '''
    Pecora è un nuovo tipo di Actor
    ovvero può averne lo stesso comportamento
    e gli stessi attributi
    Questo è il metodo costruttore
    '''
    tutte = []

    def __init__(self):
        super().__init__('pecora.png')
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.veloc_x = random.uniform(-1,1)
        self.veloc_y = random.uniform(-1,1)
        Pecora.tutte.append(self)

    def muovi(self):
        self.x += self.veloc_x
        self.y += self.veloc_y
        self.rimani_in_finestra()

    def rimani_in_finestra(self):
        if self.x < 20:         self.x = 20
        elif self.x > WIDTH - 20:   self.x = WIDTH - 20
        if self.y < 20:         self.y = 20
        elif self.y > HEIGHT - 20:  self.y = HEIGHT - 20        

# Creo quattro "istanze" (anonime)
# Per controllarle posso usare la variabile di classe "tutti"
Pecora()
Pecora()
Pecora()
Pecora()

def draw():
    screen.blit('praterie.jpeg', (0,0))
    for p in Pecora.tutte: p.draw()

def update():
    for p in Pecora.tutte: p.muovi()

pgzrun.go()