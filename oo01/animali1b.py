import pgzrun
import random

WIDTH = 500
HEIGHT = 400
TITLE = "Animali (simulazione)"

class Animale(Actor):
    '''
    Animale è un nuovo tipo di Actor
    ovvero può averne lo stesso comportamento
    e gli stessi attributi
    Questo è il metodo costruttore
    '''
    tutti = []

    def __init__(self):
        super().__init__('pecora.png')
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.veloc_x = random.uniform(-1,1)
        self.veloc_y = random.uniform(-1,1)
        Animale.tutti.append(self)

    def muovi(self):
        self.x += self.veloc_x
        self.y += self.veloc_y

# Creo quattro "istanze" (anonime)
# Per controllarle posso usare la variabile di classe "tutti"
Animale()
Animale()
Animale()
Animale()

def draw():
    screen.blit('southdowns.jpeg', (0,0))
    for a in Animale.tutti: a.draw()

def update():
    for a in Animale.tutti: a.muovi()

pgzrun.go()