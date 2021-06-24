import pgzrun
import random

WIDTH = 600
HEIGHT = 400
TITLE = "Pecore (simulazione)"

'''
Introduzione agli oggetti
Pecora è un oggetto che eredita le caratteristiche di Actor
https://pygamezero-animals.readthedocs.io/en/latest/part1.html
'''


class Pecora(Actor):
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

p = Pecora()

def draw():
    screen.blit('praterie.jpeg', (0,0))
    p.draw()

def update():
    p.muovi()

pgzrun.go()