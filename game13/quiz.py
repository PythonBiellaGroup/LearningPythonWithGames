import pgzrun
import polars as pl
import csv
import os
from pgzero.keyboard import keys

# ───────────────── CONFIG ─────────────────
TITLE = "Cyber Quiz"
WIDTH = 900
HEIGHT = 600
TEMPO_DOMANDA = 15  # secondi totali
TEMPO_DOMANDA_MS = 15000  # millisecondi totali
NOME_FILE_CSV = "domande.csv"
# NOME_FILE_RISPOSTE sarà creato dinamicamente con il nome del giocatore

# ───────────────── COLORI ─────────────────
COLOR_BG = (10, 10, 25)
COLOR_CARD = (30, 30, 50)
COLOR_ACCENT = (0, 255, 200)
COLOR_DANGER = (255, 45, 85)
COLOR_SHADOW = (5, 5, 15)
TEXT_MAIN = (255, 255, 255)

# ───────────────── STATO ─────────────────
lista_domande = []  # Qui finirà il nostro mazzo rimescolato
domanda_corrente = None
indice_domande = 0
contatore_totale = 0
punteggio = 0
secondi_mancanti = TEMPO_DOMANDA
millisecondi_trascorsi = 0  # Millisecondi dall'inizio della domanda corrente
game_over = False
mouse_pos = (0, 0)

# Nickname / iniziale stato di inserimento
entering_name = True
nome_utente = ""
nome_file_risposte = ""  # Sarà inizializzato quando il giocatore inserisce il nome

# Box
question_box = Rect(50, 90, 800, 150)
answer_boxes = [
    Rect(50, 300, 380, 110),
    Rect(470, 300, 380, 110),
    Rect(50, 430, 380, 110),
    Rect(470, 430, 380, 110),
]
timer_bar_box = Rect(50, 260, 800, 12)


# ───────────────── LOGICA DATI CON POLARS ─────────────────
def carica_e_mischia():
    """Carica le domande dal CSV e le rimescola"""
    global lista_domande, contatore_totale
    
    # Leggiamo il CSV con Polars
    df = pl.read_csv(NOME_FILE_CSV, truncate_ragged_lines=True)
    
    # Rimescoliamo le domande
    df_shuffled = df.sample(fraction=1.0, shuffle=True)
    
    # Convertiamo in una lista di dizionari
    lista_domande = df_shuffled.to_dicts()
    contatore_totale = len(lista_domande)


def prossima_domanda():
    global domanda_corrente, indice_domande, secondi_mancanti, millisecondi_trascorsi, game_over

    if len(lista_domande) > 0:
        indice_domande += 1
        # .pop(0) prende la prima domanda e la RIMUOVE dalla lista -> Mai ripetizioni
        domanda_corrente = lista_domande.pop(0)
        secondi_mancanti = TEMPO_DOMANDA
        millisecondi_trascorsi = 0  # Reset del contatore millisecondi
    else:
        game_over = True


# ───────────────── SALVATAGGIO RISPOSTE ─────────────────
def init_file_risposte():
    """Crea il file risposte con header"""
    global nome_file_risposte
    
    # Creiamo il file con l'intestazione
    with open(nome_file_risposte, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "nome_utente",
            "id_domanda",
            "numero_risposta_fornita",
            "tempo_risposta",
        ])


def salva_risposta(nome, id_domanda, numero_risposta, tempo_risposta):
    """Salva una risposta nel CSV"""
    global nome_file_risposte
    
    # Apriamo il file in modalità append (aggiunta)
    with open(nome_file_risposte, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nome, id_domanda, numero_risposta, tempo_risposta])


# ───────────────── DISEGNO ─────────────────
def draw_styled_rect(rect, color):
    screen.draw.filled_rect(Rect(rect.x + 4, rect.y + 4, rect.w, rect.h), COLOR_SHADOW)
    screen.draw.filled_rect(rect, color)


def draw():
    screen.fill(COLOR_BG)

    # Se siamo nella fase di inserimento nickname
    if entering_name:
        screen.draw.text(
            "Benvenuto a Cyber Quiz!",
            center=(WIDTH // 2, 120),
            fontsize=48,
            color=COLOR_ACCENT,
        )
        screen.draw.text(
            "Inserisci il tuo nickname e premi ENTER per iniziare:",
            center=(WIDTH // 2, 180),
            fontsize=28,
            color=TEXT_MAIN,
        )

        # box input
        input_box = Rect(WIDTH // 2 - 300, 230, 600, 60)
        draw_styled_rect(input_box, COLOR_CARD)
        display_name = nome_utente if nome_utente != "" else "(digita qui...)"
        screen.draw.text(
            display_name, center=input_box.center, fontsize=36, color=TEXT_MAIN
        )
        return

    if game_over:
        screen.draw.text(
            f"SESSIONE FINITA\nGrazie per aver partecipato!",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=50,
            color=COLOR_ACCENT,
        )
        screen.draw.text(
            f"Le tue risposte sono state salvate in:\n{nome_file_risposte}",
            center=(WIDTH // 2, HEIGHT // 2 + 80),
            fontsize=28,
            color=TEXT_MAIN,
        )
        screen.draw.text(
            "Premi SPAZIO per un nuovo giocatore",
            center=(WIDTH // 2, HEIGHT // 2 + 150),
            fontsize=24,
            color=COLOR_ACCENT,
        )
        return

    # Info
    screen.draw.text(
        f"GIOCATORE: {nome_utente}", (50, 20), color=COLOR_ACCENT, fontsize=22
    )
    screen.draw.text(
        f"DOMANDA {indice_domande}/{contatore_totale}",
        (50, 50),
        color=COLOR_ACCENT,
        fontsize=22,
    )

    # Box Domanda
    draw_styled_rect(question_box, COLOR_CARD)
    if domanda_corrente:
        screen.draw.textbox(
            str(domanda_corrente.get("domanda", "")),
            question_box.inflate(-40, -40),
            color=TEXT_MAIN,
        )
    else:
        screen.draw.textbox(
            "Caricamento...", question_box.inflate(-40, -40), color=TEXT_MAIN
        )

    # Timer Progressivo
    percent = secondi_mancanti / TEMPO_DOMANDA if TEMPO_DOMANDA > 0 else 0
    screen.draw.filled_rect(timer_bar_box, COLOR_SHADOW)
    screen.draw.filled_rect(
        Rect(
            timer_bar_box.x,
            timer_bar_box.y,
            int(timer_bar_box.w * percent),
            timer_bar_box.h,
        ),
        COLOR_ACCENT,
    )

    # Risposte
    for i in range(4):
        box = answer_boxes[i]
        chiave = f"risposta_{i + 1}"
        is_hover = box.collidepoint(mouse_pos)
        draw_styled_rect(box, (60, 60, 90) if is_hover else COLOR_CARD)
        if domanda_corrente:
            screen.draw.textbox(
                str(domanda_corrente.get(chiave, "")),
                box.inflate(-20, -20),
                color=TEXT_MAIN,
            )


# ───────────────── INPUT & TIMER ─────────────────
def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos


def on_mouse_down(pos):
    global punteggio, millisecondi_trascorsi
    if entering_name:
        return
    if game_over:
        return

    for i, box in enumerate(answer_boxes):
        if box.collidepoint(pos):
            # tempo di risposta in millisecondi
            tempo_risposta_ms = millisecondi_trascorsi
            
            # Troviamo un id per la domanda: preferiamo campi 'id_domanda' o 'id', altrimenti usiamo l'indice attuale
            id_domanda = None
            if domanda_corrente is not None:
                # se è salvato come stringa nel CSV, manteniamo la stringa (salveremo come testo)
                id_domanda = (
                    domanda_corrente.get("id_domanda")
                    if "id_domanda" in domanda_corrente
                    else domanda_corrente.get("id")
                )
            if id_domanda is None:
                id_domanda = indice_domande

            numero_risposta = i + 1

            # Salviamo la risposta nel CSV con tempo in millisecondi
            salva_risposta(nome_utente, id_domanda, numero_risposta, tempo_risposta_ms)

            # Non controlliamo più la correttezza qui (non abbiamo la colonna 'corretta')
            # Il punteggio verrà calcolato successivamente confrontando con risposte.csv

            prossima_domanda()


def on_key_down(key):
    global nome_utente, entering_name, game_over

    # Se il gioco è finito e premo SPAZIO, riavvio per un nuovo giocatore
    if game_over:
        if key == keys.SPACE:
            reset_per_nuovo_giocatore()
        return

    # Durante l'inserimento del nickname
    if entering_name:
        # BACKSPACE
        if key == keys.BACKSPACE:
            nome_utente = nome_utente[:-1]
            return
        # ENTER -> iniziare se nome non vuoto
        if key == keys.RETURN or key == keys.KP_ENTER:
            if nome_utente.strip() != "":
                start_game()
            return
        # SOLO caratteri stampabili (singolo carattere nel nome della key)
        try:
            ch = key.name
        except Exception:
            ch = None
        if ch and len(ch) == 1:
            nome_utente += ch
        return


def tick():
    global secondi_mancanti
    if not game_over and not entering_name:
        if secondi_mancanti > 0:
            secondi_mancanti -= 1
        else:
            # se finisce il tempo, salviamo una risposta vuota/timeout
            id_domanda = None
            if domanda_corrente is not None:
                id_domanda = (
                    domanda_corrente.get("id_domanda")
                    if "id_domanda" in domanda_corrente
                    else domanda_corrente.get("id")
                )
            if id_domanda is None:
                id_domanda = indice_domande
            # numero_risposta 0 per timeout, tempo = TEMPO_DOMANDA_MS (tempo massimo)
            salva_risposta(nome_utente, id_domanda, 0, TEMPO_DOMANDA_MS)
            prossima_domanda()


def update(dt):
    """Aggiornamento continuo per contare i millisecondi con precisione"""
    global millisecondi_trascorsi
    if not game_over and not entering_name:
        # dt è il tempo in secondi dall'ultimo frame
        # Lo convertiamo in millisecondi e aggiungiamo al contatore
        millisecondi_trascorsi += int(dt * 1000)


# ───────────────── CONTROLLO START / RESTART ─────────────────

def reset_per_nuovo_giocatore():
    """Reset completo del gioco per un nuovo giocatore"""
    global entering_name, nome_utente, nome_file_risposte
    global lista_domande, domanda_corrente, indice_domande
    global contatore_totale, punteggio, secondi_mancanti, millisecondi_trascorsi, game_over
    
    # Reset di tutte le variabili
    entering_name = True
    nome_utente = ""
    nome_file_risposte = ""
    lista_domande = []
    domanda_corrente = None
    indice_domande = 0
    contatore_totale = 0
    punteggio = 0
    secondi_mancanti = TEMPO_DOMANDA
    millisecondi_trascorsi = 0
    game_over = False


def start_game():
    global entering_name, nome_utente, nome_file_risposte
    global lista_domande, domanda_corrente, indice_domande
    global contatore_totale, punteggio, secondi_mancanti, millisecondi_trascorsi, game_over
    
    # Reset di tutte le variabili
    entering_name = False
    game_over = False
    indice_domande = 0
    punteggio = 0
    secondi_mancanti = TEMPO_DOMANDA
    millisecondi_trascorsi = 0
    
    # Inizializziamo il nome del file risposte con il nome del giocatore
    nome_file_risposte = f"{nome_utente}_risposte.csv"
    
    # Creiamo il file CSV con l'intestazione
    init_file_risposte()
    
    # Carichiamo e avviamo
    carica_e_mischia()
    prossima_domanda()
    
    # Avviamo il tick
    clock.schedule_interval(tick, 1.0)


# AVVIO: non carichiamo automaticamente le domande, aspettiamo il nickname
pgzrun.go()
