import pgzrun

TITLE = "Quiz"
WIDTH = 870
HEIGHT = 650

# Disegna componenti della GUI progettata
scorrevole_box = Rect(0,0,880,80)
domanda_box = Rect(0,0,650,150)
timer_box = Rect(0,0,150,150)
risposta_box1 = Rect(0,0,300,150)
risposta_box2 = Rect(0,0,300,150)
risposta_box3 = Rect(0,0,300,150)
risposta_box4 = Rect(0,0,300,150)
salta_box = Rect(0,0,150,330)

# Variabili di gioco
punteggio = 0
secondi_mancanti = 10
nome_file_domande = "domande.txt"
msg_scorrevole = ""
is_game_over = False

risposte = [risposta_box1,risposta_box2,risposta_box3,risposta_box4]
domande = []
contatore_domande = 0
indice_domande = 0

# Posizionamento elementi nello schermo
scorrevole_box.move_ip(0,0)
domanda_box.move_ip(20,100)
timer_box.move_ip(700,100)
risposta_box1.move_ip(20,270)
risposta_box2.move_ip(370,270)
risposta_box3.move_ip(20,450)
risposta_box4.move_ip(370,450)
salta_box.move_ip(700,270)

def draw():
    global msg_scorrevole
    screen.clear()
    screen.fill(color="black")
    screen.draw.filled_rect(scorrevole_box, "black")
    screen.draw.filled_rect(domanda_box, "navy blue")
    screen.draw.filled_rect(timer_box, "navy blue")
    screen.draw.filled_rect(salta_box, "dark green")

    for risposta_box in risposte:
        screen.draw.filled_rect(risposta_box, "dark orange")
    
    msg_scorrevole = "Quiz ..."
    msg_scorrevole = msg_scorrevole + f"Domanda: {indice_domande} di {contatore_domande}"

    screen.draw.textbox(msg_scorrevole, scorrevole_box, color="white")
    screen.draw.textbox(
        str(secondi_mancanti),timer_box,
        color="white", shadow=(0.5, 0.5),
        scolor="dim grey"
    )
    screen.draw.textbox(
        "Salta", salta_box,
        color="black", angle=-90
    )
    screen.draw.textbox(
        domanda[0].strip(), domanda_box,
        color="white", shadow=(0.5,0.5),
        scolor="dim grey"
    )
    # domanda[0] contiene la domanda
    # domanda[1..] contiene le risposte
    indice = 1
    for risposta_box in risposte:
        screen.draw.textbox(domanda[indice].strip(), risposta_box, color="black")
        indice = indice + 1


def update():
    '''
    Funzione scorrimento scritta
    '''
    scorri_scritta()


def scorri_scritta():
    '''
    Funzione scorrimento scritta
    '''
    scorrevole_box.x = scorrevole_box.x - 2
    if scorrevole_box.right < 0:
        scorrevole_box.left = WIDTH


def leggi_domande_da_file():
    '''
    Lettura delle domande dal file .txt
    '''
    global contatore_domande, domande
    q_file=open(nome_file_domande, "r")
    for domanda in q_file:
        domande.append(domanda)
        contatore_domande = contatore_domande + 1
    q_file.close()


def leggi_prossima_domanda():
    '''
    Avanzamento indice domande
    '''
    global indice_domande
    indice_domande = indice_domande + 1
    return domande.pop(0).split("|")
    

def on_mouse_down(pos):
    '''
    Gestione del click dell'utente
    '''
    indice = 1
    for box in risposte:
        if box.collidepoint(pos):
            # int(domanda[5] è la risposta corretta
            if indice is int(domanda[5]):
                risposta_corretta()
            else:
                game_over()
        indice = indice + 1
    
    if salta_box.collidepoint(pos):
        salta_domanda()


def risposta_corretta():
    '''
    Controllo risposta
    '''
    global punteggio, domanda, secondi_mancanti, domande
    punteggio = punteggio + 1
    if domande:
        domanda = leggi_prossima_domanda()
        secondi_mancanti = 10
    else:
        game_over()


def game_over():
    '''
    Gestione della fine del gioco
    '''
    global domanda, secondi_mancanti, is_game_over
    messaggio = f"Game over!\nHai risposto a {punteggio} domande in modo corretto!"
    domanda = [messaggio, "-","-","-","-",5]
    secondi_mancanti = 0
    is_game_over = True


def salta_domanda():
    '''
    Gestione dello skip
    '''
    global domanda, secondi_mancanti
    if domande and not is_game_over:
        domanda = leggi_prossima_domanda()
        secondi_mancanti = 10
    else:
        game_over()


def update_secondi_mancanti():
    '''
    Gestione dalla visualizzazione dei secondi mancanti
    tramite clock.schedule_interval
    '''
    global secondi_mancanti
    if secondi_mancanti:
        secondi_mancanti = secondi_mancanti - 1
    else:
        game_over()


leggi_domande_da_file()
domanda = leggi_prossima_domanda()
clock.schedule_interval(update_secondi_mancanti, 1)

pgzrun.go()