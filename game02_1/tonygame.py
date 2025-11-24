# Importazione dei moduli necessari di Pygame Zero
from pgzero.actor import Actor  # Per creare sprite/personaggi
from pgzero.clock import clock  # Per gestire timer e eventi temporizzati
from pgzero.keyboard import keyboard  # Per rilevare input da tastiera
import pgzrun  # Per avviare il gioco
from random import randint  # Per generare posizioni casuali


def draw():
    """
    Funzione chiamata automaticamente da Pygame Zero per disegnare tutto sullo schermo.
    Viene eseguita continuamente (circa 60 volte al secondo).
    """
    # Disegna l'immagine di sfondo
    screen.blit("sfondo_bn", (0, 0))

    # Disegna gli sprite di nota e Tony
    nota.draw()
    tony.draw()

    # Disegna il punteggio con ombra bianca
    screen.draw.text(
        "Note imparate: " + str(punteggio),
        color="black",
        topleft=(10, 10),
        shadow=(1, 1),  # Offset dell'ombra (x, y)
        scolor="#FFFFFF",  # Colore dell'ombra (bianco)
        fontsize=40,
    )

    # Se il gioco è finito, mostra la schermata finale
    if game_over:
        # Schermata di vittoria (se punteggio supera la soglia)
        if punteggio > VITTORIA_PUNTEGGIO:
            screen.blit(
                "vittoria", (0, 0)
            )  # Sfondo studio musicale per rappresentare la vittoria
            screen.draw.text(
                "Daje Tony, questo pezzo spacca!\nNote messe insieme: "
                + str(punteggio),
                center=(WIDTH / 2, HEIGHT / 2),
                fontsize=60,
                color="white",
            )
            tony.image = "tony2"  # Cambia l'immagine di Tony (versione vittoria)
            tony.pos = 400, 200
            tony.draw()

        else:
            # Schermata di sconfitta
            screen.draw.text(
                "Peccato!\nDevi esercitarti di più.\nNote messe insieme: "
                + str(punteggio),
                midtop=(WIDTH / 2, 10),
                fontsize=40,
                color="red",
            )

        # Messaggio per ricominciare con il tasto SPAZIO
        screen.draw.text(
            "Premi SPAZIO per ricominciare",
            center=(WIDTH / 2, HEIGHT - 100),
            fontsize=40,
            color="white",
        )


def piazza_nota():
    """
    Posiziona la nota musicale in una posizione casuale dello schermo.
    Mantiene un margine di 70 pixel dai bordi per evitare che la nota
    appaia troppo vicino al limite dello schermo.
    """
    nota.x = randint(70, (WIDTH - 70))
    nota.y = randint(70, (HEIGHT - 70))


def tempo_scaduto():
    """
    Funzione chiamata dal timer quando il tempo di gioco è finito.
    Imposta la variabile game_over a True per terminare la partita.
    """
    global game_over, musica_vittoria_suonata
    game_over = True

    # fai partire la canzone per la vittoria solo se si ha vinto (e falla partire solo una volta)
    if punteggio > VITTORIA_PUNTEGGIO and not musica_vittoria_suonata:
        sounds.last_note.play()
        musica_vittoria_suonata = True


def reset_gioco():
    """
    Resetta tutte le variabili e lo stato del gioco per iniziare una nuova partita.
    Riporta tutto ai valori iniziali.
    """
    global punteggio, game_over, musica_vittoria_suonata
    punteggio = 0  # Azzera il punteggio
    game_over = False  # Riattiva il gioco
    musica_vittoria_suonata = False  # Reset variabile per la musica finale
    tony.pos = 100, 100  # Riporta Tony alla posizione iniziale
    tony.image = "tony"  # Ripristina l'immagine normale di Tony
    piazza_nota()  # Posiziona una nuova nota
    clock.schedule(tempo_scaduto, DURATA_GIOCO)  # Riavvia il timer
    sounds.last_note.stop()  # Ferma la musica di vittoria se stava suonando


def on_key_down(key):
    """
    Funzione chiamata automaticamente quando viene premuto un tasto.
    Gestisce il riavvio del gioco quando si preme SPAZIO dopo il game over.

    Args:
        key: Il tasto premuto dall'utente
    """
    global game_over
    if game_over and key == keys.SPACE:
        reset_gioco()


def update():
    """
    Funzione chiamata automaticamente da Pygame Zero per aggiornare la logica del gioco.
    Viene eseguita continuamente (circa 60 volte al secondo).
    Gestisce il movimento del personaggio e il rilevamento delle collisioni.
    """
    global punteggio, game_over

    # Esegui la logica di gioco solo se il gioco non è finito
    if not game_over:
        # Controlla i tasti freccia per muovere Tony
        if keyboard.left:
            tony.x -= 5  # Muove a sinistra
        if keyboard.right:
            tony.x += 5  # Muove a destra
        if keyboard.up:
            tony.y -= 5  # Muove in alto
        if keyboard.down:
            tony.y += 5  # Muove in basso

        # Controlla se Tony ha raggiunto la nota
        nota_presa = tony.colliderect(nota)

        if nota_presa:
            punteggio += 1  # Incrementa il punteggio
            """
            Suona una nota musicale diversa in base al punteggio corrente.
            Utilizza il modulo 7 per ciclare attraverso le 7 note della scala (do, re, mi, fa, sol, la, si).
            """
            if punteggio % 7 == 0:
                sounds.do.play()
            elif punteggio % 7 == 1:
                sounds.re.play()
            elif punteggio % 7 == 2:
                sounds.mi.play()
            elif punteggio % 7 == 3:
                sounds.fa.play()
            elif punteggio % 7 == 4:
                sounds.sol.play()
            elif punteggio % 7 == 5:
                sounds.la.play()
            elif punteggio % 7 == 6:
                sounds.si.play()
            piazza_nota()  # Posiziona una nuova nota in un punto casuale


# ===== CONFIGURAZIONE INIZIALE DEL GIOCO =====

# Costanti della finestra di gioco
TITLE = "Tony alla ricerca... della musica"  # Titolo della finestra
WIDTH = 800  # Larghezza della finestra in pixel
HEIGHT = 600  # Altezza della finestra in pixel

# Costanti di gioco
DURATA_GIOCO = 30  # Durata della partita in secondi
VITTORIA_PUNTEGGIO = 20  # Punteggio minimo per vincere

# Variabili di stato del gioco
punteggio = 0  # Punteggio iniziale
game_over = False  # Stato del gioco (False = in corso, True = finito)
musica_vittoria_suonata = False  # Inizializziamo a False la variabile che ci fa partire la musica per la vittoria

# Creazione del personaggio principale
tony = Actor("tony")  # Crea lo sprite di Tony
tony.pos = 100, 100  # Posizione iniziale (x=100, y=100)

# Creazione della nota musicale da raccogliere
nota = Actor("nota musicale")
piazza_nota()  # Posiziona la prima nota in modo casuale

# Avvia il timer per la fine del gioco
clock.schedule(tempo_scaduto, DURATA_GIOCO)

# Avvia il gioco
pgzrun.go()
