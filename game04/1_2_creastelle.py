import pgzrun
import random

TITLE = "Stella Rossa"
FONT_COLOR = (255,255,255)
WIDTH = 800
HEIGHT = 600
CENTRO_X = WIDTH / 2
CENTRO_Y = HEIGHT / 2
CENTRO = (CENTRO_X, CENTRO_Y)
LIVELLO_FINALE = 8
VEL_INIZIALE = 10
COLORI_STELLA = ["blu","verde","arancione","porpora","gialla"]


game_over = False
game_completato = False
# livello_corrente: si parte con 1 stella rossa + 1 altra stella
livello_corrente = 1
stelle = []
animazioni = []

def draw():
    global stelle, livello_corrente, game_over, game_completato
    screen.clear()
    screen.blit("sfondo", (0,0))
    if game_over:
        mostra_messaggio("GAME OVER","Prova di nuovo...")
    elif game_completato:
        mostra_messaggio("HAI VINTO!","Complimenti!")
    else:
        for stella in stelle:
            stella.draw()

def update():
    '''
    Funzione richiamata in automatico da PGZ
    circa 60 volte al secondo
    '''
    global stelle, contatore
    if len(stelle) == 0:
        stelle = genera_stelle(livello_corrente)

def genera_stelle(numero_stelle_extra):
    '''
    Funzione di controllo principale, richiamata
    dentro la funzione update() gestita da PGZ
    in partenza e ad ogni cambio di livello
    '''
    # Calcola i colori da creare
    colori_da_creare = ottieni_colore_da_creare(numero_stelle_extra)
    # Crea le stelle
    stelle_nuove = crea_stelle(colori_da_creare)
    # Posiziona le stelle
    mostra_stelle(stelle_nuove)
    # Anima le stelle
    return stelle_nuove

def ottieni_colore_da_creare(numero_stelle_extra):
    '''
    Funzione per ottenere la lista dei colori delle stelle da creare
    Una stella rossa ci deve essere sempre
    Gli altri colori sono presi a caso da COLORI_STELLA
    '''
    colori_da_creare = ["rossa"]
    for i in range(0, numero_stelle_extra):
        random_color = random.choice(COLORI_STELLA)
        # Aggiunge il colore alla lista
        colori_da_creare.append(random_color)
    return colori_da_creare

def crea_stelle(colori_da_creare):
    '''
    Funzione per creare le stelle partendo dalla lista colori
    Il nome del file immagine della stella è composto da
    "stella"+colore
    Ritorna una lista di Actor stella
    '''
    stelle_nuove = []
    for colore in colori_da_creare:
        # Combina le due stringhe per ottenere il file immagine corretto
        stella = Actor("stella" + colore )
        stelle_nuove.append(stella)
    return stelle_nuove


def mostra_stelle(stelle_da_mostrare):
    '''
    Implementazione temporanea
    '''
    for indice, stella in enumerate(stelle_da_mostrare):
        stella.x = CENTRO_X + indice*50
        stella.y = CENTRO_Y + indice*50

def anima_stelle(stelle_da_animare):
    pass

def mostra_messaggio(titolo, sottotitolo):
    screen.draw.text(titolo, fontsize=60, center=CENTRO, color=FONT_COLOR)
    screen.draw.text(sottotitolo,fontsize=30, center=(CENTRO_X,CENTRO_Y+30), color=FONT_COLOR)

pgzrun.go()
