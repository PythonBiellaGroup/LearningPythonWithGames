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
# Usata per gestire le mosse degli alieni
sequenza_mosse = 0
# contatore_mosse e ritardo_mossa usati per ritardare il movimento
# altrimenti il cambio immagine degli alieni sarebbe troppo veloce
contatore_mosse = 0
ritardo_mossa = 30
punteggio = 0

pos_iniziale_giocatore = (400, 600)
giocatore = Actor("giocatore", pos_iniziale_giocatore)
giocatore.vite = 3

def draw():
    screen.blit("sfondo", (0,0))
    # math.floor arrotonda all'intero più vicino
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
    '''
    Funzione con testo parametrico per visualizzazione
    messaggio centro schermo
    '''
    screen.draw.text(
        message, center = (CENTRO_X,CENTRO_Y),
        owidth = 0.5, ocolor = (255,255,255), color = (255,64,0),
        fontsize = 60
    )


def mostra_vite():
    '''
    Mostra le vite posizionando una piccola astronave per ognuna
    '''
    for lv in range(giocatore.vite):
        screen.blit("vita", (10 + (lv*32), 10))


def update():
    global contatore_mosse, lasers, punteggio
    if giocatore.status < 30 and len(alieni) > 0:
        controlla_tasti()
        aggiorna_lasers()
        contatore_mosse += 1
        # Aggiunto ritardo nell'aggiornamento
        if contatore_mosse == ritardo_mossa:
            aggiorna_alieni()
            contatore_mosse = 0
        # Se il giocatore è colpito...
        # Inizia l'animazione incrementando status fino a 30
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
    '''
    Gestisce il movimento dx-sx e lo sparo
    mantenendo i margini (40 - 760)
    '''
    global lasers
    if keyboard.left:
        if giocatore.x > 40: giocatore.x -= 5
    if keyboard.right:
        if giocatore.x < 760: giocatore.x += 5
    if keyboard.space:
        if giocatore.laser_attivo == 1:
            giocatore.laser_attivo = 0
            # https://pygame-zero.readthedocs.io/en/stable/builtins.html#sounds
            sounds.laser.play()
            clock.schedule(attiva_laser, 1.0)
            l = len(lasers)
            # Il laser parte dalla posizione dell'astronave 
            # (un po' più sù per la precisione)
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
            # Il laser degli alieni si muove dal'alto verso il basso
            alieno_colpisce(laser)
            laser.y += 2
            if laser.y > HEIGHT:
                laser.status = 1
        if laser.type == 1:
            giocatore_colpisce(laser)
            # Il laser del giocatore si muove dal basso verso l'alto
            laser.y -= 5
            if laser.y < 10:
                laser.status = 1
    # Pulizia liste
    alieni = pulizia_lista(alieni)
    lasers = pulizia_lista(lasers)


def pulizia_lista(l):
    '''
    Pulizia oggetti usando lo status
    Ricreo una lista solo con quelli con status a 0
    '''
    nuova_lista = []
    for i in range(len(l)):
        if l[i].status == 0: nuova_lista.append(l[i])
    return nuova_lista

def giocatore_colpisce(laser):
    '''
    Gestita la collisione, setto lo status del laser a 1 per la sua eliminazione
    '''
    global punteggio
    for alieno in alieni:
        if alieno.collidepoint(laser.x, laser.y):
            # https://pygame-zero.readthedocs.io/en/stable/builtins.html#sounds
            sounds.eep.play()
            laser.status = 1
            alieno.status = 1
            punteggio += 100


def alieno_colpisce(laser):
    '''
    Gestita la collisione, setto lo status del laser a 1 per la sua eliminazione
    '''
    if giocatore.collidepoint(laser.x, laser.y):
        giocatore.status = 1
        laser.status = 1
        # https://pygame-zero.readthedocs.io/en/stable/builtins.html#sounds
        sounds.explosion.play()


def init_alieni():
    '''
    Creazione degli alieni:
    - posizione, immagine, status
    '''
    global alieni
    alieni = []
    for a in range(18):
        # Tre file da 6
        # int(a/6) è il trucco per disporli su file
        alienoX = 210 + (a % 6) * 80
        alienoY = 100 + int(a/6) * 64
        alieni.append(Actor("alieno1", (alienoX, alienoY)))
        alieni[a].status = 0


def mostra_alieni():
    '''
    Richiama la draw per tutti gli alieni
    '''
    for alien in alieni:
        alien.draw()


def aggiorna_alieni():
    global sequenza_mosse, lasers
    move_x = move_y = 0
    # sequenza_mosse viene incrementata fino a 40 e poi si azzera
    # Movimento a sinistra
    if sequenza_mosse < 10 or sequenza_mosse > 30:
        move_x = -15
    # Movimento in basso
    if sequenza_mosse == 10 or sequenza_mosse == 30:
        move_y = 50
    # Movimento a destra
    if sequenza_mosse > 10 and sequenza_mosse < 30:
        move_x = 15

    for alien in alieni:
        # Animazione oggetti: animate
        # https://pygame-zero.readthedocs.io/en/stable/builtins.html
        # tween = interpolazione
        animate(
            alien, pos=(alien.x + move_x, alien.y + move_y),
            duration = 0.5, tween = "linear"
        )
        # Immagine casuale tra le due disponibile, movimenta!
        if randint(0,1) == 0:
            alien.image = "alieno1"
        else:
            alien.image = "alieno1b"
            # Spara laser 
            if randint(0, 10) == 0:
                l = len(lasers)
                # Dal basso (midbottom) dell'alieno
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
    # Lista di possibili immagini del giocatore
    # indice 0 quando sta giocando
    # indice da 1 a 5 quando esplode
    giocatore.images = ["giocatore","explosion1","explosion2","explosion3","explosion4","explosion5"]
    init_alieni()
    lasers = []

init_game()
pgzrun.go()