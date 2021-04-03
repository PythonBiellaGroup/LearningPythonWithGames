import pgzrun
from random import randint

TITLE = "Colpisci l'alieno"
WIDTH = 800
HEIGHT = 600

messaggio = ""

alieno = Actor("alieno")

def draw():
    screen.clear()
    screen.fill(color=(128,0,0))
    alieno.draw()
    screen.draw.text(messaggio, center=(400,40), fontsize=60)

def piazza_alieno():
    alieno.x = randint(50, WIDTH-50)
    alieno.y = randint(50, HEIGHT-50)


def on_mouse_down(pos):
    global messaggio
    if alieno.collidepoint(pos):
        messaggio = "Bel colpo!"
        piazza_alieno()
    else:
        messaggio = "Mancato..."


piazza_alieno()
pgzrun.go()