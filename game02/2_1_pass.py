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
    """
    Funzione speciale PGZ
    """
    screen.blit("sfondo", (0, 0))
    fiore.draw()
    ape.draw()
    screen.draw.text("Punteggio: " + str(punteggio), color="black", topleft=(10, 10))

    if game_over:
        screen.fill("pink")
        screen.draw.text(
            "Tempo scaduto! Punteggio finale: " + str(punteggio),
            midtop=(WIDTH / 2, 10),
            fontsize=40,
            color="red",
        )


def piazza_fiore():
    pass


def tempo_scaduto():
    pass


def update():
    """
    Funzione speciale PGZ
    """
    pass


pgzrun.go()
