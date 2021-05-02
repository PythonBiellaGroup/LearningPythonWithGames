import pgzrun
from random import randint
import math

TITLE = "Invasione dallo spazio"
WIDTH = 800
HEIGHT = 700
CENTRO_X = WIDTH / 2
CENTRO_Y = HEIGHT / 2

alieni = []
lasers = []
sequenza_mosse = 0
contatore_mosse = 0
ritardo_mossa = 30
punteggio = 0

pos_iniziale_giocatore = (400, 600)
giocatore = Actor("giocatore", pos_iniziale_giocatore)
giocatore.vite = 3

def draw():
    screen.blit("sfondo", (0,0))
    giocatore.image = giocatore.images[math.floor(giocatore.status/6)]
    giocatore.draw()
    mostra_alieni()
    mostra_lasers()
    mostra_vite()
    screen.draw.text(
        str(punteggio), topright = (780,10), owidth=0.5,
        ocolor = (255,255,255), color=(0,64,255), fontsize=60
    )
    if len(alieni) == 0:
        testo_centrale("HAI VINTO!\nPremi INVIO per giocare ancora")
    if giocatore.status >= 30:
        if giocatore.vite == 0:
            testo_centrale("GAME OVER\nPremi INVIO per giocare ancora")            
        else:
            testo_centrale("SEI STATO COLPITO\nPremi INVIO per continuare")

            
def testo_centrale(message):
    screen.draw.text(
        message, center = (CENTRO_X,CENTRO_Y),
        owidth = 0.5, ocolor = (255,255,255), color = (255,64,0),
        fontsize = 60
    )


def mostra_vite():
    for lv in range(giocatore.vite):
        screen.blit("vita", (10 + (lv*32), 10))


def update():
    global contatore_mosse, lasers, punteggio
    if giocatore.status < 30 and len(alieni) > 0:
        controlla_tasti()
        aggiorna_lasers()
        contatore_mosse += 1
        if contatore_mosse == ritardo_mossa:
            aggiorna_alieni()
            contatore_mosse = 0
        if giocatore.status > 0:
            giocatore.status += 1
            if giocatore.status == 30:
                giocatore.vite -= 1
    else:
        if keyboard.RETURN:
            if giocatore.vite > 0:
                lasers = []
                giocatore.pos = pos_iniziale_giocatore
                giocatore.status = 0
            if giocatore.vite == 0 or len(alieni) == 0:
                if giocatore.vite == 0:
                    punteggio = 0
                    giocatore.vite = 3
                init_game()

def controlla_tasti():
    global lasers
    if keyboard.left:
        if giocatore.x > 40: giocatore.x -= 5
    if keyboard.right:
        if giocatore.x < 760: giocatore.x += 5
    if keyboard.space:
        if giocatore.laser_attivo == 1:
            giocatore.laser_attivo = 0
            sounds.laser.play()
            clock.schedule(attiva_laser, 1.0)
            l = len(lasers)
            lasers.append(Actor("laser2",(giocatore.x, giocatore.y-32)))
            lasers[l].status = 0
            lasers[l].type = 1

def attiva_laser():
    giocatore.laser_attivo = 1


def mostra_lasers():
    for laser in lasers:
        laser.draw()


def aggiorna_lasers():
    global lasers, alieni
    for laser in lasers:
        if laser.type == 0:
            alieno_colpisce(laser)
            laser.y += 2
            if laser.y > HEIGHT:
                laser.status = 1
        if laser.type == 1:
            giocatore_colpisce(laser)
            laser.y -= 5
            if laser.y < 10:
                laser.status = 1

    alieni = pulizia_lista(alieni)
    lasers = pulizia_lista(lasers)


def pulizia_lista(l):
    nuova_lista = []
    for i in range(len(l)):
        if l[i].status == 0: nuova_lista.append(l[i])
    return nuova_lista

def giocatore_colpisce(laser):
    global punteggio
    for alieno in alieni:
        if alieno.collidepoint(laser.x, laser.y):
            sounds.eep.play()
            laser.status = 1
            alieno.status = 1
            punteggio += 100


def alieno_colpisce(laser):
    if giocatore.collidepoint(laser.x, laser.y):
        giocatore.status = 1
        laser.status = 1
        sounds.explosion.play()


def init_alieni():
    global alieni
    alieni = []
    for a in range(18):
        alienoX = 210 + (a % 6) * 80
        alienoY = 100 + int(a/6) * 64
        alieni.append(Actor("alieno1", (alienoX, alienoY)))
        alieni[a].status = 0


def mostra_alieni():
    for alien in alieni:
        alien.draw()


def aggiorna_alieni():
    global sequenza_mosse, lasers
    move_x = move_y = 0
    if sequenza_mosse < 10 or sequenza_mosse > 30:
        move_x = -15
    if sequenza_mosse == 10 or sequenza_mosse == 30:
        move_y = 50
    if sequenza_mosse > 10 and sequenza_mosse < 30:
        move_x = 15

    for alien in alieni:
        animate(
            alien, pos=(alien.x + move_x, alien.y + move_y),
            duration = 0.5, tween = "linear"
        )
        if randint(0,1) == 0:
            alien.image = "alieno1"
        else:
            alien.image = "alieno1b"
            if randint(0, 10) == 0:
                l = len(lasers)
                lasers.append(Actor("laser1", midtop=alien.midbottom))
                lasers[l].status = 0
                lasers[l].type = 0
    
    sequenza_mosse += 1
    if sequenza_mosse == 40:
        sequenza_mosse = 0


def init_game():
    global lasers
    giocatore.laser_attivo = 1
    giocatore.status = 0
    giocatore.pos = pos_iniziale_giocatore
    giocatore.images = ["giocatore","explosion1","explosion2","explosion3","explosion4","explosion5"]
    init_alieni()
    lasers = []

init_game()
pgzrun.go()