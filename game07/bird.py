import pgzrun
from random import randint

TITLE = "Flappy Bird"
WIDTH = 800
HEIGHT = 700

# Parametri di gioco, trova quelli più giocabili
# GAP è la distanza tra il tubo sopra e quello sotto
GAP = 150 # prova a cambiarla
# FORZA_BATTITO_ALI quando fa salire il battito d'ali
FORZA_BATTITO_ALI = 5 # prova a cambiarla
# VELOCITA è quando scorre il gioco
VELOCITA = 2  # prova a cambiarla
# GRAVITA usata per simulare la caduta per gravità, in percentule
GRAVITA = 0.3  # prova a cambiarla
# DIST_TUBO usata per definire la distanza tra i tubi consecutivi
DIST_TUBO = 600 # prova a cambiarla

uccello = Actor("uccello0", (80,300))
# Diamo degli attributi ad Actor
uccello.morto = False
uccello.colpito = False
uccello.punteggio = 0
# Velocità verticale
uccello.vy = 0

# Gli Actors hanno una “anchor position”, che è un modo conveniente per posizionarli nella scena (schermo) 
# Per default è center, in modo che l'attributo .pos (coordinate x e y) si riferisca al centro dell'attore
# In questo caso no...
tubo_top1 = Actor("sopra", anchor=("left", "bottom"))
tubo_bottom1 = Actor("sotto", anchor=("left", "top"))

tubo_top2 = Actor("sopra", anchor=("left", "bottom"))
tubo_bottom2 = Actor("sotto", anchor=("left", "top"))

# Salviamo il punteggio più alto in un dizionario
dizionario = {"highscore":0}
inizio_gioco = False

def draw():
    screen.blit("sfondo", (0,0))
    # Due tubi e l'uccello
    tubo_top1.draw()
    tubo_bottom1.draw()
    tubo_top2.draw()
    tubo_bottom2.draw()
    uccello.draw()

    # Punteggio della partita in corso
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
    if not inizio_gioco:
        # Scritta gialla con bordo nero
        screen.draw.text(
            "Premi un tasto qualsiasi", color = "yellow",
            center = (WIDTH/2, HEIGHT/2),
            fontsize = 60, owidth = 0.5, ocolor = "black"
        )

def set_tubi():
    '''
    Funzione che piazza i primi due tubi per volta
    tubo_gap_y1, tubo_gap_y2 rappresenta la componente casuale dell'altezza
    '''
    tubo_gap_y1 = randint(200, HEIGHT-200)
    tubo_top1.pos = (WIDTH/2, tubo_gap_y1 - GAP/2)
    tubo_bottom1.pos = (WIDTH/2, tubo_gap_y1 + GAP/2)
    
    tubo_gap_y2 = randint(200, HEIGHT-200)
    tubo_top2.pos = (WIDTH/2 + DIST_TUBO, tubo_gap_y2 - GAP/2)
    tubo_bottom2.pos = (WIDTH/2 + DIST_TUBO, tubo_gap_y2 + GAP/2)

def reset_tubi():
    '''
    Funzione che rimette i tubi quando spariscono
    tubo_gap_y1, tubo_gap_y2 rappresenta la componente casuale dell'altezza
    '''
    if tubo_top1.right < 0:
        tubo_gap_y1 = randint(200, HEIGHT-200)
        tubo_top1.pos = (WIDTH, tubo_gap_y1 - GAP/2)
        tubo_bottom1.pos = (WIDTH, tubo_gap_y1 + GAP/2)

    if tubo_top2.right < 0:
        tubo_gap_y2 = randint(200, HEIGHT-200)
        tubo_top2.pos = (WIDTH, tubo_gap_y2 - GAP/2)
        tubo_bottom2.pos = (WIDTH, tubo_gap_y2 + GAP/2)


def update_tubi():
    '''
    Update dei tubi, funzione richiamata dalla update generale
    '''
    global dizionario
    # I tubi scorrono...
    tubo_top1.left -= VELOCITA
    tubo_bottom1.left -= VELOCITA
    tubo_top2.left -= VELOCITA
    tubo_bottom2.left -= VELOCITA

    # Ogni volta che il tubo "esce" aggiorno il punteggio
    if tubo_top1.right < 0 or tubo_top2.right < 0:
        if not uccello.morto:
            uccello.punteggio += 1
        reset_tubi()
    
    # Se serve aggiorno il record
    if uccello.punteggio > dizionario["highscore"]:
        dizionario["highscore"] = uccello.punteggio


def update_uccello():
    '''
    Update del giocatore, funzione richiamata dalla update generale
    '''
    # L'uccello si muove solo verticalmente
    global inizio_gioco
    uy = uccello.vy
    uccello.vy += GRAVITA
    uccello.y += (uy + uccello.vy)/2
    uccello.x = 80

    # Simulazione del battito d'ali
    if not uccello.morto:
        if uccello.vy < -3:
            uccello.image = "uccello2"
        else:
            uccello.image = "uccello1"

    # Gestione collisione
    if uccello.colliderect(tubo_top1) or uccello.colliderect(tubo_bottom1) or \
        uccello.colliderect(tubo_top2) or uccello.colliderect(tubo_bottom2):
        uccello.morto = True
        # Per gestire la transizione/animazione tra colpito e morto
        if uccello.morto and not uccello.colpito:
            sounds.bang.play()
            uccello.image = "uccellocolpito"
            uccello.colpito = True
            clock.schedule(set_uccello_morto, 0.1)

    # Gestione uscita dallo schermo
    if not 0 < uccello.y < 740:
        uccello.image = "uccello0"
        uccello.y = 200
        uccello.morto = False
        uccello.colpito = False
        uccello.punteggio = 0
        uccello.vy = 0
        set_tubi()
        inizio_gioco = False
    

def set_uccello_morto():
    if uccello.morto:
        uccello.image = "uccellomorto"

def on_key_down():
    '''
    Qualsiasi tasto va bene
    '''
    global inizio_gioco
    inizio_gioco = True
    # Ricorda che le y diminuiscono verso l'alto, l'origine è in alto a sinistra
    if not uccello.morto:
        uccello.vy =- FORZA_BATTITO_ALI

def update():
    if inizio_gioco:
        update_tubi()
        update_uccello()

set_tubi()
music.play("electroman")
pgzrun.go()