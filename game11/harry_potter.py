import random
import polars as pl
import pgzrun
from pgzero.actor import Actor
from types import SimpleNamespace

# ===== CONFIGURAZIONE INIZIALE =====
WIDTH = 800
HEIGHT = 600
TITLE = "La Battaglia Finale: Harry vs Voldemort"

# Variabili globali per lo stato del gioco
punti_vita = {"Harry": 100, "Voldemort": 100}
# SimpleNamespace permette di animare i valori come se fossero proprietà di un oggetto
visualizzazione = SimpleNamespace(Harry=100, Voldemort=100)
# Variabili di controllo del flusso
messaggio = "VOLDEMORT è apparso!"
descrizione = "Cosa farà HARRY?"
attesa_input = True
gioco_attivo = True

# Creazione degli sprite
harry_sprite = Actor("harry", (200, 320))
voldy_sprite = Actor("voldemort", (600, 100))

# Variabile per memorizzare chi ha vinto
vincitore = None

# --- Caricamento Dati ---
incantesimi_df = pl.read_csv(
    r"C:\Users\alema\Desktop\pythonbiella\LearningPythonWithGames\game11\spells.csv"
)


def ottieni_opzioni(personaggio):
    """Filtra il DataFrame per ottenere solo gli incantesimi di un personaggio specifico."""
    return incantesimi_df.filter(pl.col("character") == personaggio)


# Effetti Visivi


def flash_danno(sprite):
    """Crea un effetto visivo di scossa e lampeggio quando uno sprite subisce danni."""
    x_originale = sprite.x
    # Animazione di scossa
    animate(sprite, duration=0.5, x=x_originale + 10, tween="bounce_end")
    # Ciclo per far sparire e riapparire lo sprite
    for i in range(3):
        clock.schedule_unique(lambda: setattr(sprite, "opacity", 0), i * 0.5)
        clock.schedule_unique(lambda: setattr(sprite, "opacity", 255), i * 0.5 + 0.1)
    # Ripristina la posizione originale dopo l'effetto
    clock.schedule_unique(lambda: setattr(sprite, "x", x_originale), 0.6)


# Logica di Gioco


def reset_gioco():
    """Ripristina lo stato iniziale per una nuova partita."""
    global \
        punti_vita, \
        visualizzazione, \
        messaggio, \
        descrizione, \
        attesa_input, \
        gioco_attivo, \
        vincitore
    punti_vita = {"Harry": 100, "Voldemort": 100}
    visualizzazione.Harry = 100
    visualizzazione.Voldemort = 100
    messaggio = "Nuovo Duello!"
    descrizione = "Cosa farà HARRY?"
    attesa_input = True
    gioco_attivo = True
    # Ripristina opacità
    harry_sprite.opacity = 255
    harry_sprite.pos = (200, 320)
    voldy_sprite.opacity = 255
    voldy_sprite.pos = (600, 100)
    vincitore = None


def esegui_mossa(nome_attaccante, nome_difensore, df_incantesimi, indice_incantesimo):
    """Gestisce il calcolo dei danni, le cure e gli aggiornamenti grafici di una mossa."""
    global messaggio, descrizione, gioco_attivo, vincitore

    # Estrazione dati dal DataFrame
    danno = float(df_incantesimi[indice_incantesimo, "damage"])
    precisione = float(df_incantesimi[indice_incantesimo, "precision"])
    nome_incantesimo = df_incantesimi[indice_incantesimo, "spell"].upper()

    messaggio = f"{nome_attaccante.upper()} usa {nome_incantesimo}!"

    # Calcolo successo basato sulla precisione
    successo = random.random() < precisione

    if successo:
        if danno < 0:  # Caso incantesimo di Cura
            quantita = abs(danno)
            punti_vita[nome_attaccante] = min(
                100, punti_vita[nome_attaccante] + quantita
            )
            descrizione = f"Ha recuperato {quantita} PV!"
            # Anima la barra della vita che sale
            animate(
                visualizzazione,
                duration=0.6,
                **{nome_attaccante: punti_vita[nome_attaccante]},
            )
        else:  # Caso incantesimo di Attacco
            punti_vita[nome_difensore] = max(0, punti_vita[nome_difensore] - danno)
            descrizione = f"Ha inflitto {danno} danni!"
            # Attiva effetti visivi sul bersaglio
            target_sprite = (
                voldy_sprite if nome_difensore == "Voldemort" else harry_sprite
            )
            flash_danno(target_sprite)
            # Anima la barra della vita che scende
            animate(
                visualizzazione,
                duration=0.6,
                **{nome_difensore: punti_vita[nome_difensore]},
            )
    else:
        # la precisione dell'incantesimo nno è tale da andare a segno
        descrizione = f"L'incantesimo è fallito!"

    # Controllo condizione di vittoria
    if punti_vita[nome_difensore] <= 0:
        gioco_attivo = False
        vincitore = nome_attaccante


def fase_voldemort():
    """Gestisce l'intelligenza artificiale di Voldemort."""
    global messaggio, descrizione
    if not gioco_attivo:
        return

    opzioni = ottieni_opzioni("Voldemort")
    indice = random.randint(0, len(opzioni) - 1)
    esegui_mossa("Voldemort", "Harry", opzioni, indice)

    # Se Harry è ancora vivo, torna il suo turno dopo 3 secondi
    if gioco_attivo:
        clock.schedule_unique(prepara_harry, 3.0)


def prepara_harry():
    """Ripristina il menu per il turno del giocatore."""
    global messaggio, descrizione, attesa_input
    messaggio = "Cosa farà HARRY?"
    descrizione = "Scegli un incantesimo..."
    attesa_input = True


def on_mouse_down(pos):
    """Gestisce il click del mouse sulle opzioni degli incantesimi."""
    global attesa_input

    if gioco_attivo and attesa_input:
        opzioni = ottieni_opzioni("Harry")[:4]
        for i in range(len(opzioni)):
            # Calcolo dinamico della posizione dei rettangoli cliccabili (2x2)
            x = 40 + (i % 2) * 380
            y = 440 + (i // 2) * 60
            if Rect((x, y), (350, 50)).collidepoint(pos):
                attesa_input = False
                esegui_mossa("Harry", "Voldemort", opzioni, i)

                # Turno di Voldemort dopo 3 secondi se non ha perso
                if gioco_attivo:
                    clock.schedule_unique(fase_voldemort, 3.0)


def on_key_down(key):
    """Gestisce il riavvio con SPAZIO."""
    if not gioco_attivo and key == keys.SPACE:
        reset_gioco()


# Funzioni di Disegno


def draw():
    """Disegna l'interfaccia di gioco ogni frame."""
    screen.clear()
    # Disegno ambiente (Cielo e Prato)
    if gioco_attivo:
        screen.draw.filled_rect(Rect((0, 0), (800, 400)), (200, 230, 255))
        screen.draw.filled_rect(Rect((0, 400), (800, 200)), (120, 180, 120))

        # Disegno personaggi
        voldy_sprite.draw()
        harry_sprite.draw()

        # Disegno barre della vita
        disegna_barra_stato("VOLDEMORT", visualizzazione.Voldemort, 50, 50)
        disegna_barra_stato("HARRY", visualizzazione.Harry, 450, 250)

        # Box dei Dialoghi / Menu (rettangolo scuro in basso)
        screen.draw.filled_rect(Rect((10, 410), (780, 180)), (50, 50, 60))
        screen.draw.rect(Rect((10, 410), (780, 180)), "white")

        if attesa_input:
            disegna_menu()
        else:
            screen.draw.text(messaggio, (40, 450), fontsize=40)
            screen.draw.text(descrizione, (40, 510), fontsize=30, color="lightgray")

    else:
        # Schermata Finale: qualcuno ha vinto
        if vincitore == "Harry":
            screen.blit("vittoria", (0, 0))
            screen.draw.text(
                "HARRY HA VINTO!",
                center=(WIDTH / 2, 100),
                fontsize=70,
                color="white",
                shadow=(2, 2),
            )
            harry_sprite.pos = (WIDTH / 2, HEIGHT / 2)
            harry_sprite.draw()
        else:
            screen.blit("sconfitta", (0, 0))
            screen.draw.text(
                "IL MALE HA PREVALSO...",
                center=(WIDTH / 2, 100),
                fontsize=60,
                color="red",
            )
            voldy_sprite.pos = (WIDTH / 2, HEIGHT / 2)
            voldy_sprite.draw()

        screen.draw.text(
            "Premi SPAZIO per un nuovo duello",
            center=(WIDTH / 2, HEIGHT - 50),
            fontsize=40,
            color="white",
        )


def disegna_barra_stato(nome, valore, x, y):
    """Disegna un riquadro con nome e barra della salute proporzionale al valore."""
    screen.draw.filled_rect(Rect((x, y), (300, 80)), "white")
    screen.draw.rect(Rect((x, y), (300, 80)), "black")
    screen.draw.text(nome, (x + 20, y + 15), color="black", fontsize=30)

    # Sfondo nero della barra
    screen.draw.rect(Rect((x + 100, y + 45), (160, 15)), "black")

    # Calcolo larghezza e colore barra salute
    larghezza_barra = (valore / 100) * 158
    colore = "green" if valore > 50 else "orange" if valore > 20 else "red"

    if larghezza_barra > 0:
        screen.draw.filled_rect(Rect((x + 101, y + 46), (larghezza_barra, 13)), colore)


def disegna_menu():
    """Disegna le 4 opzioni di incantesimo cliccabili per Harry."""
    opzioni = ottieni_opzioni("Harry")[:4]
    for i in range(len(opzioni)):
        x, y = 40 + (i % 2) * 380, 440 + (i // 2) * 60
        screen.draw.rect(Rect((x, y), (350, 50)), "white")
        screen.draw.text(
            f"> {opzioni[i, 'spell'].upper()}", (x + 20, y + 15), fontsize=30
        )


pgzrun.go()
