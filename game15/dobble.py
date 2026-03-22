import pgzrun
from random import shuffle

TITLE = "Dobble"
WIDTH = 1000
HEIGHT = 700
TEMPO_ROUND = 30
PUNTEGGIO_OBIETTIVO = 8
VITE_INIZIALI = 3

# Barra in alto e area messaggi
barra_superiore = Rect(20, 20, 960, 70)
area_messaggi = Rect(190, 105, 620, 55)
area_regole = Rect(220, 155, 560, 110)

# Pulsanti del menu e di fine partita
bottone_start = Rect(380, 610, 240, 60)
bottone_rigioca = Rect(380, 560, 240, 60)

# Due carte principali
carta_sinistra = Rect(60, 180, 400, 480)
carta_destra = Rect(540, 180, 400, 480)

# Box cliccabili della carta sinistra
box_sinistra_1 = Rect(85, 215, 150, 100)
box_sinistra_2 = Rect(285, 215, 150, 100)
box_sinistra_3 = Rect(85, 325, 150, 100)
box_sinistra_4 = Rect(285, 325, 150, 100)
box_sinistra_5 = Rect(85, 435, 150, 100)
box_sinistra_6 = Rect(285, 435, 150, 100)
box_sinistra_7 = Rect(85, 545, 150, 100)
box_sinistra_8 = Rect(285, 545, 150, 100)

# Box cliccabili della carta destra
box_destra_1 = Rect(565, 215, 150, 100)
box_destra_2 = Rect(765, 215, 150, 100)
box_destra_3 = Rect(565, 325, 150, 100)
box_destra_4 = Rect(765, 325, 150, 100)
box_destra_5 = Rect(565, 435, 150, 100)
box_destra_6 = Rect(765, 435, 150, 100)
box_destra_7 = Rect(565, 545, 150, 100)
box_destra_8 = Rect(765, 545, 150, 100)

box_carta_sinistra = [
    box_sinistra_1,
    box_sinistra_2,
    box_sinistra_3,
    box_sinistra_4,
    box_sinistra_5,
    box_sinistra_6,
    box_sinistra_7,
    box_sinistra_8,
]

box_carta_destra = [
    box_destra_1,
    box_destra_2,
    box_destra_3,
    box_destra_4,
    box_destra_5,
    box_destra_6,
    box_destra_7,
    box_destra_8,
]

# Round pronti: 8 simboli a sinistra, 8 a destra, 1 simbolo uguale
rounds_raw = [
    "sole;gatto;albero;luna;cane;stella;treno;fiore|pesce;chiave;luna;cuore;libro;nuvola;mela;razzo|luna",
    "occhio;pane;robot;scarpa;sole;gatto;fiore;treno|banana;chiave;scarpa;cuore;libro;nuvola;mela;razzo|scarpa",
    "pesce;chiave;cuore;libro;albero;gatto;cane;banana|sole;stella;treno;fiore;occhio;pane;banana;razzo|banana",
    "sole;pesce;occhio;mela;cane;stella;treno;fiore|gatto;albero;luna;nuvola;mela;chiave;cuore;libro|mela",
    "robot;banana;libro;cuore;sole;stella;treno;fiore|occhio;pane;scarpa;gatto;albero;luna;robot;pesce|robot",
    "razzo;mela;libro;chiave;sole;gatto;cane;stella|nuvola;cuore;pesce;occhio;pane;scarpa;banana;chiave|chiave",
    "treno;fiore;sole;albero;luna;cane;robot;banana|pesce;chiave;cuore;libro;nuvola;mela;razzo;treno|treno",
    "occhio;pane;scarpa;robot;banana;sole;gatto;albero|luna;cane;stella;fiore;pesce;cuore;libro;occhio|occhio",
    "nuvola;mela;razzo;pesce;sole;treno;fiore;cane|gatto;albero;luna;chiave;cuore;libro;razzo;banana|razzo",
    "stella;treno;fiore;pesce;chiave;cuore;libro;nuvola|sole;gatto;albero;luna;cane;mela;razzo;stella|stella",
    "pane;scarpa;robot;banana;sole;gatto;albero;luna|cane;stella;treno;fiore;pesce;chiave;cuore;pane|pane",
]

# Simboli che hanno gia' un'immagine nella cartella images
simboli_con_immagine = [
    "sole",
    "gatto",
    "albero",
    "luna",
    "cane",
    "stella",
    "treno",
    "fiore",
    "pesce",
    "chiave",
    "cuore",
    "libro",
    "nuvola",
    "mela",
    "razzo",
    "occhio",
    "pane",
    "scarpa",
    "robot",
    "banana",
]

stato_gioco = "menu"
punteggio = 0
vite = VITE_INIZIALI
secondi_mancanti = TEMPO_ROUND
messaggio = "Premi START per iniziare."
indice_round = 0
rounds = []
round_corrente = ""
simboli_sinistra = []
simboli_destra = []
simbolo_comune = ""
messaggio_finale = ""


def prepara_rounds():
    global rounds
    rounds = []
    for testo_round in rounds_raw:
        rounds.append(testo_round)
    shuffle(rounds)


def leggi_prossimo_round():
    global indice_round, round_corrente
    indice_round = indice_round + 1
    round_corrente = rounds.pop(0)
    return round_corrente.split("|")


def carica_round():
    global simboli_sinistra, simboli_destra, simbolo_comune, secondi_mancanti, messaggio
    if punteggio >= PUNTEGGIO_OBIETTIVO:
        vittoria()
        return

    if not rounds:
        # Regola semplice: se i round finiscono prima del punteggio obiettivo, la partita termina.
        fine_gioco("Round finiti!")
        return

    dati_round = leggi_prossimo_round()
    simboli_sinistra = dati_round[0].split(";")
    simboli_destra = dati_round[1].split(";")
    simbolo_comune = dati_round[2]
    secondi_mancanti = TEMPO_ROUND
    messaggio = "Trova il simbolo uguale."


def avvia_partita():
    global stato_gioco, punteggio, vite, secondi_mancanti, messaggio, indice_round, messaggio_finale
    global simboli_sinistra, simboli_destra, simbolo_comune, round_corrente
    punteggio = 0
    vite = VITE_INIZIALI
    secondi_mancanti = TEMPO_ROUND
    messaggio = "Nuova partita iniziata."
    indice_round = 0
    messaggio_finale = ""
    simboli_sinistra = []
    simboli_destra = []
    simbolo_comune = ""
    round_corrente = ""
    stato_gioco = "gioco"
    prepara_rounds()
    carica_round()


def draw():
    if stato_gioco == "menu":
        draw_menu()
    elif stato_gioco == "gioco":
        draw_gioco()
    elif stato_gioco == "vittoria":
        draw_vittoria()
    elif stato_gioco == "game_over":
        draw_game_over()


def draw_menu():
    screen.clear()
    screen.fill((20, 70, 110))

    screen.draw.text("DOBBLE", center=(WIDTH / 2, 70), fontsize=72, color="white")
    screen.draw.text(
        "Trova il simbolo uguale tra le due carte",
        center=(WIDTH / 2, 120),
        fontsize=28,
        color="white",
    )

    screen.draw.filled_rect(area_regole, (245, 245, 220))
    screen.draw.text("Regole", center=(WIDTH / 2, 178), fontsize=30, color="black")
    screen.draw.text("Clicca il simbolo uguale nelle due carte.", center=(WIDTH / 2, 208), fontsize=24, color="black")
    screen.draw.text("Hai 3 vite, 30 secondi per round e 8 punti per vincere.", center=(WIDTH / 2, 238), fontsize=24, color="black")

    anteprima_sinistra = Rect(120, 320, 290, 220)
    anteprima_destra = Rect(590, 320, 290, 220)
    screen.draw.filled_rect(anteprima_sinistra, "white")
    screen.draw.filled_rect(anteprima_destra, "white")
    screen.draw.text("Carta sinistra", center=(anteprima_sinistra.centerx, 355), fontsize=28, color="black")
    screen.draw.text("Carta destra", center=(anteprima_destra.centerx, 355), fontsize=28, color="black")
    screen.blit("sole", (anteprima_sinistra.x + 60, anteprima_sinistra.y + 75))
    screen.blit("luna", (anteprima_sinistra.x + 160, anteprima_sinistra.y + 75))
    screen.blit("pesce", (anteprima_destra.x + 60, anteprima_destra.y + 75))
    screen.blit("luna", (anteprima_destra.x + 160, anteprima_destra.y + 75))
    screen.draw.text("C'e' un simbolo uguale", center=(WIDTH / 2, 570), fontsize=24, color="white")

    screen.draw.filled_rect(bottone_start, "dark green")
    screen.draw.text("START", center=bottone_start.center, fontsize=36, color="white")


def draw_gioco():
    screen.clear()
    screen.fill((30, 120, 150))

    screen.draw.filled_rect(barra_superiore, (10, 45, 80))
    screen.draw.text("DOBBLE", (45, 38), fontsize=36, color="white")
    screen.draw.text("Round: " + str(indice_round), (250, 42), fontsize=26, color="white")
    screen.draw.text("Punti: " + str(punteggio), (430, 42), fontsize=26, color="white")
    screen.draw.text("Vite: " + str(vite), (585, 42), fontsize=26, color="white")
    screen.draw.text("Tempo: " + str(secondi_mancanti), (730, 42), fontsize=26, color="white")

    screen.draw.filled_rect(area_messaggi, (245, 245, 220))
    screen.draw.text(messaggio, center=area_messaggi.center, fontsize=28, color="black")

    screen.draw.filled_rect(carta_sinistra, "white")
    screen.draw.filled_rect(carta_destra, "white")
    screen.draw.text("Carta sinistra", center=(carta_sinistra.centerx, 155), fontsize=28, color="black")
    screen.draw.text("Carta destra", center=(carta_destra.centerx, 155), fontsize=28, color="black")

    disegna_carta(box_carta_sinistra, simboli_sinistra, (255, 230, 180), "black")
    disegna_carta(box_carta_destra, simboli_destra, (210, 235, 255), "black")


def draw_vittoria():
    screen.clear()
    screen.fill((30, 130, 80))

    screen.draw.text("HAI VINTO!", center=(WIDTH / 2, 170), fontsize=76, color="white")
    screen.draw.text(
        "Punteggio finale: " + str(punteggio),
        center=(WIDTH / 2, 260),
        fontsize=38,
        color="white",
    )
    screen.draw.textbox(
        "Hai trovato abbastanza simboli uguali.\nPremi il pulsante per giocare ancora.",
        Rect(250, 320, 500, 110),
        color="white",
    )

    screen.draw.filled_rect(bottone_rigioca, "dark green")
    screen.draw.text("RIGIOCA", center=bottone_rigioca.center, fontsize=38, color="white")


def draw_game_over():
    screen.clear()
    screen.fill((120, 40, 40))

    screen.draw.text("GAME OVER", center=(WIDTH / 2, 170), fontsize=76, color="white")
    screen.draw.text(
        "Punteggio finale: " + str(punteggio),
        center=(WIDTH / 2, 260),
        fontsize=38,
        color="white",
    )

    box_finale = Rect(220, 320, 560, 110)
    screen.draw.filled_rect(box_finale, (245, 235, 220))
    screen.draw.textbox(messaggio_finale, box_finale, color="black")

    screen.draw.filled_rect(bottone_rigioca, "dark green")
    screen.draw.text("RIGIOCA", center=bottone_rigioca.center, fontsize=38, color="white")


def disegna_carta(lista_box, lista_simboli, colore_box, colore_testo):
    indice = 0
    for box in lista_box:
        screen.draw.filled_rect(box, colore_box)
        if indice < len(lista_simboli):
            disegna_simbolo(box, lista_simboli[indice], colore_testo)
        indice = indice + 1


def disegna_simbolo(box, simbolo, colore_testo):
    if simbolo in simboli_con_immagine:
        screen.blit(simbolo, (box.centerx - 36, box.y + 8))
        screen.draw.text(
            simbolo,
            center=(box.centerx, box.y + 82),
            fontsize=20,
            color=colore_testo,
        )
    else:
        screen.draw.text(simbolo, center=box.center, fontsize=22, color=colore_testo)


def update():
    pass


def on_mouse_down(pos):
    if stato_gioco == "menu":
        if bottone_start.collidepoint(pos):
            avvia_partita()
        return

    if stato_gioco == "vittoria" or stato_gioco == "game_over":
        if bottone_rigioca.collidepoint(pos):
            avvia_partita()
        return

    if stato_gioco != "gioco":
        return

    indice = 0
    for box in box_carta_sinistra:
        if box.collidepoint(pos):
            controlla_risposta(simboli_sinistra[indice])
            return
        indice = indice + 1

    indice = 0
    for box in box_carta_destra:
        if box.collidepoint(pos):
            controlla_risposta(simboli_destra[indice])
            return
        indice = indice + 1


def controlla_risposta(simbolo_selezionato):
    global punteggio, vite, messaggio
    if stato_gioco != "gioco":
        return

    if simbolo_selezionato == simbolo_comune:
        punteggio = punteggio + 1
        messaggio = "Corretto!"
        if punteggio >= PUNTEGGIO_OBIETTIVO:
            vittoria()
        else:
            carica_round()
    else:
        vite = vite - 1
        messaggio = "Sbagliato!"
        if vite <= 0:
            fine_gioco("Hai perso tutte le vite.")
        else:
            carica_round()


def fine_gioco(testo):
    global stato_gioco, messaggio_finale
    stato_gioco = "game_over"
    messaggio_finale = testo


def vittoria():
    global stato_gioco, messaggio_finale
    stato_gioco = "vittoria"
    messaggio_finale = "Hai completato l'obiettivo."


def update_secondi_mancanti():
    global secondi_mancanti, vite, messaggio
    if stato_gioco != "gioco":
        return

    if secondi_mancanti > 0:
        secondi_mancanti = secondi_mancanti - 1

    if secondi_mancanti <= 0:
        vite = vite - 1
        messaggio = "Tempo scaduto!"
        if vite <= 0:
            fine_gioco("Tempo scaduto e vite finite.")
        else:
            carica_round()


clock.schedule_interval(update_secondi_mancanti, 1)
pgzrun.go()
