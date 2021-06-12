import pgzrun

TITLE = "Colpisci l'alieno"
WIDTH = 800
HEIGHT = 600

alieno = Actor("alieno")
# pos è la posizione del centro
# alieno.pos = 0,0
alieno.pos = 50,50

def draw():
    screen.clear()
    screen.fill(color=(128,0,0))
    alieno.draw()

pgzrun.go()