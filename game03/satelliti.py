import pgzrun
from random import randint
from time import time

TITLE = "🐍🐍 Connetti i satelliti 🐍🐍"
WIDTH = 800
HEIGHT = 600

satelliti = []
linee = []
indice_prossimo_satellite = 0

tempo_iniziale = 0
tempo_totale = 0
tempo_finale = 0

NUM_SATELLITI = 8

def crea_satelliti():
    global tempo_iniziale 
    for count in range(0, NUM_SATELLITI):
        satellite = Actor("satellite")
        # Creazione della posizione in modo casuale
        satellite.pos = randint(40, WIDTH-40), randint(40, HEIGHT-40)
        # Aggiunta alla lista
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
        # Le linee vengono disegnate in bianco
        screen.draw.line(linea[0], linea[1], (255,255,255))

    if indice_prossimo_satellite < NUM_SATELLITI:
        tempo_totale = time() - tempo_iniziale
        screen.draw.text(str(round(tempo_totale,2)), (10,10), fontsize=30)
    else:
        screen.draw.text(str(round(tempo_totale,2)), (10,10), fontsize=30)

def update():
    pass

def on_mouse_down(pos):
    '''
    Gestione click: se le connessioni non sono completate...
    Se l'indice del satellite cliccato è quello corretto si aggiunge la linea
    altrimenti si resetta
    '''
    global indice_prossimo_satellite, linee

    if indice_prossimo_satellite < NUM_SATELLITI:
        if satelliti[indice_prossimo_satellite].collidepoint(pos):
            if indice_prossimo_satellite:
                # La lista linee contiene tuple (posizione precedente, posizione successiva)
                # Ogni posizione è a sua volta una tupla pos(x,y)
                linee.append((satelliti[indice_prossimo_satellite-1].pos, satelliti[indice_prossimo_satellite].pos))
            indice_prossimo_satellite = indice_prossimo_satellite + 1
        else:            
            linee = []
            indice_prossimo_satellite = 0

crea_satelliti()
pgzrun.go()