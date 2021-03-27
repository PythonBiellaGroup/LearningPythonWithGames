import pgzrun
from random import randint
from time import time

WIDTH = 800
HEIGHT = 600

satelliti = []
linee = []
prossimo_satellite = 0

tempo_iniziale = 0
tempo_totale = 0
tempo_finale = 0

numero_satelliti = 8

def crea_satelliti():
    global tempo_iniziale 
    for count in range(0, numero_satelliti):
        satellite = Actor("satellite")
        satellite.pos = randint(40, WIDTH-40), randint(40, HEIGHT-40)
        satelliti.append(satellite)
    tempo_iniziale = time()


def draw():
    global tempo_totale
    screen.blit("sfondo", (0,0))
    numero = 1
    for satellite in satelliti:
        screen.draw.text(str(numero), (satellite.pos[0], satellite.pos[1]+20))
        satellite.draw()
        numero = numero + 1
    
    for line in linee:
        screen.draw.line(line[0], line[1], (255,255,255))

    if prossimo_satellite < numero_satelliti:
        tempo_totale = time() - tempo_iniziale
        screen.draw.text(str(round(tempo_totale,1)), (10,10), fontsize=30)
    else:
        screen.draw.text(str(round(tempo_totale,1)), (10,10), fontsize=30)


def update():
    pass

def on_mouse_down(pos):
    global prossimo_satellite, linee

    if prossimo_satellite < numero_satelliti:
        if satelliti[prossimo_satellite].collidepoint(pos):
            if prossimo_satellite:
                linee.append((satelliti[prossimo_satellite-1].pos, satelliti[prossimo_satellite].pos))
            prossimo_satellite = prossimo_satellite + 1
        else:
            linee = []
            prossimo_satellite = 0

crea_satelliti()
pgzrun.go()