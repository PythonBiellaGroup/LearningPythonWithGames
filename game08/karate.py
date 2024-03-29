import pgzrun
from random import randint

TITLE = "Karate Kid"
WIDTH = 800
HEIGHT = 600

CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
CENTER = (CENTER_X, CENTER_Y)

lista_mosse = []
mostra_lista = []

punteggio = 0
mossa_corrente = 0
cnt_alla_rovescia = 4
durata_combattimento = 4

combatti = False
mostra_contoallarovescia = False
mosse_completate = False
game_over = False
inizio_gioco = False
turni = 0

# Karate Kid
karate_kid = Actor("karate-start")
karate_kid.pos = CENTER_X, CENTER_Y + 100
# Anche le frecce per le mosse sono Actors
su = Actor("su")
su.pos = CENTER_X, CENTER_Y - 230
destra = Actor("destra")
destra.pos = CENTER_X + 60, CENTER_Y - 170
giu = Actor("giu")
giu.pos = CENTER_X, CENTER_Y - 100
sinistra = Actor("sinistra")
sinistra.pos = CENTER_X - 60, CENTER_Y - 170

def draw():
    '''
    Draw PGZ: gli oggetti di gioco
    '''
    global game_over, punteggio, combatti, cnt_alla_rovescia, mostra_contoallarovescia, inizio_gioco
    screen.clear()
    screen.blit("sfondo", (0,0))
    karate_kid.draw()
    su.draw()
    giu.draw()
    sinistra.draw()
    destra.draw()
    screen.draw.text(
        "Punteggio: " + str(punteggio),
        color = "black", topleft = (10,10),
        fontsize = 30
    )
    if combatti:
        screen.draw.text(
            "Combatti!", color = "white",
            topleft = (CENTER_X - 65, CENTER_Y + 200),
            fontsize = 60
        )
    if mostra_contoallarovescia:
        screen.draw.text(
            str(cnt_alla_rovescia), color = "white",
            topleft = (CENTER_X - 8, CENTER_Y + 200),
            fontsize = 60
        )
    if not inizio_gioco and not game_over:
        screen.draw.text(
            "Premi SPAZIO per iniziare", midbottom = CENTER,
            fontsize = 40, color = "orange", owidth = 0.5,
            ocolor = "black", shadow = (1,1), scolor = "black"
        )
    if game_over:
        inizio_gioco = False
        screen.draw.text(
            "Oops! Mossa sbagliata.\nPremi SPAZIO per ricominciare",
            color = "orange",
            midbottom = CENTER, fontsize = 40, owidth = 0.5,
            ocolor = "black", shadow = (1,1), scolor = "black"
        )

def update():
    '''
    Update PGZ: aggiornamento degli oggetti di gioco
    '''
    global game_over, mossa_corrente, mosse_completate, inizio_gioco
    if not game_over:
        if mosse_completate:
            genera_mosse()
            mosse_completate = False
            mossa_corrente = 0
    else:
        music.stop()

    if keyboard.SPACE and not inizio_gioco:
        reset_game()

def reset_game():
    '''
    Reset di tutte le variabili per (ri)partire
    '''
    global game_over, inizio_gioco, punteggio, durata_combattimento, mossa_corrente
    global lista_mosse, mostra_lista, turni
    game_over = False
    inizio_gioco = True
    mossa_corrente = 0
    turni = 0
    punteggio = 0
    durata_combattimento = 4
    lista_mosse = []
    mostra_lista = []
    risistema_karate_kid()
    music.play("baseafterbase")
    genera_mosse()

def risistema_karate_kid():
    '''
    Reset degli actor
    '''
    global game_over
    if not game_over:
        karate_kid.image = "karate-start"
        su.image = "su"
        destra.image = "destra"
        sinistra.image = "sinistra"
        giu.image = "giu"

def aggiorna_karate_kid(mossa):
    '''
    Per ogni mossa, aggiornamento immagine karateca e freccia relativa
    '''
    global game_over
    if not game_over:
        if mossa == 0:
            su.image = "su-lit"
            karate_kid.image = "karate-up"
            clock.schedule(risistema_karate_kid, 0.5)
        elif mossa == 1:
            destra.image = "destra-lit"
            karate_kid.image = "karate-right"
            clock.schedule(risistema_karate_kid, 0.5)
        elif mossa == 2:
            giu.image = "giu-lit"
            karate_kid.image = "karate-down"
            clock.schedule(risistema_karate_kid, 0.5)
        else:
            sinistra.image = "sinistra-lit"
            karate_kid.image = "karate-left"
            clock.schedule(risistema_karate_kid, 0.5)
        sounds.shout.play()

def genera_mosse():
    '''
    Genera la sequenza di mosse e mostra il conto alla rovescia
    '''
    global lista_mosse, durata_combattimento, cnt_alla_rovescia, mostra_contoallarovescia, combatti, turni
 
    cnt_alla_rovescia = 4
    lista_mosse = []
    combatti = False

    turni += 1
    # Ogni tre turni aumenta la difficoltà aggiungendo una mossa in più
    if turni % 3 == 0:
        durata_combattimento += 1

    # Crea la sequenza delle mosse
    for mossa in range(0, durata_combattimento):
        mossa_casuale = randint(0,3)
        lista_mosse.append(mossa_casuale)
        mostra_lista.append(mossa_casuale)
    
    mostra_contoallarovescia = True
    contoallarovescia()

def mostra_mosse():
    '''
    Mostra la sequenza di mosse
    '''
    global lista_mosse, mostra_lista, durata_combattimento
    global combatti, mostra_contoallarovescia, mossa_corrente

    if mostra_lista:
        questa_mossa = mostra_lista[0]
        mostra_lista = mostra_lista[1:]

        aggiorna_karate_kid(questa_mossa)
        # Visualizza la mossa per un secondo
        clock.schedule(mostra_mosse, 1)
    else:
        combatti = True
        mostra_contoallarovescia = False

def contoallarovescia():
    '''
    Mostra la sequenza di mosse
    '''
    global cnt_alla_rovescia, game_over, mostra_contoallarovescia
    if cnt_alla_rovescia > 1:
        cnt_alla_rovescia -= 1
        clock.schedule(contoallarovescia, 1)
    else:
        mostra_contoallarovescia = False
        mostra_mosse()

def prossima_mossa():
    '''
    Aggiorna la prossima mossa e verifica se la sequenza è completa
    '''
    global durata_combattimento, mossa_corrente, mosse_completate
    if mossa_corrente < durata_combattimento - 1:
        mossa_corrente += 1
    else:
        mosse_completate = True

def on_key_down(key):
    '''
    Gestione input da tastiera e verifica correttezza mosse
    '''
    global punteggio, game_over, lista_mosse, mossa_corrente
    if key == keys.UP:
        aggiorna_karate_kid(0)
        if lista_mosse[mossa_corrente] == 0:
            punteggio += 1
            prossima_mossa()
        else:
            game_over = True
    elif key == keys.RIGHT:
        aggiorna_karate_kid(1)
        if lista_mosse[mossa_corrente] == 1:
            punteggio += 1
            prossima_mossa()
        else:
            game_over = True
    elif key == keys.DOWN:
        aggiorna_karate_kid(2)
        if lista_mosse[mossa_corrente] == 2:
            punteggio += 1
            prossima_mossa()
        else:
            game_over = True
    elif key == keys.LEFT:
        aggiorna_karate_kid(3)
        if lista_mosse[mossa_corrente] == 3:
            punteggio += 1
            prossima_mossa()
        else:
            game_over = True

pgzrun.go()