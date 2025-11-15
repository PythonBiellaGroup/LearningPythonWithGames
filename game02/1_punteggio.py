import pgzrun
from random import randint

WIDTH = 600
HEIGHT = 500

punteggio = 0
game_over = False

ape = Actor("ape")
ape.pos = 100, 100

fiore = Actor("fiore")
fiore.pos = 200, 200


def draw():
    screen.blit("sfondo", (0, 0))
    fiore.draw()
    ape.draw()
    screen.draw.text("Punteggio: " + str(punteggio), color="black", topleft=(10, 10))


pgzrun.go()
