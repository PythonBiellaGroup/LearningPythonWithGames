import random
import pgzrun

# --- Finestra ---
WIDTH  = 700
HEIGHT = 500
TITLE  = "MEMO"

# --- Layout ---
COLONNE   = 6
CARTA_W   = 80
CARTA_H   = 110
SPAZIO_X  = 20
SPAZIO_Y  = 30
MARGINE_X = (WIDTH - COLONNE * CARTA_W - (COLONNE - 1) * SPAZIO_X) // 2
MARGINE_Y = 110

# --- Colori delle 6 coppie ---
COLORI = [
    (220,  60,  60),   # rosso
    ( 60, 160, 220),   # azzurro
    ( 60, 200, 100),   # verde
    (230, 180,  40),   # giallo
    (180,  80, 220),   # viola
    (230, 120,  40),   # arancione
]

# --- Palette UI ---
SFONDO        = (30,  30,  40)
CARTA_COPERTA = (60,  65,  90)
CARTA_BORDO   = (90,  95, 130)
BIANCO        = (255, 255, 255)
GRIGIO        = (180, 180, 200)
TESTO_TITOLO  = (200, 210, 255)
VERDE_OK      = ( 80, 220, 130)
ROSSO_ERR     = (220,  80,  80)

DURATA_MOSTRA = 2   # secondi prima di nascondere le carte sbagliate (usato da clock.schedule)

# =============================================================
# Struttura carta: lista  [colore_idx, scoperta, trovata, x, y]
#   colore_idx : int  – indice in COLORI
#   scoperta   : bool – temporaneamente visibile
#   trovata    : bool – coppia indovinata, resta visibile
#   x, y       : int  – angolo superiore sinistro della carta
# =============================================================

def crea_carte():
    indici = list(range(6)) * 2
    random.shuffle(indici)
    carte = []
    for i, idx_col in enumerate(indici):
        riga = i // COLONNE
        col  = i %  COLONNE
        x = MARGINE_X + col * (CARTA_W + SPAZIO_X)
        y = MARGINE_Y + riga * (CARTA_H + SPAZIO_Y)
        carte.append([idx_col, False, False, x, y])
    return carte


# --- Stato globale ---
carte         = crea_carte()
errori        = 0
selezionate   = []        # indici delle carte scelte nel turno corrente (max 2)
attesa_hide   = False
partita_vinta = False

# =============================================================
# Disegno
# =============================================================

def draw():
    screen.fill(SFONDO)

    # Titolo
    screen.draw.text("MEMO", topleft=(28, 16),
                     fontsize=42, color=TESTO_TITOLO, bold=True)

    # Contatore errori
    col_err = ROSSO_ERR if errori > 0 else GRIGIO
    screen.draw.text(f"Errori: {errori}", topleft=(200, 26),
                     fontsize=24, color=col_err)

    # Suggerimento tasto spazio (solo durante il gioco)
    if partita_vinta:
        screen.draw.text("SPAZIO = nuova partita", topright=(WIDTH - 20, 26),
                         fontsize=18, color=GRIGIO)

    # Carte
    for carta in carte:
        disegna_carta(carta)

    # Schermata di vittoria
    if partita_vinta:
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (20, 20, 35))
        screen.draw.text("Hai vinto!",
                         center=(WIDTH // 2, HEIGHT // 2 - 35),
                         fontsize=48, color=VERDE_OK, bold=True)
        screen.draw.text(f"Completato con {errori} errori",
                         center=(WIDTH // 2, HEIGHT // 2 + 15),
                         fontsize=26, color=BIANCO)
        screen.draw.text("Premi SPAZIO per giocare ancora",
                         center=(WIDTH // 2, HEIGHT // 2 + 55),
                         fontsize=18, color=GRIGIO)


def disegna_carta(carta):
    idx_col, scoperta, trovata, x, y = carta
    r = Rect(x, y, CARTA_W, CARTA_H)

    if scoperta or trovata:
        colore = COLORI[idx_col]
        screen.draw.filled_rect(r, colore)
        bordo = tuple(min(255, c + 70) for c in colore)
        screen.draw.rect(r, bordo)
        if trovata:
            screen.draw.rect(r, VERDE_OK)
    else:
        screen.draw.filled_rect(r, CARTA_COPERTA)
        screen.draw.rect(r, CARTA_BORDO)
        # Puntini decorativi sul retro
        for dr in range(3):
            for dc in range(3):
                px = x + CARTA_W // 4 + dc * (CARTA_W // 4)
                py = y + CARTA_H // 5 + dr * (CARTA_H // 4)
                screen.draw.filled_circle((px, py), 3, CARTA_BORDO)


# =============================================================
# Logica
# =============================================================

def nascondi_carte():
    """Chiamata da clock.schedule dopo DURATA_MOSTRA secondi."""
    global attesa_hide
    for idx in selezionate:
        carte[idx][1] = False   # nascondi la carta
    selezionate.clear()
    attesa_hide = False


def on_key_down(key):
    global errori, attesa_hide, selezionate, partita_vinta, carte

    if key == keys.SPACE and partita_vinta:
        clock.unschedule(nascondi_carte)
        carte         = crea_carte()
        errori        = 0
        selezionate   = []
        attesa_hide   = False
        partita_vinta = False


def on_mouse_down(pos):
    global errori, attesa_hide, selezionate, partita_vinta, carte

    mx, my = pos

    # Ignora clic durante attesa o a partita vinta
    if attesa_hide or partita_vinta:
        return

    idx = indice_carta_sotto(mx, my)
    if idx == -1:
        return

    carta = carte[idx]
    # Ignora carte già trovate, già scoperte o già selezionate
    if carta[2] or carta[1] or idx in selezionate:
        return

    carta[1] = True           # scopri la carta
    selezionate.append(idx)

    if len(selezionate) == 2:
        idx_a, idx_b = selezionate
        if carte[idx_a][0] == carte[idx_b][0]:
            # Coppia corretta: segna come trovata
            carte[idx_a][2] = True
            carte[idx_b][2] = True
            selezionate = []
            if all(c[2] for c in carte):
                partita_vinta = True
        else:
            # Coppia sbagliata: incrementa errori e programma il nascondimento
            errori     += 1
            attesa_hide = True
            clock.schedule(nascondi_carte, DURATA_MOSTRA)


def indice_carta_sotto(mx, my):
    """Restituisce l'indice della carta sotto il cursore, -1 se nessuna."""
    for i, carta in enumerate(carte):
        _, _, _, x, y = carta
        if x <= mx <= x + CARTA_W and y <= my <= y + CARTA_H:
            return i
    return -1

# Avvia il game loop di Pygame Zero
pgzrun.go()