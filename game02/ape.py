import pgzrun
from random import randint

TITLE = "Ape golosa"
WIDTH = 600
HEIGHT = 500

punteggio = 0
game_over = False

ape = Actor("ape")
ape.pos = 100,100

fiore = Actor("fiore")

def draw():
    screen.blit("sfondo", (0,0))
    fiore.draw()
    ape.draw()
    screen.draw.text("Punteggio: " + str(punteggio), color="black", topleft=(10,10))

    if game_over:
            screen.fill("pink")
            screen.draw.text("Tempo scaduto! Punteggio finale: " + str(punteggio), midtop=(WIDTH/2,10), 
            fontsize=40, color="red")

def piazza_fiore():
    fiore.x = randint(70, (WIDTH-70))
    fiore.y = randint(70, (HEIGHT-70))

def tempo_scaduto():
    global game_over 
    game_over = True

def update():
    '''
    Funzione speciale PGZ
    '''
    global punteggio

    if keyboard.left:
        ape.x = ape.x - 2
    if keyboard.right:
        ape.x = ape.x + 2
    if keyboard.up:
        ape.y = ape.y - 2
    if keyboard.down:
        ape.y = ape.y + 2

    fiore_raccolto = ape.colliderect(fiore)

    if fiore_raccolto:
        punteggio = punteggio + 10
        piazza_fiore()


piazza_fiore()
clock.schedule(tempo_scaduto, 10.0)
pgzrun.go()