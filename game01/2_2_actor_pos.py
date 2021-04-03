# pgzrun è importato tutto
import pgzrun
# random: modulo per numeri casuali
from random import randint

TITLE = "Colpisci l'alieno"
WIDTH = 800
HEIGHT = 600

alieno = Actor("alieno")
#alieno.pos = 50,50

def draw():
    screen.clear()
    screen.fill(color=(128,0,0))
    alieno.draw()

def piazza_alieno():
    '''
    Il limite di 50 pixel è definito per evitare che l'immagina 
    sia parzialmente fuori schermo
    '''
    alieno.x = randint(50, WIDTH-50)
    alieno.y = randint(50, HEIGHT-50)

piazza_alieno()
pgzrun.go()