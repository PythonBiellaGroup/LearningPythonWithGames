"""
SPACE DATA COMMANDER
Un gioco educativo per imparare Polars e visualizzazione dati

COMANDI:
- Frecce: Muovi l'astronave
- SPAZIO: Scansiona pianeta vicino
- INVIO: Atterra sul pianeta selezionato
- R: Reset dati missione

OBIETTIVO:
Raccogli dati da 10 pianeti e trova quello migliore dove fondare una colonia!
(Alta temperatura, molte risorse, basso pericolo)
"""

import pgzrun
import polars as pl
import random
import math
import os

# Configurazione finestra
WIDTH = 1200
HEIGHT = 700
TITLE = "Space Data Commander - Missione Esplorativa"

# --- VARIABILI DI GIOCO (usando dizionari e liste) ---

# Astronave (dizionario)
spaceship = {
    "x": 100,
    "y": HEIGHT // 2,
    "speed": 3,
    "scan_range": 80
}

# Lista di pianeti (ogni pianeta è un dizionario)
planets = []

# Lista di pianeti scansionati (solo gli ID)
scanned_planets = []

# Pianeta selezionato (None o ID del pianeta)
selected_planet = None

# Messaggi e stato
game_message = "Usa le FRECCE per muoverti. SPAZIO per scansionare pianeti."
mission_complete = False

# File CSV per salvare i dati
CSV_FILE = "planets_data.csv"

# --- FUNZIONI PER I PIANETI ---

def create_planet(planet_id, existing_planets):
    """Crea un nuovo pianeta (dizionario) evitando sovrapposizioni"""
    
    # Prova a trovare una posizione valida
    for attempt in range(50):
        x = random.randint(150, WIDTH - 450)
        y = random.randint(50, HEIGHT - 50)
        size = random.randint(15, 40)
        
        # Controlla distanza da altri pianeti
        too_close = False
        for other_planet in existing_planets:
            dist = math.sqrt((x - other_planet["x"])**2 + (y - other_planet["y"])**2)
            if dist < 100:  # Distanza minima
                too_close = True
                break
        
        if not too_close:
            break  # Posizione ok!
    
    # Genera attributi del pianeta
    temperature = random.randint(-100, 300)
    resources = random.randint(0, 100)
    danger = random.randint(0, 100)
    
    # Scegli colore in base alla temperatura
    if temperature < 0:
        color = (100, 150, 255)  # Blu ghiacciato
    elif temperature < 100:
        color = (100, 200, 100)  # Verde temperato
    elif temperature < 200:
        color = (255, 200, 100)  # Arancione caldo
    else:
        color = (255, 100, 100)  # Rosso rovente
    
    # Crea il dizionario pianeta
    planet = {
        "id": planet_id,
        "x": x,
        "y": y,
        "size": size,
        "temperature": temperature,
        "resources": resources,
        "danger": danger,
        "color": color,
        "scanned": False
    }
    
    return planet

def get_nearby_planet(spaceship_dict, planets_list):
    """Trova il pianeta più vicino all'astronave"""
    for planet in planets_list:
        dist = math.sqrt((spaceship_dict["x"] - planet["x"])**2 + 
                        (spaceship_dict["y"] - planet["y"])**2)
        if dist < spaceship_dict["scan_range"]:
            return planet
    return None

def get_planet_by_id(planet_id, planets_list):
    """Trova un pianeta dato il suo ID"""
    for planet in planets_list:
        if planet["id"] == planet_id:
            return planet
    return None

# --- FUNZIONI DATI (Polars) ---

def init_csv():
    """Inizializza il file CSV"""
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)

def save_planet_data(planet_dict):
    """Salva i dati del pianeta nel CSV usando Polars"""
    # Crea il nuovo record
    new_row = pl.DataFrame({
        "planet_id": [planet_dict["id"]],
        "size": [planet_dict["size"]],
        "temperature": [planet_dict["temperature"]],
        "resources": [planet_dict["resources"]],
        "danger": [planet_dict["danger"]],
    })
    
    # Leggi dati esistenti e concatena
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            df = pl.read_csv(CSV_FILE)
            df = pl.concat([df, new_row])
        except:
            df = new_row
    else:
        df = new_row
    
    df.write_csv(CSV_FILE)
    print(f"✓ Pianeta {planet_dict['id']} salvato nel database")

def load_planet_stats():
    """Carica statistiche dai dati usando Polars"""
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        return None
    
    df = pl.read_csv(CSV_FILE)
    
    if len(df) == 0:
        return None
    
    # Calcola statistiche usando Polars
    stats = {
        "count": len(df),
        "avg_temp": df["temperature"].mean(),
        "total_resources": df["resources"].sum(),
        "avg_danger": df["danger"].mean(),
        "temp_distribution": df["temperature"].to_list(),
        "best_planet": None
    }
    
    # Trova il pianeta migliore calcolando uno score
    df_scored = df.with_columns([
        ((pl.col("temperature") / 300) * 0.3 +
         (pl.col("resources") / 100) * 0.5 +
         (1 - pl.col("danger") / 100) * 0.2).alias("score")
    ])
    
    best = df_scored.sort("score", descending=True).head(1)
    if len(best) > 0:
        stats["best_planet"] = {
            "id": best["planet_id"][0],
            "temp": best["temperature"][0],
            "resources": best["resources"][0],
            "danger": best["danger"][0],
            "score": best["score"][0]
        }
    
    return stats

# --- SETUP INIZIALE ---

def reset_game():
    """Reset della missione"""
    global planets, scanned_planets, selected_planet, game_message, mission_complete
    
    # Crea 10 pianeti
    planets = []
    for i in range(1, 11):
        planet = create_planet(i, planets)
        planets.append(planet)
    
    scanned_planets = []
    selected_planet = None
    game_message = "Nuova missione iniziata! Scansiona tutti i pianeti."
    mission_complete = False
    
    # Reset CSV
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    init_csv()

# Inizializza il gioco
init_csv()
reset_game()

# --- GAME LOOP ---

def update():
    """Aggiorna lo stato del gioco (movimento)"""
    # Movimento astronave
    if keyboard.left:
        spaceship["x"] = max(20, spaceship["x"] - spaceship["speed"])
    if keyboard.right:
        spaceship["x"] = min(WIDTH - 420, spaceship["x"] + spaceship["speed"])
    if keyboard.up:
        spaceship["y"] = max(20, spaceship["y"] - spaceship["speed"])
    if keyboard.down:
        spaceship["y"] = min(HEIGHT - 20, spaceship["y"] + spaceship["speed"])

def on_key_down(key):
    """Gestisce i tasti premuti"""
    global game_message, selected_planet, mission_complete
    
    # Scansiona pianeta
    if key == keys.SPACE:
        nearby = get_nearby_planet(spaceship, planets)
        if nearby:
            if nearby["scanned"]:
                game_message = f"Pianeta {nearby['id']} già scansionato. Selezionalo con INVIO per vedere dettagli."
            else:
                # Scansiona il pianeta
                nearby["scanned"] = True
                scanned_planets.append(nearby["id"])
                save_planet_data(nearby)
                game_message = f"Pianeta {nearby['id']} scansionato! Temp: {nearby['temperature']} gradi, Risorse: {nearby['resources']}"
                
                if len(scanned_planets) == len(planets):
                    game_message = "Tutti i pianeti scansionati! Premi INVIO sul pianeta migliore per atterrare."
        else:
            game_message = "Nessun pianeta nel raggio di scansione!"
    
    # Seleziona/Atterra
    if key == keys.RETURN:
        nearby = get_nearby_planet(spaceship, planets)
        if nearby and nearby["scanned"]:
            selected_planet = nearby["id"]
            stats = load_planet_stats()
            if stats and stats["best_planet"]:
                best = stats["best_planet"]
                if nearby["id"] == best["id"]:
                    game_message = f"OTTIMA SCELTA! Pianeta {nearby['id']} e' il migliore! Missione COMPLETATA!"
                    mission_complete = True
                else:
                    game_message = f"Pianeta {nearby['id']} selezionato. Controlla i grafici - e' davvero il migliore?"
        else:
            game_message = "Devi prima scansionare questo pianeta!"
    
    # Reset
    if key == keys.R:
        reset_game()

def draw():
    """Disegna tutto sullo schermo"""
    screen.clear()
    screen.fill((10, 10, 30))  # Sfondo spazio profondo
    
    # Stelle di sfondo
    for i in range(100):
        x = (i * 137) % (WIDTH - 400)
        y = (i * 211) % HEIGHT
        screen.draw.filled_circle((x, y), 1, (200, 200, 200))
    
    # Disegna tutti i pianeti
    for planet in planets:
        if planet["scanned"]:
            # Pianeta scansionato - colorato
            screen.draw.filled_circle((planet["x"], planet["y"]), planet["size"], planet["color"])
            screen.draw.circle((planet["x"], planet["y"]), planet["size"] + 2, (255, 255, 255))
            screen.draw.text(str(planet["id"]), (planet["x"] - 5, planet["y"] - 5), 
                           color="white", fontsize=20)
        else:
            # Pianeta non scansionato - grigio
            screen.draw.filled_circle((planet["x"], planet["y"]), planet["size"], (80, 80, 80))
            screen.draw.text("?", (planet["x"] - 5, planet["y"] - 5), 
                           color="white", fontsize=25)
    
    # Disegna astronave
    screen.draw.filled_circle((spaceship["x"], spaceship["y"]), 15, (100, 200, 255))
    screen.draw.circle((spaceship["x"], spaceship["y"]), 17, (255, 255, 255))
    
    # Raggio di scansione (se c'è un pianeta vicino)
    nearby = get_nearby_planet(spaceship, planets)
    if nearby:
        screen.draw.circle((spaceship["x"], spaceship["y"]), spaceship["scan_range"], (100, 255, 100))
    
    # --- PANNELLO DATI (lato destro) ---
    panel_x = WIDTH - 380
    screen.draw.filled_rect(Rect(panel_x, 0, 380, HEIGHT), (20, 20, 40))
    screen.draw.line((panel_x, 0), (panel_x, HEIGHT), (100, 100, 150))
    
    # Titolo pannello
    screen.draw.text("=== CRUSCOTTO DATI ===", (panel_x + 20, 20), 
                    color="cyan", fontsize=24)
    
    # Statistiche missione
    y_pos = 70
    screen.draw.text(f"Pianeti scansionati: {len(scanned_planets)}/10", 
                    (panel_x + 20, y_pos), color="white", fontsize=18)
    
    # Carica e mostra statistiche con Polars
    stats = load_planet_stats()
    if stats:
        y_pos += 30
        screen.draw.text(f"Temp. media: {stats['avg_temp']:.1f} gradi C", 
                        (panel_x + 20, y_pos), color="orange", fontsize=16)
        y_pos += 25
        screen.draw.text(f"Risorse totali: {stats['total_resources']}", 
                        (panel_x + 20, y_pos), color="yellow", fontsize=16)
        y_pos += 25
        screen.draw.text(f"Pericolo medio: {stats['avg_danger']:.1f}%", 
                        (panel_x + 20, y_pos), color="red", fontsize=16)
        
        # Grafico distribuzione temperature
        y_pos += 40
        screen.draw.text("Distribuzione Temperature:", 
                        (panel_x + 20, y_pos), color="cyan", fontsize=16)
        
        # Conta pianeti per fascia di temperatura
        temps = stats['temp_distribution']
        cold = 0
        mild = 0
        warm = 0
        hot = 0
        
        for temp in temps:
            if temp < 0:
                cold += 1
            elif temp < 100:
                mild += 1
            elif temp < 200:
                warm += 1
            else:
                hot += 1
        
        y_pos += 30
        bar_width = 60
        max_height = 100
        
        # Trova il valore massimo per scalare le barre
        max_count = max(cold, mild, warm, hot)
        if max_count == 0:
            max_count = 1
        
        # Lista di barre da disegnare
        bars_data = [
            (cold, "Freddo", (100, 150, 255)),
            (mild, "Mite", (100, 200, 100)),
            (warm, "Caldo", (255, 200, 100)),
            (hot, "Rovente", (255, 100, 100))
        ]
        
        # Disegna le barre
        for i in range(len(bars_data)):
            count, label, color = bars_data[i]
            x = panel_x + 30 + i * 85
            
            if count > 0:
                height = int((count / max_count) * max_height)
            else:
                height = 0
            
            # Disegna la barra
            screen.draw.filled_rect(
                Rect(x, y_pos + max_height - height, bar_width, height), 
                color
            )
            # Numero sopra la barra
            screen.draw.text(str(count), (x + bar_width//2 - 5, y_pos + max_height - height - 20), 
                           color="white", fontsize=16)
            # Etichetta sotto la barra
            screen.draw.text(label, (x - 5, y_pos + max_height + 10), 
                           color="white", fontsize=12)
        
        # Pianeta migliore
        if stats["best_planet"]:
            best = stats["best_planet"]
            y_pos += max_height + 60
            screen.draw.text("*** PIANETA MIGLIORE ***", 
                            (panel_x + 20, y_pos), color="gold", fontsize=18)
            y_pos += 25
            screen.draw.text(f"ID: {best['id']} (Score: {best['score']:.2f})", 
                            (panel_x + 20, y_pos), color="white", fontsize=16)
            y_pos += 20
            screen.draw.text(f"Temp: {best['temp']} gradi C", 
                            (panel_x + 30, y_pos), color="orange", fontsize=14)
            y_pos += 18
            screen.draw.text(f"Risorse: {best['resources']}", 
                            (panel_x + 30, y_pos), color="yellow", fontsize=14)
            y_pos += 18
            screen.draw.text(f"Pericolo: {best['danger']}%", 
                            (panel_x + 30, y_pos), color="red", fontsize=14)
    
    # Dettagli pianeta selezionato
    if selected_planet:
        planet = get_planet_by_id(selected_planet, planets)
        if planet:
            y_pos = HEIGHT - 150
            screen.draw.filled_rect(Rect(panel_x + 10, y_pos, 360, 140), (40, 40, 80))
            screen.draw.text(f"Pianeta {planet['id']} - DETTAGLI:", 
                            (panel_x + 20, y_pos + 10), color="cyan", fontsize=16)
            screen.draw.text(f"Dimensione: {planet['size']}", 
                            (panel_x + 20, y_pos + 35), color="white", fontsize=14)
            screen.draw.text(f"Temperatura: {planet['temperature']} gradi C", 
                            (panel_x + 20, y_pos + 55), color="orange", fontsize=14)
            screen.draw.text(f"Risorse: {planet['resources']}", 
                            (panel_x + 20, y_pos + 75), color="yellow", fontsize=14)
            screen.draw.text(f"Pericolo: {planet['danger']}%", 
                            (panel_x + 20, y_pos + 95), color="red", fontsize=14)
    
    # Messaggi di gioco
    screen.draw.text(game_message, (20, HEIGHT - 40), 
                    color="white", fontsize=16, width=WIDTH - 420)
    
    # Istruzioni
    screen.draw.text("SPAZIO: Scansiona | INVIO: Seleziona/Atterra | R: Reset", 
                    (20, HEIGHT - 20), color="gray", fontsize=14)
    
    # Messaggio vittoria
    if mission_complete:
        screen.draw.filled_rect(Rect(WIDTH//2 - 250, HEIGHT//2 - 50, 500, 100), 
                               (0, 150, 0))
        screen.draw.text("*** MISSIONE COMPLETATA! ***", 
                        (WIDTH//2 - 220, HEIGHT//2 - 30), 
                        color="gold", fontsize=32)
        screen.draw.text("Hai trovato il pianeta perfetto!", 
                        (WIDTH//2 - 150, HEIGHT//2 + 10), 
                        color="white", fontsize=20)

pgzrun.go()