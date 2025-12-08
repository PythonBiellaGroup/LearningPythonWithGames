import pgzrun
import random
import math

# COSTANTI DI GIOCO

TITOLO_GIOCO = "Stranger Python"
COLORE_TESTO = (255, 255, 255)

LARGHEZZA = 800
ALTEZZA = 600

LIVELLO_MASSIMO = 8

# Coordinate che useremo per stampare a video il testo
CENTRO_X = LARGHEZZA / 2
CENTRO_Y = ALTEZZA / 2
CENTRO = (CENTRO_X, CENTRO_Y)

# Personaggi disponibili
LISTA_PERSONAGGI = ["dustin", "lucas", "mike", "undici", "will"]

# Timer casuale per attivare il Sottosopra
TEMPO_MIN_SOTTOSOPRA = 3
TEMPO_MAX_SOTTOSOPRA = 10

# VARIABILI DI STATO

gioco_terminato = False
gioco_completato = False
livello_corrente = 1
fase_scelta_personaggio = True

personaggio_obiettivo = None
personaggi_da_selezionare = []
lista_personaggi_in_gioco = []  # gli attori che cadono a schermo

modalita_sottosopra = False
timer_sottosopra = random.randint(TEMPO_MIN_SOTTOSOPRA, TEMPO_MAX_SOTTOSOPRA)


def draw():
    screen.clear()

    # Sfondi diversi in base al mondo
    if modalita_sottosopra:
        screen.blit("sfondo-sottosopra", (-200, -50))
    else:
        screen.blit("sfondo", (-150, -50))

    # GAME OVER
    if gioco_terminato:
        mostra_messaggio("GAME OVER", "Prova di nuovo...")
        return

    # VITTORIA
    if gioco_completato:
        mostra_messaggio("HAI VINTO!", "Complimenti!")
        return

    # SCHERMATA DI SCELTA PERSONAGGIO
    if fase_scelta_personaggio:
        screen.draw.text(
            "Scegli il tuo personaggio",
            center=(CENTRO_X, 100),
            fontsize=40,
            color="white",
        )
        for personaggio in personaggi_da_selezionare:
            personaggio.draw()
        return

    # Disegna tutti i personaggi
    for attore in lista_personaggi_in_gioco:
        attore.draw()


# LOGICA DI AGGIORNAMENTO


def update():
    global lista_personaggi_in_gioco, timer_sottosopra, modalita_sottosopra

    # Se siamo in una schermata di pausa
    if fase_scelta_personaggio or gioco_terminato or gioco_completato:
        return

    # Se non ci sono attori sullo schermo → genera quelli del livello
    if len(lista_personaggi_in_gioco) == 0:
        lista_personaggi_in_gioco = genera_personaggi_in_caduta(livello_corrente)
        return

    # Aggiorna movimento di ogni personaggio
    for attore in lista_personaggi_in_gioco:
        # Movimento verticale diverso nel Sottosopra
        if modalita_sottosopra:
            attore.y -= attore.velocita_y
            if attore.y < -80:
                attiva_game_over()
        else:
            attore.y += attore.velocita_y
            if attore.y > ALTEZZA + 80:
                attiva_game_over()

        # Oscillazione orizzontale sinusoidale
        oscillazione = math.sin(attore.timer * 0.1) * attore.ampiezza_oscillazione
        attore.x += attore.velocita_x + oscillazione
        attore.timer += 1

        # Evita che escano dai bordi orizzontali
        if attore.x < 0:
            attore.x = 0
            attore.velocita_x = -attore.velocita_x
        if attore.x > LARGHEZZA:
            attore.x = LARGHEZZA
            attore.velocita_x = -attore.velocita_x

        # Piccole variazioni casuali del movimento
        if random.random() < 0.01:
            attore.velocita_x = random.randint(-3, 3)

    # Gestione timer Sottosopra
    timer_sottosopra -= 1 / 60
    if timer_sottosopra <= 0:
        attiva_sottosopra()
        timer_sottosopra = random.randint(TEMPO_MIN_SOTTOSOPRA, TEMPO_MAX_SOTTOSOPRA)


# GENERAZIONE PERSONAGGI


def genera_personaggi_in_caduta(numero_extra):
    """Genera il personaggio obiettivo + altri personaggi casuali."""
    lista_nomi = scegli_personaggi_livello(numero_extra)
    nuovi_attori = []

    for nome in lista_nomi:
        attore = Actor(nome)

        # Posizione iniziale X
        attore.x = random.randint(100, LARGHEZZA - 100)

        # Posizione iniziale Y (alto o basso nel Sottosopra)
        attore.y = -50 if not modalita_sottosopra else ALTEZZA + 50

        # Velocità verticale basata sul livello
        velocità_base = random.uniform(livello_corrente * 0.3, livello_corrente * 0.6)
        attore.velocita_y = velocità_base * (1.3 if modalita_sottosopra else 1)

        # Velocità orizzontale
        attore.velocita_x = random.randint(-3, 3)

        # Oscillazione sinusoidale
        attore.ampiezza_oscillazione = random.uniform(1, 4)
        attore.timer = random.randint(0, 1000)

        nuovi_attori.append(attore)

    return nuovi_attori


def scegli_personaggi_livello(num_extra):
    """Ritorna il personaggio obiettivo + altri casuali."""
    lista = [personaggio_obiettivo]
    altri = [p for p in LISTA_PERSONAGGI if p != personaggio_obiettivo]

    for _ in range(num_extra):
        lista.append(random.choice(altri))

    return lista


# INPUT DEL MOUSE


def on_mouse_down(pos):
    global fase_scelta_personaggio, personaggio_obiettivo, lista_personaggi_in_gioco

    # Se siamo nella schermata di scelta
    if fase_scelta_personaggio:
        for attore in personaggi_da_selezionare:
            if attore.collidepoint(pos):
                personaggio_obiettivo = attore.image
                fase_scelta_personaggio = False
                return

    # Durante il gioco: verifica se si clicca il personaggio corretto
    for attore in lista_personaggi_in_gioco:
        if attore.collidepoint(pos):
            if attore.image == personaggio_obiettivo:
                avanza_livello()
            else:
                attiva_game_over()


# LOGICA DI LIVELLO / GAME OVER


def avanza_livello():
    """Gestisce il passaggio al livello successivo."""
    global livello_corrente, lista_personaggi_in_gioco, gioco_completato

    if livello_corrente == LIVELLO_MASSIMO:
        gioco_completato = True
    else:
        livello_corrente += 1
        lista_personaggi_in_gioco = []  # per rigenerare i nuovi personaggi


def attiva_game_over():
    """Mostra la schermata di fallimento."""
    global gioco_terminato
    gioco_terminato = True


# INTERFACCIA UTENTE


def mostra_messaggio(titolo, sottotitolo):
    screen.draw.text(titolo, fontsize=60, center=CENTRO, color=COLORE_TESTO)
    screen.draw.text(
        sottotitolo,
        fontsize=30,
        center=(CENTRO_X, CENTRO_Y + 30),
        color=COLORE_TESTO,
    )


# SOTTOSOPRA


def attiva_sottosopra():
    """Attiva/disattiva la modalità Sottosopra e modifica la fisica."""
    global modalita_sottosopra

    modalita_sottosopra = not modalita_sottosopra

    for attore in lista_personaggi_in_gioco:
        attore.velocita_y *= 1.25  # più veloce nel Sottosopra
        attore.y = ALTEZZA - attore.y  # ribalta asse verticale


# SCHERMATA DI SCELTA


def mostra_schermata_scelta_personaggio():
    """Genera i personaggi da cliccare nella schermata iniziale."""
    global personaggi_da_selezionare

    personaggi_da_selezionare = []
    spaziatura = LARGHEZZA / (len(LISTA_PERSONAGGI) + 1)

    for indice, nome in enumerate(LISTA_PERSONAGGI):
        attore = Actor(nome)
        attore.x = (indice + 1) * spaziatura
        attore.y = ALTEZZA / 2
        personaggi_da_selezionare.append(attore)


# Avvia schermata iniziale
mostra_schermata_scelta_personaggio()

# Avvio del gioco Pygame Zero
pgzrun.go()
