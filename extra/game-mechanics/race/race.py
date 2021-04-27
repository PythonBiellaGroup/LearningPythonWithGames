# PyGame Zero Racing Game
from random import randint
import pgzrun

# First set the width and height of the window
WIDTH = 700
HEIGHT = 600

# Load in the car sprite image as an Actor object
auto = Actor("auto")
auto.pos = 250, 500 # Set the car screen position

# Some variables to control the track
VELOCITA = 4
contatore_tracciato = 0
posizione_tracciato = 250
larghezza_tracciato = 120
direzione_tracciato = False
# The following variables set up the track sprites
trackLeft = []
trackRight = [] 
# Variable to track the status of the game
stato_gioco = 0

# Pygame Zero draw function 
def draw():
    global stato_gioco
    screen.fill((128, 128, 128))
    if stato_gioco == 0:
        auto.draw()
        b = 0
        while b < len(trackLeft):
            if auto.colliderect(trackLeft[b]) or auto.colliderect(trackRight[b]):
                # Red flag time
                stato_gioco = 1
            trackLeft[b].draw()
            trackLeft[b].y += VELOCITA
            trackRight[b].draw()
            trackRight[b].y += VELOCITA
            b += 1
    if stato_gioco == 1:
        # Red Flag
        screen.blit('b_rossa', (318, 268))
    if stato_gioco == 2:
        # Chequered Flag
        screen.blit('arrivo', (318, 268))

# Pygame Zero update function
def update():
    global stato_gioco , contatore_tracciato
    if stato_gioco == 0:
        if keyboard.left:
            auto.x -= 2
        elif keyboard.right:
            auto.x += 2
        aggiorna_tracciato()
    if contatore_tracciato > 200:
        # Chequered flag time
        stato_gioco = 2

# Our game functions

# Function to make a new section of track
def crea_tracciato():
    global contatore_tracciato, trackLeft, trackRight, posizione_tracciato, larghezza_tracciato
    trackLeft.append(Actor("barriera", pos = (posizione_tracciato-larghezza_tracciato,0)))
    trackRight.append(Actor("barriera", pos = (posizione_tracciato+larghezza_tracciato,0)))
    contatore_tracciato += 1
    
# Function to update where the track blocks appear
def aggiorna_tracciato():
    global contatore_tracciato, posizione_tracciato, direzione_tracciato, larghezza_tracciato 
    if trackLeft[len(trackLeft)-1].y > 32:
        if direzione_tracciato == False:
            posizione_tracciato += 16
        if direzione_tracciato == True:
            posizione_tracciato -= 16
            
        if randint(0, 4) == 1:
            direzione_tracciato = not direzione_tracciato
        if posizione_tracciato > 700-larghezza_tracciato:
            direzione_tracciato = True
        if posizione_tracciato < larghezza_tracciato:
            direzione_tracciato = False
        crea_tracciato()
                            
# End of functions
                
crea_tracciato() # Make first block of track
pgzrun.go()

	

        
