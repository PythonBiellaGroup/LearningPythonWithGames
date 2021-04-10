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


def update():
    pass

def on_mouse_down(pos):
    pass

def risposta_corretta():
    pass

def game_over():
    pass

def update_secondi_mancanti():
    pass

clock.schedule_interval(update_secondi_mancanti, 1)

pgzrun.go()