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
    anima_stelle(stelle_nuove)
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
    Funzione per mostrare le stelle allineate
    '''
    numero_intervalli = len(stelle_da_mostrare) + 1
    distanza = WIDTH / numero_intervalli
    # Mischia le stelle in modo casuale (lista)
    random.shuffle(stelle_da_mostrare)
    for indice, stella in enumerate(stelle_da_mostrare):
        nuova_pos_x = (indice + 1) * distanza
        stella.x = nuova_pos_x

def anima_stelle(stelle_da_animare):
    '''
    Funzione per la gestione delle animazioni delle stelle
    '''
    global animazioni
    for stella in stelle_da_animare:
        # Durata dell'animazione
        durata = VEL_INIZIALE - livello_corrente
        stella.anchor = ("center","bottom")
        # gestisci_game_over viene chiamata ad animazione terminata
        animazione = animate(stella, duration=durata, on_finished=gestisci_game_over, y=HEIGHT)
        animazioni.append(animazione)

def gestisci_game_over():
    '''
    Implementazione temporanea senza stop
    '''
    global livello_corrente, stelle, animazioni
    stop_animazioni(animazioni)
    livello_corrente = livello_corrente + 1
    stelle = []
    animazioni = []

def stop_animazioni(animazioni_da_fermare):
    for animazione in animazioni_da_fermare:
        if animazione.running:
            animazione.stop()




def mostra_messaggio(titolo, sottotitolo):
    screen.draw.text(titolo, fontsize=60, center=CENTRO, color=FONT_COLOR)
    screen.draw.text(sottotitolo,fontsize=30, center=(CENTRO_X,CENTRO_Y+30), color=FONT_COLOR)

pgzrun.go()
