import pgzrun
from random import randint

TITLE = "Connetti i satelliti"
WIDTH = 800
HEIGHT = 600

satelliti = []
linee = []
# Nelle liste gli indici partono da zero!
indice_prossimo_satellite = 0

numero_satelliti = 8

def crea_satelliti():
    global tempo_iniziale 
    for count in range(0, numero_satelliti):
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
    
    for line in linee:
        # (255,255,255) -> bianco
        screen.draw.line(line[0], line[1], (255,255,255))

def on_mouse_down(pos):
    global indice_prossimo_satellite, linee
    # Se il gioco non è finito
    print(indice_prossimo_satellite)
    if indice_prossimo_satellite < numero_satelliti:
        if satelliti[indice_prossimo_satellite].collidepoint(pos):
            # L'utente ha cliccato sul satellite giusto
            if indice_prossimo_satellite:
                linee.append((satelliti[indice_prossimo_satellite-1].pos, satelliti[indice_prossimo_satellite].pos))
            indice_prossimo_satellite = indice_prossimo_satellite + 1
        else:       
            # Se l'utente clicca sul satellite sbagliato, deve ricominciare     
            linee = []
            indice_prossimo_satellite = 0

crea_satelliti()
pgzrun.go()
