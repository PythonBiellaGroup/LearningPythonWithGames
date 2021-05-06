import pgzrun
from random import randint
import math

WIDTH = 1000
HEIGHT = 700
TITLE = "Collezionista di stelle"
CENTRO_X = WIDTH/2
CENTRO_Y = HEIGHT/2
CENTRO = (CENTRO_X, CENTRO_Y)
VEL_RAZZO = 5
DISTANZA_DI_COLLISIONE = 50

lista_stelle_felici = []
lista_stelle_calde = []
punteggio = 0

razzo = Actor("razzo", pos=CENTRO)
# Sequenza esplosione
razzo.img_esplosione = ["explosion1","explosion2","explosion3","explosion4"]
razzo.stato = 0
razzo.vite = 3
razzo.colpito = False

def draw():
    screen.clear()
    screen.blit("sfondo", (0,0))
    mostra_punteggio()
    mostra_vite()
    for stella_felice in lista_stelle_felici:
        stella_felice.draw()
    for stella_calda in lista_stelle_calde:
        stella_calda.draw()
    razzo.draw()

    if razzo.colpito:
        if razzo.vite > 0:
            screen.draw.text(
                "COLPITO!\nPremi INVIO per continuare",
                center=CENTRO, owidth = 0.5, ocolor = "white",
                color = (255,64,0), fontsize=60
            )
        else:
            screen.draw.text(
                "GAME OVER!\nPremi INVIO per ricominciare",
                center = CENTRO, owidth=0.5, ocolor="white",
                color=(255,64,0), fontsize=60
            )


def update():
    global punteggio
    controlla_tasti()
    aggiorna_stella()
    controlla_collisione_stella_felice()
    controlla_collisione_stella_calda()
    # Gestione urto con stella calda
    if razzo.colpito:
        razzo_esplode()
        if keyboard.RETURN:            
            if razzo.vite == 0:
                # Ricomincia il gioco
                razzo.vite = 3
                punteggio = 0
            inizia_gioco()

def mostra_vite():
    for v in range(razzo.vite):
        screen.blit("vita", (10+(v*32),10))

def mostra_punteggio():
    global punteggio
    screen.draw.text(
        str(punteggio),
        pos=(CENTRO_X,10), color="red",
        fontsize=60, owidth=0.5, ocolor="black",
        shadow=(1,1), scolor="black"
    )    

def controlla_tasti():
    if not razzo.colpito:
        if keyboard.right and razzo.x < WIDTH:
            razzo.angle = -90
            razzo.x += VEL_RAZZO
        elif keyboard.left and razzo.x > 0:
            razzo.angle = 90
            razzo.x -= VEL_RAZZO
        elif keyboard.up and razzo.y > 0:
            razzo.angle = 0
            razzo.y -= VEL_RAZZO
        elif keyboard.down and razzo.y < HEIGHT:
            razzo.angle = 180
            razzo.y += VEL_RAZZO

def aggiungi_stella():
    global lista_stelle_felici
    if not razzo.colpito:
        nuova_stella_felice = Actor("stella")
        nuova_stella_felice.pos = randint(50, WIDTH-50), randint(50, HEIGHT-50)
        lista_stelle_felici.append(nuova_stella_felice)

def aggiorna_stella():
    if not razzo.colpito:
        for stella_calda in lista_stelle_calde:
            stella_calda.x += stella_calda.vx 
            stella_calda.y += stella_calda.vy

            if stella_calda.left < 0:
                stella_calda.vx = -stella_calda.vx
            if stella_calda.right > WIDTH:
                stella_calda.vx = -stella_calda.vx
            if stella_calda.top < 0:
                stella_calda.vy = -stella_calda.vy
            if stella_calda.bottom > HEIGHT:
                stella_calda.vy = -stella_calda.vy

def muta_stella():
    global lista_stelle_felici, lista_stelle_calde
    if not razzo.colpito and lista_stelle_felici:
        stella_casuale = randint(0, len(lista_stelle_felici)-1)
        stella_calda_pos_x = lista_stelle_felici[stella_casuale].x 
        stella_calda_pos_y = lista_stelle_felici[stella_casuale].y 

        del lista_stelle_felici[stella_casuale]

        stella_calda = Actor("stella-calda")
        stella_calda.pos = stella_calda_pos_x, stella_calda_pos_y
        stella_calda.vx = velocita_stella()
        stella_calda.vy = velocita_stella()
        lista_stelle_calde.append(stella_calda)

def velocita_stella():
    direz_casuale = randint(0,1)
    veloc_casuale = randint(1,2)
    if direz_casuale == 0:
        return -veloc_casuale
    else:
        return veloc_casuale

def controlla_collisione_stella_felice():
    global punteggio, lista_stelle_felici
    if not razzo.colpito:
        for index in range(0, len(lista_stelle_felici)-1):
            if lista_stelle_felici[index].colliderect(razzo):
                punteggio += 1
                sounds.eep.play()
                del lista_stelle_felici[index]

def controlla_collisione_stella_calda():
    global lista_stelle_calde
    if not razzo.colpito:
        for index in range(0, len(lista_stelle_calde)-1):
            distanza = razzo.distance_to(lista_stelle_calde[index])
            if not razzo.colpito and distanza < DISTANZA_DI_COLLISIONE:
                razzo.vite -= 1
                del lista_stelle_calde[index]
                razzo.colpito = True

def razzo_esplode():
    if razzo.colpito:
        if razzo.stato == 0:
            sounds.explosion.play()
        
        if razzo.stato < 90:
            razzo.stato += 1
            razzo.image = razzo.img_esplosione[math.floor(razzo.stato/30)]

def inizia_gioco():
    global lista_stelle_felici, lista_stelle_calde
    lista_stelle_felici = []
    lista_stelle_calde = []
    razzo.image = "razzo"
    razzo.pos = CENTRO
    razzo.stato = 0
    razzo.colpito = False


clock.schedule_interval(aggiungi_stella, 2)
clock.schedule_interval(muta_stella, 5)
pgzrun.go()