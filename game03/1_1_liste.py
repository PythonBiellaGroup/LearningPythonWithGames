import pgzrun
from random import randint

TITLE = "🐍🐍 Connetti i satelliti 🐍🐍"
WIDTH = 800
HEIGHT = 600

satelliti = []
linee = []

NUM_SATELLITI = 8

def crea_satelliti():
    global tempo_iniziale
    for count in range(0, NUM_SATELLITI):
        satellite = Actor("satellite")
        satellite.pos = randint(40, WIDTH-40), randint(40, HEIGHT-40)
        satelliti.append(satellite)

def draw():
    screen.blit("sfondo", (0,0))
    numero = 1
    for satellite in satelliti:
        screen.draw.text(str(numero), (satellite.pos[0], satellite.pos[1]+20))
        satellite.draw()
        numero = numero + 1
    

crea_satelliti()
pgzrun.go()