import pgzrun
import random

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
livello_corrente = 1
stelle = []
animazioni = []

def draw():
    global stelle, livello_corrente, game_over, game_completato
    screen.clear()
    screen.blit("sfondo", (0,0))
    if game_over:
        display_message("GAME OVER","Prova di nuovo...")
    elif game_completato:
        display_message("HAI VINTO!","Complimenti!")
    else:
        for stella in stelle:
            stella.draw()
    # if game_over or game_completato:
    #     clock.unschedule(mischia_stelle)
    

# contatore = 0
def update():
    global stelle, contatore
    if len(stelle) == 0:
        stelle = genera_stelle(livello_corrente)
    # else:
    #     contatore = contatore + 1
    #     if contatore % 30 == 0:
    #         mostra_stelle(stelle)
    #         contatore = 0


def genera_stelle(numero_stelle_extra):
    colori_da_creare = ottieni_colore_da_creare(numero_stelle_extra)
    stelle_nuove = crea_stelle(colori_da_creare)
    mostra_stelle(stelle_nuove)
    anima_stelle(stelle_nuove)
    return stelle_nuove


def ottieni_colore_da_creare(numero_stelle_extra):
    colori_da_creare = ["rossa"]
    for i in range(0, numero_stelle_extra):
        random_color = random.choice(COLORI_STELLA)
        colori_da_creare.append(random_color)
    return colori_da_creare

def crea_stelle(colori_da_creare):
    stelle_nuove = []
    for colore in colori_da_creare:
        stella = Actor("stella" + colore )
        stelle_nuove.append(stella)
    return stelle_nuove

def mostra_stelle(stelle_da_mostrare):
    numero_intervalli = len(stelle_da_mostrare) + 1
    distanza = WIDTH / numero_intervalli
    random.shuffle(stelle_da_mostrare)
    for indice, stella in enumerate(stelle_da_mostrare):
        nuova_pos_x = (indice + 1) * distanza
        stella.x = nuova_pos_x
    

def anima_stelle(stelle_da_animare):
    global animazioni
    for stella in stelle_da_animare:
        durata = VEL_INIZIALE - livello_corrente
        stella.anchor = ("center","bottom")
        animazione = animate(stella, duration=durata, on_finished=gestisci_game_over, y=HEIGHT)
        animazioni.append(animazione)

def gestisci_game_over():
    global game_over
    game_over = True

def on_mouse_down(pos):
    global stelle, livello_corrente
    for stella in stelle:
        if stella.collidepoint(pos):
            if "rossa" in stella.image:
                click_su_stella_rossa()
            else:
                gestisci_game_over()

def click_su_stella_rossa():
    global livello_corrente, stelle, animazioni, game_completato
    stop_animazioni(animazioni)
    if livello_corrente == LIVELLO_FINALE:
        game_completato = True
    else:
        livello_corrente = livello_corrente + 1
        stelle = []
        animazioni = []

def stop_animazioni(animazioni_da_fermare):
    for animazione in animazioni_da_fermare:
        if animazione.running:
            animazione.stop()


def display_message(heading_text, sub_heading_text):
    screen.draw.text(heading_text, fontsize=60, center=CENTRO, color=FONT_COLOR)
    screen.draw.text(sub_heading_text,fontsize=30, center=(CENTRO_X,CENTRO_Y+30), color=FONT_COLOR)


#def mischia_stelle():
#    if stelle:
#        mostra_stelle(stelle)

#clock.schedule_interval(mischia_stelle, 0.5)

pgzrun.go()
