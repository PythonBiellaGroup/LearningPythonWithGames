import pgzrun
import random

WIDTH = 600
HEIGHT = 400
TITLE = "Animali (simulazione)"

class Animale(Actor):
    '''
    Animale è un nuovo tipo di Actor
    ovvero può averne lo stesso comportamento
    e gli stessi attributi
    Questo è il metodo costruttore
    '''
    def __init__(self):
        super().__init__('pecora.png')
        # Posizione casuale
        self.x = random.randint(WIDTH*1/4, WIDTH*3/4)
        self.y = random.randint(HEIGHT*1/4, HEIGHT*3/4)

    # Metodo che ne gestisce il movimento
    def muovi(self):
        self.x += 1
        self.y += 0.5

a = Animale()

def draw():
    screen.blit('southdowns.jpeg', (0,0))
    a.draw()

def update():
    a.move()

pgzrun.go()