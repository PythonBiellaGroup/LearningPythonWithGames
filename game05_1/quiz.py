import pgzrun
import polars as pl
import random

# ───────────────── CONFIG ─────────────────
TITLE = "Cyber Quiz Polars Edition"
WIDTH = 900
HEIGHT = 600
TEMPO_DOMANDA = 15
NOME_FILE_CSV = "domande.csv"

# ───────────────── COLORI ─────────────────
COLOR_BG = (10, 10, 25)
COLOR_CARD = (30, 30, 50)
COLOR_ACCENT = (0, 255, 200) 
COLOR_DANGER = (255, 45, 85)
COLOR_SHADOW = (5, 5, 15)
TEXT_MAIN = (255, 255, 255)

# ───────────────── STATO ─────────────────
lista_domande = []  # Qui finira il nostro mazzo rimescolato
domanda_corrente = None
indice_domande = 0
contatore_totale = 0
punteggio = 0
secondi_mancanti = TEMPO_DOMANDA
game_over = False
mouse_pos = (0, 0)

# Box
question_box = Rect(50, 90, 800, 150)
answer_boxes = [Rect(50, 300, 380, 110), Rect(470, 300, 380, 110),
                Rect(50, 430, 380, 110), Rect(470, 430, 380, 110)]
timer_bar_box = Rect(50, 260, 800, 12)

# ───────────────── LOGICA DATI CON POLARS ─────────────────
def carica_e_mischia():
    global lista_domande, contatore_totale
    try:
        # Leggiamo il CSV con Polars
        df = pl.read_csv(NOME_FILE_CSV)
        
        # Rimescoliamo l'intero DataFrame. 
        # shuffle=True con fraction=1.0 ci restituisce tutto il DF in ordine casuale
        df_shuffled = df.sample(fraction=1.0, shuffle=True)
        
        # Convertiamo in una lista di dizionari per facilitare l'estrazione nel gioco
        lista_domande = df_shuffled.to_dicts()
        contatore_totale = len(lista_domande)
        
    except Exception as e:
        print(f"Errore nel caricamento dati: {e}")

def prossima_domanda():
    global domanda_corrente, indice_domande, secondi_mancanti, game_over
    
    if len(lista_domande) > 0:
        indice_domande += 1
        # .pop(0) prende la prima domanda e la RIMUOVE dalla lista -> Mai ripetizioni
        domanda_corrente = lista_domande.pop(0)
        secondi_mancanti = TEMPO_DOMANDA
    else:
        game_over = True

# ───────────────── DISEGNO ─────────────────
def draw_styled_rect(rect, color):
    screen.draw.filled_rect(Rect(rect.x+4, rect.y+4, rect.w, rect.h), COLOR_SHADOW)
    screen.draw.filled_rect(rect, color)

def draw():
    screen.fill(COLOR_BG)
    if game_over:
        screen.draw.text(f"SESSIONE FINITA\nPunteggio: {punteggio}/{contatore_totale}", 
                         center=(WIDTH//2, HEIGHT//2), fontsize=50, color=COLOR_ACCENT)
        return

    # Info
    screen.draw.text(f"DOMANDA {indice_domande}/{contatore_totale}", (50, 20), color=COLOR_ACCENT, fontsize=25)
    screen.draw.text(f"PUNTI: {punteggio}", (WIDTH-150, 20), color=TEXT_MAIN, fontsize=25)

    # Box Domanda
    draw_styled_rect(question_box, COLOR_CARD)
    screen.draw.textbox(domanda_corrente['domanda'], question_box.inflate(-40,-40), color=TEXT_MAIN)

    # Timer Progressivo
    percent = secondi_mancanti / TEMPO_DOMANDA
    screen.draw.filled_rect(timer_bar_box, COLOR_SHADOW)
    screen.draw.filled_rect(Rect(timer_bar_box.x, timer_bar_box.y, int(timer_bar_box.w * percent), timer_bar_box.h), COLOR_ACCENT)

    # Risposte
    for i in range(4):
        box = answer_boxes[i]
        chiave = f"risposta{i+1}"
        is_hover = box.collidepoint(mouse_pos)
        draw_styled_rect(box, (60, 60, 90) if is_hover else COLOR_CARD)
        screen.draw.textbox(str(domanda_corrente[chiave]), box.inflate(-20, -20), color=TEXT_MAIN)

# ───────────────── INPUT & TIMER ─────────────────
def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def on_mouse_down(pos):
    global punteggio
    if game_over: return

    for i, box in enumerate(answer_boxes):
        if box.collidepoint(pos):
            # Polars può leggere i numeri come int, quindi forziamo a stringa per il confronto
            if str(i + 1) == str(domanda_corrente['corretta']):
                punteggio += 1
            prossima_domanda()

def tick():
    global secondi_mancanti
    if not game_over:
        if secondi_mancanti > 0:
            secondi_mancanti -= 1
        else:
            prossima_domanda()

# AVVIO
carica_e_mischia()
prossima_domanda()
clock.schedule_interval(tick, 1.0)
pgzrun.go()