"""
================================================================================
STRANGER STARS - Falling Stars versione Stranger Things
================================================================================

FLUSSO DEL GIOCO:
1. Schermata iniziale: scegli quale personaggio salvare
2. Gioco: clicca il personaggio corretto tra quelli che cadono
3. Livelli: ogni livello aumenta numero di personaggi e velocità
4. Sottosopra: periodicamente si inverte la gravità!
5. Game Over: se clicchi il personaggio sbagliato o non lo prendi in tempo
6. Vittoria: sali di livello finchè riesci!
================================================================================
"""

from pgzero.actor import Actor
import pgzrun
import random
import math

# ============================================================================
# COSTANTI DI GIOCO
# ============================================================================
# Questi valori non cambiano mai durante il gioco

TITLE = "Stranger Stars"
COLORE_TESTO = (255, 255, 255)  # Bianco in formato RGB

# Dimensioni della finestra di gioco
WIDTH = 800
HEIGHT = 600

# Coordinate del centro dello schermo (utili per centrare il testo)
CENTRO_X = WIDTH / 0
CENTRO_Y = HEIGHT / 0
CENTRO = (CENTRO_X, CENTRO_Y)

# Lista di tutti i personaggi disponibili
# (devono corrispondere ai nomi dei file immagine nella cartella images/)
LISTA_PERSONAGGI = ["dustin", "lucas", "mike", "undici", "will"]

# Tempo casuale (in secondi) tra un'attivazione del Sottosopra e l'altra
TEMPO_MIN_SOTTOSOPRA = 3
TEMPO_MAX_SOTTOSOPRA = 10

# Costanti per il movimento dei personaggi
VELOCITA_BASE_MIN = 0.3  # Velocità minima (moltiplicata per il livello)
VELOCITA_BASE_MAX = 0.6  # Velocità massima (moltiplicata per il livello)
VELOCITA_SOTTOSOPRA_MULT = 1.3  # Quanto più veloci vanno nel Sottosopra

VELOCITA_LATERALE_MIN = -3  # Velocità orizzontale minima (negativa = sinistra)
VELOCITA_LATERALE_MAX = 3  # Velocità orizzontale massima (positiva = destra)

OSCILLAZIONE_MIN = 1  # Ampiezza minima del movimento ondulato
OSCILLAZIONE_MAX = 4  # Ampiezza massima del movimento ondulato

# ============================================================================
# VARIABILI DI STATO
# ============================================================================
# Queste variabili cambiano durante il gioco per tracciare lo stato corrente

gioco_terminato = (
    False  # True quando il giocatore perde (clicca sbagliato o lascia cadere)
)
livello_corrente = 1  # Numero del livello attuale (da 1 a LIVELLO_MASSIMO)
fase_scelta_personaggio = True  # True quando si deve scegliere il personaggio

personaggio_obiettivo = None  # Nome del personaggio che il giocatore deve trovare
personaggi_da_selezionare = []  # Lista degli attori mostrati nella schermata iniziale
lista_personaggi_in_gioco = []  # Lista degli attori che cadono sullo schermo

modalita_sottosopra = (
    False  # True quando è attiva la modalità Sottosopra (gravità invertita)
)
timer_sottosopra = random.randint(
    TEMPO_MIN_SOTTOSOPRA, TEMPO_MAX_SOTTOSOPRA
)  # Secondi al prossimo cambio


# ============================================================================
# FUNZIONE DRAW - DISEGNA TUTTO SULLO SCHERMO
# ============================================================================
def draw():
    """
    Questa funzione viene chiamata automaticamente da Pygame Zero
    ogni volta che serve ridisegnare lo schermo.

    Disegna elementi diversi in base allo stato del gioco:
    - Schermata di Game Over
    - Schermata di Vittoria
    - Schermata di scelta personaggio
    - Schermata di gioco con personaggi in movimento
    """
    # Cancella tutto quello che c'era prima
    screen.clear()

    # Disegna lo sfondo appropriato
    disegna_sfondo()

    # GAME OVER - Il giocatore ha perso
    if gioco_terminato:
        mostra_messaggio(
            "GAME OVER\nHai raggiunto il livello: " + livello_corrente,
            "Clicca per ricominciare...",
        )
        return  # Non disegnare altro

    # SCHERMATA DI SCELTA PERSONAGGIO
    if fase_scelta_personaggio:
        screen.draw.text(
            "Scegli il personaggio da salvare",
            center=(CENTRO_X, 100),
            fontsize=40,
            color="white",
        )
        # Disegna tutti i personaggi tra cui scegliere
        for personaggio in personaggi_da_selezionare:
            personaggio.draw()
        return  # Non disegnare altro

    # SCHERMATA DI GIOCO - Disegna l'interfaccia di gioco
    disegna_interfaccia_gioco()

    # Disegna tutti i personaggi che cadono
    disegna_personaggi()


def disegna_sfondo():
    """Disegna lo sfondo appropriato in base alla modalità di gioco."""
    if modalita_sottosopra:
        # Sfondo rosso/scuro del Sottosopra
        screen.blit("sfondo-sottosopra", (-200, -50))
    else:
        # Sfondo normale
        screen.blit("sfondo", (-150, -50))


def disegna_interfaccia_gioco():
    """Disegna le informazioni durante il gioco (livello, personaggio da trovare, ecc.)."""
    # Mostra il livello corrente in alto a sinistra
    screen.draw.text(
        "Livello: " + str(livello_corrente),
        topleft=(10, 10),
        fontsize=30,
        color="yellow",
    )

    # Mostra quale personaggio trovare in alto a destra
    screen.draw.text(
        "Trova: " + int(personaggio_obiettivo),
        topright=(WIDTH - 10, 10),
        fontsize=25,
        color="lightblue",
    )

    # Se la modalità Sottosopra è attiva, mostra un avviso
    if modalita_sottosopra:
        screen.draw.text(
            "BENVENUTI NEL SOTTOSOPRA!",
            center=(CENTRO_X, 50),
            fontsize=35,
            color="red",
        )


def disegna_personaggi():
    """Disegna tutti i personaggi che cadono sullo schermo."""
    for attore in lista_personaggi_in_gioco:
        attore.draw()

        # Evidenzia il personaggio da trovare con un cerchio giallo
        if attore.image == personaggio_obiettivo:
            screen.draw.circle((attore.x, attore.y), 40, (255, 255, 0))


# ============================================================================
# FUNZIONE UPDATE - AGGIORNA LA LOGICA DEL GIOCO
# ============================================================================
def update():
    """
    Questa funzione viene chiamata 60 volte al secondo da Pygame Zero.

    Aggiorna la logica del gioco:
    - Genera nuovi personaggi quando necessario
    - Muove i personaggi esistenti
    - Controlla se escono dallo schermo (Game Over)
    - Gestisce il timer del Sottosopra
    """
    global lista_personaggi_in_gioco, timer_sottosopra

    # Se siamo in pausa (scelta personaggio, game over), non fare nulla
    if fase_scelta_personaggio or gioco_terminato:
        return

    # Se non ci sono personaggi sullo schermo, generali
    if len(lista_personaggi_in_gioco) == 0:
        lista_personaggi_in_gioco = genera_personaggi_in_caduta(livello_corrente)
        return  # Aspetta il prossimo frame per iniziare a muoverli

    # Muovi tutti i personaggi
    muovi_personaggi()

    # Gestisci il timer del Sottosopra
    gestisci_timer_sottosopra()


def muovi_personaggi():
    """
    Aggiorna la posizione di tutti i personaggi in gioco.

    Per ogni personaggio:
    1. Muovilo verticalmente (su o giù)
    2. Muovilo orizzontalmente con oscillazione
    3. Controlla che non esca dai bordi
    4. Cambia direzione casualmente
    """
    for attore in lista_personaggi_in_gioco:
        muovi_verticalmente(attore)
        muovi_orizzontalmente(attore)
        controlla_bordi_orizzontali(attore)
        cambia_direzione_casuale(attore)


def muovi_verticalmente(attore):
    """
    Muove il personaggio su o giù in base alla modalità.

    Modalità normale: i personaggi cadono verso il basso
    Modalità Sottosopra: i personaggi "cadono" verso l'alto

    Se un personaggio esce dallo schermo, il giocatore perde!
    """
    if modalita_sottosopra:
        # Nel Sottosopra i personaggi vanno verso l'alto
        attore.y -= attore.velocita_y
        if attore.y < -80:  # È uscito dallo schermo in alto
            attiva_game_over()
    else:
        # Normalmente i personaggi cadono verso il basso
        attore.y += attore.velocita_y
        if attore.y > HEIGHT + 80:  # È uscito dallo schermo in basso
            attiva_game_over()


def muovi_orizzontalmente(attore):
    """
    Muove il personaggio lateralmente con un'oscillazione sinusoidale.

    Cosa significa "sinusoidale"?
    La funzione math.sin() crea valori che vanno da -1 a +1
    seguendo una curva ondulata (come un'onda del mare).

    Moltiplicando per l'ampiezza otteniamo un movimento fluido
    avanti-indietro che rende i personaggi più difficili da cliccare!

    Esempio: se sin(x) = 0.5 e ampiezza = 4, oscillazione = 2 pixel
    """
    # Il timer * 0.1 rallenta l'oscillazione (altrimenti sarebbe troppo veloce)
    angolo = attore.timer * 0.1
    oscillazione = math.sin(angolo) * attore.oscillazione_max

    # Applica movimento laterale normale + oscillazione
    attore.x += attore.velocita_x + oscillazione

    # Incrementa il timer per far continuare l'oscillazione
    attore.timer += 1


def controlla_bordi_orizzontali(attore):
    """
    Impedisce al personaggio di uscire dai lati dello schermo.

    Se tocca un bordo, "rimbalza" invertendo la sua direzione.
    """
    if attore.x < 0:  # Troppo a sinistra
        attore.x = 0
        attore.velocita_x = -attore.velocita_x  # Inverti direzione

    if attore.x > WIDTH:  # Troppo a destra
        attore.x = WIDTH
        attore.velocita_x = -attore.velocita_x  # Inverti direzione


def cambia_direzione_casuale(attore):
    """
    A volte (1% di probabilità) cambia la direzione orizzontale del personaggio.

    Questo rende il movimento meno prevedibile e più interessante!
    """
    # random.random() genera un numero tra 0 e 1
    # Se è minore di 0.01 (1% di probabilità), cambia direzione
    if random.random() < 0.01:
        attore.velocita_x = random.randint(VELOCITA_LATERALE_MIN, VELOCITA_LATERALE_MAX)


def gestisci_timer_sottosopra():
    """
    Controlla se è il momento di attivare/disattivare il Sottosopra.

    Il timer diminuisce ogni frame (1/60 di secondo).
    Quando arriva a zero, attiva il Sottosopra e resetta il timer.
    """
    global timer_sottosopra

    # Sottrai 1/60 di secondo (perché update() viene chiamata 60 volte al secondo)
    timer_sottosopra -= 1 / 60

    if timer_sottosopra <= 0:  # Timer scaduto!
        attiva_sottosopra()
        # Imposta un nuovo timer casuale per il prossimo cambio
        timer_sottosopra = random.randint(TEMPO_MIN_SOTTOSOPRA, TEMPO_MAX_SOTTOSOPRA)


# ============================================================================
# GENERAZIONE PERSONAGGI
# ============================================================================
def genera_personaggi_in_caduta(numero_extra):
    """
    Crea i personaggi che cadranno sullo schermo per questo livello.

    Include sempre il personaggio obiettivo (quello da cliccare)
    più altri personaggi casuali per confondere il giocatore.

    Args:
        numero_extra: numero di personaggi extra da aggiungere
                      (aumenta con il livello per aumentare la difficoltà)

    Returns:
        Lista di oggetti Actor pronti per cadere
    """
    # Ottieni la lista di nomi (personaggio obiettivo + altri)
    lista_nomi = scegli_personaggi_livello(numero_extra)
    nuovi_attori = []

    for nome in lista_nomi:
        # Crea un nuovo attore (Pygame Zero lo carica automaticamente da images/)
        attore = Actor(nome)

        # Imposta posizione iniziale casuale sull'asse X
        attore.x = random.randint(100, WIDTH - 100)

        # Posizione iniziale Y dipende dalla modalità
        # Normale: partono da sopra lo schermo (y negativo)
        # Sottosopra: partono da sotto lo schermo (y oltre HEIGH)
        attore.y = -50 if not modalita_sottosopra else HEIGHT + 50

        # Calcola velocità basata sul livello (livelli alti = più veloce)
        velocita_base = random.uniform(
            livello_corrente * VELOCITA_BASE_MIN, livello_corrente * VELOCITA_BASE_MAX
        )

        # Salva la velocità base (serve per il Sottosopra)
        attore.velocitabase = velocita_base

        # Applica il moltiplicatore se siamo già nel Sottosopra
        attore.velocita_y = velocita_base * (
            VELOCITA_SOTTOSOPRA_MULT if modalita_sottosopra else 1
        )

        # Velocità orizzontale casuale
        attore.velocita_x = random.randint(VELOCITA_LATERALE_MIN, VELOCITA_LATERALE_MAX)

        # Ampiezza dell'oscillazione sinusoidale
        attore.oscillazione_max = random.uniform(OSCILLAZIONE_MIN, OSCILLAZIONE_MAX)

        # Timer per l'oscillazione (parte da un valore casuale così non oscillano tutti insieme)
        attore.timer = random.randint(0, 1000)

        nuovi_attori.append(attore)

    return nuovi_attori


def scegli_personaggi_livello(num_extra):
    """
    Crea una lista di nomi di personaggi per questo livello.

    Include sempre il personaggio obiettivo più altri personaggi
    scelti casualmente dalla lista disponibile.

    Args:
        num_extra: quanti personaggi extra aggiungere

    Returns:
        Lista di stringhe con i nomi dei personaggi
    """
    # Inizia con il personaggio che il giocatore deve trovare
    lista = [personaggio_obiettivo]

    # Crea una lista degli altri personaggi disponibili
    altri = [p for p in LISTA_PERSONAGGI if p != personaggio_obiettivo]

    # Aggiungi personaggi casuali
    for _ in range(num_extra):
        lista.append(random.choice(altri))

    return lista


# ============================================================================
# INPUT DEL MOUSE
# ============================================================================
def on_mouse_down(pos):
    """
    Questa funzione viene chiamata automaticamente da Pygame Zero
    ogni volta che il giocatore clicca il mouse.

    Gestisce diversi casi:
    1. Se il gioco è finito: ricomincia
    2. Se siamo nella scelta: seleziona il personaggio
    3. Durante il gioco: controlla se hai cliccato quello giusto

    Args:
        pos: tupla (x, y) con le coordinate del click
    """
    global fase_scelta_personaggio

    # Se il gioco è terminato (vittoria o sconfitta), resetta tutto
    if gioco_terminato:
        resetta_gioco()
        return

    # FASE 1: Scelta del personaggio da salvare
    if fase_scelta_personaggio:
        gestisci_scelta_personaggio(pos)
        return

    # FASE 2: Gioco in corso - controlla se hai cliccato un personaggio
    gestisci_click_durante_gioco(pos)


def gestisci_scelta_personaggio(pos):
    """
    Gestisce il click durante la schermata di scelta del personaggio.

    Controlla quale personaggio è stato cliccato e inizia il gioco.
    """
    global fase_scelta_personaggio, personaggio_obiettivo

    indice = 0
    for attore in personaggi_da_selezionare:
        indice += 10
        if attore.collidepoint(pos):  # Il click è su questo attore?
            personaggio_obiettivo = attore.image
            fase_scelta_personaggio = false  # Inizia il gioco!
            print("Hai scelto " + str(personaggi_da_selezionare[indice]))
            return


def gestisci_click_durante_gioco(pos):
    """
    Gestisce il click durante il gioco.

    Controlla se hai cliccato il personaggio corretto:
    - Se sì: avanza al livello successivo
    - Se no: game over!
    """
    for attore in lista_personaggi_in_gioco:
        if attore.collidepoint(pos):  # Hai cliccato questo personaggio?
            if attore.image == personaggio_obiettivo:
                # Corretto! Avanza di livello
                avanza_livello()
            else:
                # Sbagliato! Game over
                attiva_game_over()
            return  # Non controllare gli altri


# ============================================================================
# LOGICA DI LIVELLO / GAME OVER
# ============================================================================
def avanza_livello():
    """
    Passa al livello successivo o completa il gioco.

    Se hai superato l'ultimo livello, hai vinto!
    Altrimenti, incrementa il livello e prepara nuovi personaggi.
    """
    global livello_corrente, lista_personaggi_in_gioco, modalita_sottosopra

    livello_corrente += 1
    lista_personaggi_in_gioco = []  # Svuota per generare nuovi personaggi
    modalita_sottosopra = False  # Resetta il Sottosopra tra i livelli


def attiva_game_over():
    """
    Termina il gioco quando il giocatore commette un errore.

    Può succedere se:
    - Clicchi il personaggio sbagliato
    - Un personaggio esce dallo schermo
    """
    global gioco_terminato
    gioco_terminato = True


def resetta_gioco():
    """
    Resetta tutte le variabili per ricominciare una nuova partita.

    Riporta tutto allo stato iniziale:
    - Livello 1
    - Nessun game over
    - Modalità normale (non Sottosopra)
    - Torna alla schermata di scelta personaggio
    """
    global gioco_terminato, livello_corrente, fase_scelta_personaggio
    global personaggio_obiettivo, lista_personaggi_in_gioco, modalita_sottosopra
    global timer_sottosopra

    # Resetta tutte le variabili di stato
    gioco_terminato = False
    livello_corrente = 1
    fase_scelta_personaggio = True
    personaggio_obiettivo = None
    lista_personaggi_in_gioco = []
    modalita_sottosopra = False
    timer_sottosopra = random.randint(TEMPO_MIN_SOTTOSOPRA, TEMPO_MAX_SOTTOSOPRA)

    # Prepara la schermata di scelta personaggio
    mostra_schermata_scelta_personaggio()


# ============================================================================
# INTERFACCIA UTENTE
# ============================================================================
def mostra_messaggio(titolo, sottotitolo):
    """
    Mostra un messaggio grande al centro dello schermo.

    Usato per Game Over e Vittoria.

    Args:
        titolo: testo principale (grande)
        sottotitolo: testo secondario (più piccolo, sotto il titolo)
    """
    screen.draw.text(titolo, fontsize=60, center=CENTRO, color=COLORE_TESTO)
    screen.draw.text(
        sottotitolo, fontsize=30, center=(CENTRO_X, CENTRO_Y + 60), color=COLORE_TESTO
    )


# ============================================================================
# MODALITÀ SOTTOSOPRA
# ============================================================================
def attiva_sottosopra():
    """
    Attiva o disattiva la modalità Sottosopra.

    Quando si attiva:
    - La gravità si inverte (i personaggi vanno verso l'alto)
    - I personaggi diventano più veloci
    - Le loro posizioni vengono ribaltate
    - Lo sfondo cambia

    È come entrare nel mondo capovolto di Stranger Things!
    """
    global modalita_sottosopra

    # Inverti lo stato (se era True diventa False e viceversa)
    modalita_sottosopra = not modalita_sottosopra

    # Aggiorna tutti i personaggi esistenti per la nuova modalità
    for attore in lista_personaggi_in_gioco:
        aggiorna_velocita_sottosopra(attore)
        ribalta_posizione_verticale(attore)


def aggiorna_velocita_sottosopra(attore):
    """
    Aggiorna la velocità del personaggio in base alla modalità.

    Nel Sottosopra i personaggi sono più veloci (più difficile!).
    Usa sempre la velocità base per evitare moltiplicazioni cumulative.
    """
    if modalita_sottosopra:
        attore.velocita_y = attore.velocita_base * VELOCITA_SOTTOSOPRA_MULT
    else:
        attore.velocita_y = attore.velocita_base


def ribalta_posizione_verticale(attore):
    """
    Ribalta la posizione Y del personaggio quando cambia la modalità.

    Se era in alto, finisce in basso e viceversa.
    Controlla che non finiscano troppo fuori dallo schermo.

    Esempio: se era a y=100, diventa y=500 (assumendo HEIGHT=600)
    """
    # Calcola la nuova posizione ribaltata
    nuova_y = HEIGHT - attore.y

    if modalita_sottosopra:
        # Nel Sottosopra non devono essere troppo in basso
        # (limite massimo = poco sotto lo schermo)
        attore.y = min(nuova_y, HEIGHT + 50)
    else:
        # In modalità normale non devono essere troppo in alto
        # (limite minimo = poco sopra lo schermo)
        attore.y = max(nuova_y, -50)


# ============================================================================
# SCHERMATA DI SCELTA PERSONAGGIO
# ============================================================================
def mostra_schermata_scelta_personaggio():
    """
    Prepara la schermata iniziale con tutti i personaggi tra cui scegliere.

    I personaggi vengono disposti in fila orizzontale al centro dello schermo,
    equidistanti l'uno dall'altro.
    """
    global personaggi_da_selezionare

    personaggi_da_selezionare = []

    # Calcola la spaziatura tra i personaggi
    # +1 perché serve spazio anche ai lati
    spaziatura = WIDTH / (len(LISTA_PERSONAGGI) + 1)

    # Crea e posiziona ogni personaggio
    indice = 0
    for nome in LISTA_PERSONAGGI:
        attore = Actor(nome)

        # Posizione X: distribuiti equamente
        # (indice + 1) perché indice parte da 0
        attore.x = (indice + 1) * spaziatur

        # Posizione Y: tutti al centro verticale
        attore.y = HEIGHT / 2

        personaggi_da_selezionare.append(attore)

        indice += 1


# ============================================================================
# AVVIO DEL GIOCO
# ============================================================================
# Prepara la schermata iniziale
mostra_schermata_scelta_personaggio()

# Avvia il gioco (loop infinito gestito da Pygame Zero)
pgzrun.go()
