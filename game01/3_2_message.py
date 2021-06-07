# pgzrun è importato tutto
import pgzrun
# random: modulo per numeri casuali
from random import randint

TITLE = "Colpisci l'alieno"
WIDTH = 800
HEIGHT = 600

alieno = Actor("alieno")
messaggio = ""

def draw():
    screen.clear()
    screen.fill(color=(128,0,0))
    alieno.draw()
    screen.draw.text(messaggio, center=(400,40), fontsize=20)

def piazza_alieno():
    '''
    Il limite di 50 pixel è definito per evitare che l'immagine 
    sia parzialmente fuori schermo
    Alieno ha size 64x64
    '''
    alieno.x = randint(50, WIDTH-50)
    alieno.y = randint(50, HEIGHT-50)

def on_mouse_down(pos):
    global messaggio
    if alieno.collidepoint(pos):
        messaggio = "Bel colpo!"
        piazza_alieno()

piazza_alieno()
pgzrun.go()

'''
ESERCIZIO
- Gestire il messaggio in caso di alieno non "colpito"
- Aumentare il font del carattere
'''