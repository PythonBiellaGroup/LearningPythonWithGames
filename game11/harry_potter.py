import random
import polars as pl
import pgzrun
from pgzero.actor import Actor
from types import SimpleNamespace

WIDTH = 800
HEIGHT = 600
TITLE = "La Battaglia Finale"

punti_vita = {"Harry": 100, "Voldemort": 100}
visualizzazione = SimpleNamespace(Harry=100, Voldemort=100)

harry_sprite = Actor('harry', (200, 320))
voldy_sprite = Actor('voldemort', (600, 150))

messaggio = "VOLDEMORT è apparso!"
descrizione = "Cosa farà HARRY?"
attesa_input = True 
gioco_attivo = True

# --- Caricamento Dati ---
incantesimi_df = pl.read_csv(r"C:\Users\alema\Desktop\pythonbiella\LearningPythonWithGames\game11\spells.csv")

def ottieni_opzioni(personaggio):
    return incantesimi_df.filter(pl.col("character") == personaggio)

def flash_danno(sprite):
    """Fa lampeggiare lo sprite e lo scuote leggermente."""
    x_originale = sprite.x
    # Scossa rapida
    animate(sprite, duration=0.5, x=x_originale + 10, tween='bounce_end')
    # Lampeggio
    for i in range(3):
        clock.schedule_unique(lambda: setattr(sprite, 'opacity', 0), i * 0.2)
        clock.schedule_unique(lambda: setattr(sprite, 'opacity', 255), i * 0.2 + 0.1)
    # Ripristina posizione
    clock.schedule_unique(lambda: setattr(sprite, 'x', x_originale), 0.3)

# --- Logica di Gioco ---

def esegui_mossa(nome_attaccante, nome_difensore, df_incantesimi, indice_incantesimo):
    global messaggio, descrizione, gioco_attivo
    
    danno = float(df_incantesimi[indice_incantesimo, "damage"])
    precisione = float(df_incantesimi[indice_incantesimo, "precision"])
    nome_incantesimo = df_incantesimi[indice_incantesimo, 'spell'].upper()
    
    messaggio = f"{nome_attaccante.upper()} usa {nome_incantesimo}!"
    
    probabilita = random.random()
    successo = probabilita < precisione 
    
    if successo:
        if danno < 0: # Cura
            quantita = abs(danno)
            punti_vita[nome_attaccante] = min(100, punti_vita[nome_attaccante] + quantita)
            descrizione = f"Ha recuperato {quantita} PV!"
            animate(visualizzazione, duration=0.6, **{nome_attaccante: punti_vita[nome_attaccante]})
        else: # Attacco
            punti_vita[nome_difensore] = max(0, punti_vita[nome_difensore] - danno)
            descrizione = f"Ha inflitto {danno} danni!"
            # Effetto visivo danno
            target_sprite = voldy_sprite if nome_difensore == "Voldemort" else harry_sprite
            flash_danno(target_sprite)
            animate(visualizzazione, duration=0.6, **{nome_difensore: punti_vita[nome_difensore]})
    else:
        descrizione = f"L'incantesimo è fallito!"

    if punti_vita[nome_difensore] <= 0:
        gioco_attivo = False
        messaggio = f"{nome_difensore.upper()} è esausto!"
        descrizione = "Il duello è terminato."

# --- Gestione Turni ---

def fase_voldemort():
    """Voldemort sceglie un incantesimo casuale e lo lancia."""
    global messaggio, descrizione
    if not gioco_attivo: return

    opzioni = ottieni_opzioni("Voldemort")
    indice = random.randint(1, len(opzioni)) - 1
    esegui_mossa("Voldemort", "Harry", opzioni, indice)
    
    # Dopo la mossa di Voldemort, aspetta 2 secondi e passa a Harry
    if gioco_attivo:
        clock.schedule_unique(prepara_harry, 2.0)

def prepara_harry():
    """Ripristina l'interfaccia per il turno di Harry."""
    global messaggio, descrizione, attesa_input
    messaggio = "Cosa farà HARRY?"
    descrizione = "Scegli un incantesimo..."
    attesa_input = True

def on_mouse_down(pos):
    global attesa_input
    
    if gioco_attivo and attesa_input:
        opzioni = ottieni_opzioni("Harry")[:4]
        for i in range(len(opzioni)):
            x = 40 + (i % 2) * 380
            y = 440 + (i // 2) * 60
            if Rect((x, y), (350, 50)).collidepoint(pos):
                # Azione di Harry
                attesa_input = False
                esegui_mossa("Harry", "Voldemort", opzioni, i)
                
                # Se Voldemort è ancora vivo, tocca a lui tra 2 secondi
                if gioco_attivo:
                    clock.schedule_unique(fase_voldemort, 2.0)

# --- Funzioni di Disegno ---

def draw():
    screen.clear()
    # Sfondo Cielo e Prato
    screen.draw.filled_rect(Rect((0, 0), (800, 400)), (200, 230, 255)) 
    screen.draw.filled_rect(Rect((0, 400), (800, 200)), (120, 180, 120)) 

    voldy_sprite.draw()
    harry_sprite.draw()

    disegna_barra_stato("VOLDEMORT", visualizzazione.Voldemort, 50, 50)
    disegna_barra_stato("HARRY", visualizzazione.Harry, 450, 250)
    
    # Box dei Dialoghi
    screen.draw.filled_rect(Rect((10, 410), (780, 180)), (50, 50, 60))
    screen.draw.rect(Rect((10, 410), (780, 180)), "white")

    if attesa_input and gioco_attivo:
        disegna_menu_mosse()
    else:
        screen.draw.text(messaggio, (40, 450), fontsize=40, color="white")
        screen.draw.text(descrizione, (40, 510), fontsize=30, color="lightgray")

def disegna_barra_stato(nome, valore, x, y):
    screen.draw.filled_rect(Rect((x, y), (300, 80)), "white")
    screen.draw.rect(Rect((x, y), (300, 80)), "black")
    screen.draw.text(nome, (x+20, y+15), color="black", fontsize=30)
    screen.draw.rect(Rect((x+100, y+45), (160, 15)), "black")
    
    larghezza_barra = (valore / 100) * 158
    colore = "green" if valore > 50 else "orange" if valore > 20 else "red"
    
    if larghezza_barra > 0: 
        screen.draw.filled_rect(Rect((x+101, y+46), (larghezza_barra, 13)), colore)

def disegna_menu_mosse():
    opzioni = ottieni_opzioni("Harry")[:4]
    for i in range(len(opzioni)):
        x, y = 40 + (i%2)*380, 440 + (i//2)*60
        screen.draw.rect(Rect((x, y), (350, 50)), "white")
        screen.draw.text(f"> {opzioni[i, 'spell'].upper()}", (x+20, y+15), fontsize=30)

pgzrun.go()