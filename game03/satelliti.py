import pgzrun
from random import randint
from time import time

TITLE = "Connetti i satelliti"
WIDTH = 800
HEIGHT = 600

satelliti = []
linee = []
indice_prossimo_satellite = 0

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
    
    for linea in linee:
        screen.draw.line(linea[0], linea[1], (255,255,255))

    if indice_prossimo_satellite < numero_satelliti:
        tempo_totale = time() - tempo_iniziale
        screen.draw.text(str(round(tempo_totale,2)), (10,10), fontsize=30)
    else:
        screen.draw.text(str(round(tempo_totale,2)), (10,10), fontsize=30)

def update():
    pass

def on_mouse_down(pos):
    global indice_prossimo_satellite, linee

    if indice_prossimo_satellite < numero_satelliti:
        if satelliti[indice_prossimo_satellite].collidepoint(pos):
            if indice_prossimo_satellite:
                linee.append((satelliti[indice_prossimo_satellite-1].pos, satelliti[indice_prossimo_satellite].pos))
            indice_prossimo_satellite = indice_prossimo_satellite + 1
        else:            
            linee = []
            indice_prossimo_satellite = 0

crea_satelliti()
pgzrun.go()