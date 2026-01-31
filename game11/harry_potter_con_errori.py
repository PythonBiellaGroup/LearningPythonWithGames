# ========================================================================
# LA BATTAGLIA FINALE - HARRY VS VOLDEMORT
# ========================================================================

import random
import polars as pl  # Libreria per gestire dati in formato tabellare (come Excel/CSV)
import pgzrun
from pgzero.actor import Actor
from pgzero.clock import clock

# ===== CONFIGURAZIONE INIZIALE =====
# Queste costanti definiscono le dimensioni della finestra di gioco
WIDTH = 800  # Larghezza in pixel
HEIGHT = 600  # Altezza in pixel
TITLE = "La Battaglia Finale: Harry vs Voldemort"  # Titolo della finestra

# ===== VARIABILI GLOBALI DI STATO =====
# Punti vita di ciascun personaggio (sostituiti i dizionari con variabili singole)
punti_vita_harry = 100
punti_vita_voldemort = 100

# Valori visualizzati nelle barre (aggiornati gradualmente per animazioni fluide)
display_punti_vita_harry = 100
display_punti_vita_voldemort = 100

# Variabili che controllano il flusso del gioco
messaggio = "VOLDEMORT è apparso!"
descrizione = "Cosa farà HARRY?"
attesa_input = True  # True = è il turno del giocatore, False = animazione in corso
gioco_attivo = True  # True = partita in corso, False = qualcuno ha vinto
opzioni_correnti = None  # Conterrà i 4 incantesimi casuali del turno corrente

# ===== CREAZIONE DEGLI SPRITE (PERSONAGGI GRAFICI) =====
harry_sprite = actor("harry", (200, 320))
voldy_sprite = Actor("voldemort", (600, 100))

# Variabile per salvare chi ha vinto la partita
vincitore = None

# ===== CARICAMENTO DATI ESTERNI =====
# Legge il file CSV contenente tutti gli incantesimi disponibili
incantesimi_df = pl.read_csv("spells.xlsx")


# ========================================================================
# FUNZIONI DI SUPPORTO
# ========================================================================


def ottieni_opzioni(personaggio):
    """
    Filtra il DataFrame per ottenere solo gli incantesimi di un personaggio.

    DIDATTICA: Questa funzione usa Polars per filtrare righe, come si farebbe
    con Excel usando i filtri. Restituisce solo le righe dove la colonna
    "character" corrisponde al personaggio richiesto.

    Args:
        personaggio (str): "Harry" o "Voldemort"

    Returns:
        DataFrame Polars con solo gli incantesimi del personaggio
    """
    return incantesimi_df.filter(pl.col("charac") == personaggio)


# ========================================================================
# EFFETTI VISIVI
# ========================================================================


def flash_danno(sprite):
    """
    Crea un effetto visivo quando un personaggio subisce danni.
    Lo sprite vibra orizzontalmente e lampeggia 3 volte.

    Questa funzione dimostra l'uso di:
    - animate(): anima proprietà dell'oggetto (es. posizione X)
    - clock.schedule_unique(): esegue codice dopo un certo tempo
    - lambda: funzione anonima per codice breve
    - setattr(): modifica attributi di un oggetto dinamicamente

    Args:
        sprite (Actor): lo sprite da animare
    """
    x_originale = sprite.x  # Salva posizione X iniziale

    # Anima lo spostamento orizzontale con effetto "rimbalzo"
    animate(sprite, duration=0.5, x=x_originale + 10, tween="bounce_end")

    # Ciclo che fa lampeggiare lo sprite 3 volte
    for i in range(3):
        clock.schedule_unique(lambda: setattr(sprite, "opacity", 0), i * 0.5)
        clock.schedule_unique(lambda: setattr(sprite, "opacity", 255), i * 0.5 + 0.1)

    # Dopo 0.6 secondi ripristina la posizione originale
    clock.schedule_unique(lambda: setattr(sprite, "x", x_originale), 0.6)


# ========================================================================
# LOGICA DI GIOCO
# ========================================================================


def reset_gioco():
    """
    Ripristina tutte le variabili allo stato iniziale per una nuova partita.
    """
    global \
        punti_vita_harry, punti_vita_voldemort, \
        display_punti_vita_harry, display_punti_vita_voldemort, \
        messaggio, \
        descrizione, \
        attesa_input, \
        gioco_attivo, \
        vincitore

    # Resetta i punti vita (sia reali che visualizzati)
    punti_vita_harry = 100
    punti_vita_voldemort = 100
    display_punti_vita_harry = 100
    display_punti_vita_voldemort = 100

    # Resetta i messaggi
    messaggio = "Nuovo Duello!"
    descrizione = "Cosa farà HARRY?"

    # Resetta lo stato del gioco
    attesa_input = True
    gioco_attivo = True
    vincitore = None

    # Ripristina grafica degli sprite
    harry_sprite.opacity = 255  # Completamente visibile
    harry_sprite.pos = (200, 320)  # Posizione originale
    voldy_sprite.opacity = 255
    voldy_sprite.pos = (600, 100)


def update():
    """
    Funzione chiamata automaticamente da Pygame Zero ogni frame (60 volte/sec).
    Aggiorna le barre della vita facendole scorrere verso il valore reale.
    """
    global display_punti_vita_voldemort

    # Velocità di aggiornamento della barra
    velocita = "1"

    # Anima barra Harry
    if display_punti_vita_harry > punti_vita_harry:
        display_punti_vita_harry = max(display_punti_vita_harry - velocita, punti_vita_harry)
    elif display_punti_vita_harry < punti_vita_harry:
        display_punti_vita_harry = min(display_punti_vita_harry + velocita, punti_vita_harry)

    # Anima barra Voldemort
    if display_punti_vita_voldemort > punti_vita_voldemort:
        display_punti_vita_voldemort = max(display_punti_vita_voldemort - velocita, punti_vita_voldemort)
    elif display_punti_vita_voldemort < punti_vita_voldemort:
        display_punti_vita_voldemort = min(display_punti_vita_voldemort + velocita, punti_vita_voldemort)


def esegui_mossa(nome_attaccante, nome_difensore, df_incantesimi, indice_incantesimo):
    """
    Gestisce l'esecuzione di un incantesimo: calcola danni/cure e aggiorna lo stato.

    Questa è la funzione centrale del gioco. Mostra:
    - Accesso ai dati del DataFrame con [riga, colonna]
    - Logica condizionale (if/else)
    - Uso di random.random() per probabilità
    - Manipolazione di variabili globali
    """
    global messaggio, descrizione, gioco_attivo, vincitore, punti_vita_harry, punti_vita_voldemort

    # ===== ESTRAZIONE DATI DAL CSV =====
    # Accediamo alla riga specificata e prendiamo i valori delle colonne
    danno = float(df_incantesimi["damage", indice_incantesimo])
    precisione = float(df_incantesimi[indice_incantesimo, "precision"])
    nome_incantesimo = df_incantesimi[indice_incantesimo, "spell"].upper()

    # Aggiorna il messaggio principale
    messaggio = f"{nome_attaccante.upper()} usa {nome_incantesimo}!"

    # ===== CALCOLO SUCCESSO =====
    # random.random() restituisce un numero tra 0 e 1
    # Se è minore della precisione (es. 0.8 = 80%), l'incantesimo riesce
    successo = random.random() < precisione

    if successo:
        # ===== CASO 1: INCANTESIMO DI CURA (danno negativo) =====
        if danno < 0:
            quantita = abs(danno)
            if nome_attaccante == "Harry":
                punti_vita_harry = min(100, punti_vita_harry + quantita)
            else:
                punti_vita_voldemort = min(100, punti_vita_voldemort + quantita)
            descrizione = f"Ha recuperato {quantita} PV!"

        # ===== CASO 2: INCANTESIMO DI ATTACCO (danno positivo) =====
        else:
            if nome_difensore == "Harry":
                punti_vita_harry = max(0, punti_vita_harry - danno)
                flash_danno(harry_sprite)
            else:
                punti_vita_voldemort = max(0, punti_vita_voldemort - danno)
                flash_danno(voldy_sprite)
            descrizione = f"Ha inflitto {danno} danni!"

    # ===== CASO 3: INCANTESIMO FALLITO =====
    else:
        descrizione = "L'incantesimo è fallito!"

    # ===== CONTROLLO VITTORIA =====
    if punti_vita_harry <= 0:
        vincitore = "Voldemort"
        clock.schedule_unique(termina_gioco, 2.0)
    elif punti_vita_voldemort <= 0:
        vincitore = "Harry"
        clock.schedule_unique(termina_gioco, 2.0)


def termina_gioco():
    """Funzione che termina il gioco dopo aver mostrato l'ultima animazione."""
    global gioco_attivo
    gioco_attivo = False


def fase_voldemort():
    """Voldemort sceglie un incantesimo casuale."""
    # Se il gioco è finito, non fare nulla
    if not gioco_attivo:
        return

    # Ottiene tutti gli incantesimi di Voldemort
    opzioni = ottieni_opzioni("Voldemort")
    # Sceglie un indice casuale
    indice = random.randint(0, len(opzioni) - 1)
    # Esegue l'incantesimo
    esegui_mossa("Voldemort", "Harry", opzioni, indice)

    # Se Harry è ancora vivo, dopo 3 secondi è di nuovo il suo turno
    if gioco_attivo:
        clock.schedule_unique(prepara_harry, 3.0)


def prepara_harry():
    """
    Prepara il turno del giocatore: seleziona 4 incantesimi casuali tra quelli di Harry.

    .sample(4) prende 4 righe casuali dal DataFrame.
    Questo crea varietà: ogni turno il giocatore ha opzioni diverse.
    """
    global messaggio, descrizione, attesa_input, opzioni_correnti

    messaggio = "Cosa farà HARRY?"
    descrizione = "Scegli un incantesimo..."

    # Estrae 4 incantesimi casuali di Harry
    opzioni_correnti = ottieni_opzioni("Harry").sample(4)
    attesa_input = True  # Ora il giocatore può cliccare


# ========================================================================
# GESTIONE INPUT UTENTE
# ========================================================================


def on_mouse_down(pos):
    """
    Funzione chiamata automaticamente da Pygame Zero quando si clicca col mouse.
    Gestisce la selezione degli incantesimi.

    Mostra come:
    - Rilevare click del mouse
    - Calcolare posizioni dinamiche (griglia 2x2)
    - Usare Rect.collidepoint() per collision detection

    Args:
        pos (tuple): coordinate (x, y) del click
    """
    global attesa_input

    # Controlla che sia il momento giusto per cliccare
    if gioco_attivo and attesa_input and opzioni_correnti is not None:
        # Cicla sui 4 incantesimi disponibili
        for i in range(len(opzioni_correnti)):
            # ===== CALCOLO POSIZIONE GRIGLIA 2x2 =====
            # i % 2 → colonna (0 o 1)
            # i // 2 → riga (0 o 1)
            x = 40 + (i % 2) * 380  # Colonna: 40 o 420
            y = 440 + (i // 2) * 60  # Riga: 440 o 500

            # Crea un rettangolo e controlla se il click è dentro
            if Rect((x, y), (350, 50)).collidepoint(pos):
                attesa_input = False  # Disabilita ulteriori click
                esegui_mossa("Harry", "Voldemort", opzioni_correnti, i)

                # Dopo 3 secondi, se Voldemort è vivo, tocca a lui
                if gioco_attivo:
                    clock.schedule_unique(fase_voldemort, 3.0)


def on_key_down(key):
    """
    Funzione chiamata quando si preme un tasto.
    Permette di riavviare il gioco con SPAZIO.

    Pygame Zero chiama automaticamente questa funzione.

    Args:
        key: costante che rappresenta il tasto premuto
    """
    # Se il gioco è finito e si preme SPAZIO, ricomincia
    if not gioco_attivo and key == keys.SPACE:
        reset_gioco()


# ========================================================================
# RENDERING GRAFICO
# ========================================================================


def draw():
    """
    Funzione chiamata automaticamente da Pygame Zero 60 volte al secondo.
    Disegna tutto ciò che appare sullo schermo.

    Questa funzione è il "cuore grafico" del gioco.
    Viene eseguita continuamente (game loop) per aggiornare la schermata.
    """
    screen.clear()  # Cancella il frame precedente

    # ===== SCHERMATA DI GIOCO =====
    if gioco_attivo:
        # Sfondo: cielo azzurro e prato verde
        screen.draw.filled_rect(Rect((0, 0), (800, 400)), (200, 230, 255))  # Cielo
        screen.draw.filled_rect(Rect((0, 400), (800, 200)), (120, 180, 120))  # Prato

        # Disegna i personaggi
        voldy_sprite.draw()
        harry_sprite.draw()

        # Disegna le barre della vita (usa i valori animati)
        disegna_barra_stato("VOLDEMORT", display_punti_vita_voldemort, 50, 50)
        disegna_barra_stato("HARRY", display_punti_vita_harry, 450, 250)

        # ===== BOX MESSAGGI/MENU IN BASSO =====
        screen.draw.filled_rect(
            Rect((10, 410), (780, 180)), (50, 50, 60)
        )  # Sfondo scuro
        screen.draw.rect(Rect((10, 410), (780, 180)), "white")  # Bordo bianco

        # Se è il turno del giocatore, mostra il menu
        if attesa_input:
            disegna_menu()
        # Altrimenti mostra i messaggi di azione
        else:
            screen.draw.text(messaggio, (40, 450), fontsize=40)
            screen.draw.text(descrizione, (40, 510), fontsize=30, color="lightgray")

    # ===== SCHERMATA FINALE =====
    else:
        if vincitore == "Harry":
            # Schermata vittoria
            screen.blit("vittoria", (0, 0))
            screen.draw.text("HARRY HA VINTO!", center=(WIDTH / 2, 100), fontsize=70, color="white", shadow=(2, 2))
            harry_sprite.pos = (WIDTH / 2, HEIGHT / 2)
            harry_sprite.draw()
        else:
            # Schermata sconfitta
            screen.blit("sconfitta", (0, 0))
            screen.draw.text("IL MALE HA PREVALSO...", center=(WIDTH / 2, 100), fontsize=60, color="red")
            voldy_sprite.pos = (WIDTH / 2, HEIGHT / 2)
            voldy_sprite.draw()

        screen.draw.text("Premi SPAZIO per un nuovo duello", center=(WIDTH / 2, HEIGHT - 50), fontsize=40, color="white")


def disegna_barra_stato(nome, valore, x, y):
    """
    Disegna un riquadro con nome del personaggio e barra della vita.

    Esempio di grafica procedurale - creiamo elementi visuali
    con forme geometriche semplici.

    Args:
        nome (str): nome da visualizzare
        valore (float): punti vita attuali (0-100)
        x, y (int): coordinate dell'angolo superiore sinistro
    """
    # Rettangolo bianco di sfondo
    screen.draw.filled_rect(Rect((x, y), (300, 80)), "white")
    screen.draw.rect(Rect((x, y), (300, 80)), "black")  # Bordo nero

    # Nome del personaggio
    screen.draw.text(nome, (x + 20, y + 15), color="black", fontsize=30)

    # Cornice della barra (nera)
    screen.draw.rect(Rect((x + 100, y + 45), (160, 15)), "black")

    # ===== CALCOLO BARRA PROPORZIONALE =====
    # La barra è lunga 158 pixel al massimo
    larghezza_barra = (valore / 100) * 158

    # Colore dinamico: verde → arancione → rosso
    if valore > 50:
        colore = "green"
    elif valore > 20:
        colore = "orange"
    else:
        colore = "red"

    # Disegna la barra solo se ci sono PV rimasti
    if larghezza_barra > 0:
        screen.draw.filled_rect(Rect((x + 101, y + 46), (larghezza_barra, 13)), colore)


def disegna_menu():
    """
    Disegna i 4 incantesimi selezionabili in una griglia 2x2.

    Mostra come visualizzare dati da un DataFrame in modo interattivo.
    """
    if opzioni_correnti is not None:
        for i in range(len(opzioni_correnti)):
            # Calcolo posizione (stesso algoritmo di on_mouse_down)
            x = 40 + (i % 2) * 380
            y = 440 + (i // 2) * 60

            # Rettangolo cliccabile
            screen.draw.rect(Rect((x, y), (350, 50)), "white")

            # Testo dell'incantesimo
            screen.draw.text(
                f"> {opzioni_correnti[i, 'spell'].upper()}",
                (x + 20, y + 15),
                fontsize=30,
            )


# ========================================================================
# AVVIO DEL GIOCO
# ========================================================================

# Prepara il primo turno di Harry
prepara_harry()

# Avvia il game loop di Pygame Zero
pgzrun.go()
