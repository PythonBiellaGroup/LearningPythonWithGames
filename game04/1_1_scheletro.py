import pgzrun
import random

# Costanti
TITLE = "Stella Rossa"
FONT_COLOR = (255,255,255)
WIDTH = 800
HEIGHT = 600
# Per la funzione mostra_messaggio
CENTRO_X = WIDTH / 2
CENTRO_Y = HEIGHT / 2
CENTRO = (CENTRO_X, CENTRO_Y)
# Numero livelli
LIVELLO_FINALE = 8
# Velocità di partenza
VEL_INIZIALE = 10
# Il rosso non è presente perchè va gestito in modo particolare
COLORI_STELLA = ["blu","verde","arancione","porpora","gialla"]

# Variabili globali
game_over = False
game_completato = False
livello_corrente = 1
stelle = []
animazioni = []

def draw():
    '''
    Funzione richiamata in automatico da PGZ
    '''
    global stelle, livello_corrente, game_over, game_completato
    screen.clear()
    screen.blit("sfondo", (0,0))
    if game_over:
        mostra_messaggio("GAME OVER","Prova di nuovo...")
    elif game_completato:
        mostra_messaggio("HAI VINTO!","Complimenti!")
    else:
        for stella in stelle:
            # Richiama il metodo draw() dell'Actor stella
            stella.draw()

def update():
    '''
    Funzione richiamata in automatico da PGZ
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
    # Crea le stelle (usando i colori)
    # Posiziona le stelle
    # Anima le stelle
    return []

def ottieni_colore_da_creare(numero_stelle_extra):
    '''
    Funzione per ottenere la lista dei colori delle stelle da creare
    Una stella rossa ci deve essere sempre
    Gli altri colori sono presi a caso da COLORI_STELLA
    '''
    return []

def crea_stelle(colori_da_creare):
    '''
    Funzione per creare le stelle partendo dalla lista colori
    Il nome del file immagine della stella è composto da
    "stella"+colore
    Ritorna una lista di Actor stella
    '''
    stelle_nuove = []
    for colore in colori_da_creare:
        stella = Actor("stella" + colore )
        stelle_nuove.append(stella)
    return stelle_nuove

def mostra_stelle(stelle_da_mostrare):
    pass

def anima_stelle(stelle_da_animare):
    '''
    Funzione che fa muovere le stelle dall'alto verso il basso
    '''
    pass

def mostra_messaggio(titolo, sottotitolo):
    '''
    Funzione per visualizzare i messaggi al centro dello schermo
    titolo con font più grande
    sottotitolo con font più piccolo
    '''
    screen.draw.text(titolo, fontsize=60, center=CENTRO, color=FONT_COLOR)
    screen.draw.text(sottotitolo,fontsize=30, center=(CENTRO_X,CENTRO_Y+30), color=FONT_COLOR)

pgzrun.go()
