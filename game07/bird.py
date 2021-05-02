import pgzrun
from random import randint

TITLE = "Flappy Bird"
WIDTH = 800
HEIGHT = 700

# Parametri di gioco, trova quelli più giocabili
GAP = 130 # change to 100 instead of 130
FORZA_BATTITO_ALI = 5
VELOCITA = 3  # change to 4 instead of 2
GRAVITA = 0.5  # change to 0.5 instead of 0.3
DIST_TUBO = 600

uccello = Actor("uccello0", (80,300))
# Diamo degli attributi ad Actor
uccello.morto = False
uccello.colpito = False
uccello.punteggio = 0
uccello.vy = 0

tubo_top1 = Actor("sopra", anchor=("left", "bottom"))
tubo_bottom1 = Actor("sotto", anchor=("left", "top"))

tubo_top2 = Actor("sopra", anchor=("left", "bottom"))
tubo_bottom2 = Actor("sotto", anchor=("left", "top"))

dizionario = {"highscore":0}
inzio_gioco = False

def draw():
    screen.blit("sfondo", (0,0))
    tubo_top1.draw()
    tubo_bottom1.draw()
    tubo_top2.draw()
    tubo_bottom2.draw()
    uccello.draw()

    # Punteggio attuale
    screen.draw.text(
        str(uccello.punteggio),
        color = "red",
        midtop = (WIDTH/2, 10),
        fontsize = 70,
        shadow = (1,1)
    )
    # Punteggio migliore
    screen.draw.text(
        "Migliore: " + str(dizionario["highscore"]),
        color = (200, 170, 0),
        midbottom = (WIDTH/2, HEIGHT - 10),
        fontsize = 30,
        shadow = (1,1)
    )
    if not inzio_gioco:
        screen.draw.text(
            "Premi un tasto qualsiasi", color = "yellow",
            center = (WIDTH/2, HEIGHT/2),
            fontsize = 60, owidth = 0.5, ocolor = "black"
        )

def set_tubo():
    tubo_gap_y1 = randint(200, HEIGHT-200)
    tubo_top1.pos = (WIDTH/2, tubo_gap_y1 - GAP/2)
    tubo_bottom1.pos = (WIDTH/2, tubo_gap_y1 + GAP/2)
    
    tubo_gap_y2 = randint(200, HEIGHT-200)
    tubo_top2.pos = (WIDTH/2 + DIST_TUBO, tubo_gap_y2 - GAP/2)
    tubo_bottom2.pos = (WIDTH/2 + DIST_TUBO, tubo_gap_y2 + GAP/2)

def reset_tubo():
    if tubo_top1.right < 0:
        tubo_gap_y1 = randint(200, HEIGHT-200)
        tubo_top1.pos = (WIDTH, tubo_gap_y1 - GAP/2)
        tubo_bottom1.pos = (WIDTH, tubo_gap_y1 + GAP/2)

    if tubo_top2.right < 0:
        tubo_gap_y2 = randint(200, HEIGHT-200)
        tubo_top2.pos = (WIDTH, tubo_gap_y2 - GAP/2)
        tubo_bottom2.pos = (WIDTH, tubo_gap_y2 + GAP/2)


def update_tubo():
    global dizionario
    tubo_top1.left -= VELOCITA
    tubo_bottom1.left -= VELOCITA
    tubo_top2.left -= VELOCITA
    tubo_bottom2.left -= VELOCITA

    if tubo_top1.right < 0 or tubo_top2.right < 0:
        if not uccello.morto:
            uccello.punteggio += 1
        reset_tubo()
    
    if uccello.punteggio > dizionario["highscore"]:
        dizionario["highscore"] = uccello.punteggio


def update_uccello():
    global inzio_gioco
    uy = uccello.vy
    uccello.vy += GRAVITA
    uccello.y += (uy + uccello.vy)/2
    uccello.x = 80

    if not uccello.morto:
        if uccello.vy < -3:
            uccello.image = "uccello2"
        else:
            uccello.image = "uccello1"

    if uccello.colliderect(tubo_top1) or uccello.colliderect(tubo_bottom1) or \
        uccello.colliderect(tubo_top2) or uccello.colliderect(tubo_bottom2):
        uccello.morto = True
        if uccello.morto and not uccello.colpito:
            sounds.bang.play()
            uccello.image = "uccellocolpito"
            uccello.colpito = True
            clock.schedule(set_uccello_morto, 0.1)

    if not 0 < uccello.y < 740:
        uccello.image = "uccello0"
        uccello.y = 200
        uccello.morto = False
        uccello.colpito = False
        uccello.punteggio = 0
        uccello.vy = 0
        set_tubo()
        inzio_gioco = False
    

def set_uccello_morto():
    if uccello.morto:
        uccello.image = "uccellomorto"

def on_key_down():
    global inzio_gioco
    inzio_gioco = True

    if not uccello.morto:
        uccello.vy =- FORZA_BATTITO_ALI

def update():
    if inzio_gioco:
        update_tubo()
        update_uccello()

set_tubo()
music.play("electroman")
pgzrun.go()