import random
import polars as pl
import pgzrun
from types import SimpleNamespace

# --- Settings ---
WIDTH = 800
HEIGHT = 600
TITLE = "Wizarding Duel: Turn-Based Strategy"

# --- State ---
hp = {"Harry": 100, "Voldemort": 100}
display = SimpleNamespace(Harry=100, Voldemort=100)

message = "A wild VOLDEMORT appeared!"
sub_message = "What will HARRY do?"
current_turn = "Harry" # Who is currently attacking
waiting_for_input = True # Controls if buttons are visible
game_active = True

# --- Load Data ---
spells_df = pl.read_csv("spells.csv")

def get_options(character):
    return spells_df.filter(pl.col("character") == character).to_dicts()

# --- Battle Logic ---

def player_choice(spell_data):
    """Triggered when Harry clicks a button."""
    global waiting_for_input, message, sub_message
    
    waiting_for_input = False
    execute_move("Harry", "Voldemort", spell_data)
    
    # If Voldemort survived, schedule his turn in 2 seconds
    if game_active:
        clock.schedule_unique(voldemort_turn, 2.0)

def voldemort_turn():
    """Triggered automatically after Harry's turn."""
    global message, sub_message, waiting_for_input
    
    if not game_active: return

    choices = get_options("Voldemort")
    spell = random.choice(choices)
    
    execute_move("Voldemort", "Harry", spell)
    
    # After Voldemort attacks, give Harry control back in 1.5 seconds
    if game_active:
        clock.schedule_unique(reset_to_player, 1.5)

def execute_move(attacker, defender, spell_data):
    global message, sub_message, game_active
    
    raw_damage = float(spell_data["damage"])
    
    # --- HEALING LOGIC ---
    if raw_damage < 0:
        # It's a heal! Target is the attacker, not the defender
        heal_amount = abs(raw_damage)
        hp[attacker] = min(100, hp[attacker] + heal_amount) # Cap at 100
        
        message = f"{attacker.upper()} used {spell_data['spell'].upper()}!"
        sub_message = f"It recovered {heal_amount} HP!"
        
        # Animate the attacker's bar
        if attacker == "Harry":
            animate(display, duration=0.6, Harry=hp["Harry"])
        else:
            animate(display, duration=0.6, Voldemort=hp["Voldemort"])
            
    # --- ATTACK LOGIC ---
    else:
        hp[defender] = max(0, hp[defender] - raw_damage)
        message = f"{attacker.upper()} used {spell_data['spell'].upper()}!"
        sub_message = f"It dealt {raw_damage} damage!"
        
        # Animate the defender's bar
        if defender == "Harry":
            animate(display, duration=0.6, Harry=hp["Harry"])
        else:
            animate(display, duration=0.6, Voldemort=hp["Voldemort"])

    # Check for win/loss (only matters if damage was dealt)
    if hp[defender] <= 0:
        game_active = False
        message = f"{defender.upper()} fainted!"
        sub_message = f"{attacker.upper()} is the winner!"

def reset_to_player():
    global message, sub_message, waiting_for_input
    message = "What will HARRY do?"
    sub_message = "Choose a spell to cast!"
    waiting_for_input = True

# --- Draw Functions ---

def draw():
    screen.draw.filled_rect(Rect((0, 0), (800, 400)), (200, 230, 255)) 
    screen.draw.filled_rect(Rect((0, 400), (800, 200)), (120, 180, 120)) 

    # Status Boxes
    draw_status_box("VOLDEMORT", display.Voldemort, 50, 50)
    draw_status_box("HARRY", display.Harry, 450, 300)
    
    # UI Box
    screen.draw.filled_rect(Rect((10, 410), (780, 180)), (50, 50, 60))
    screen.draw.rect(Rect((10, 410), (780, 180)), "white")

    if waiting_for_input and game_active:
        draw_move_menu()
    else:
        # Show text messages during animations or enemy turn
        screen.draw.text(message, (40, 450), fontsize=40, color="white")
        screen.draw.text(sub_message, (40, 510), fontsize=30, color="lightgray")

def draw_status_box(name, current_hp, x, y):
    screen.draw.filled_rect(Rect((x, y), (300, 80)), "white")
    screen.draw.rect(Rect((x, y), (300, 80)), "black")
    screen.draw.text(name, (x + 20, y + 15), color="black", fontsize=30)
    # HP Bar Border
    screen.draw.rect(Rect((x + 100, y + 45), (160, 15)), "black")
    # Fill
    bar_width = (current_hp / 100) * 158
    color = "green" if current_hp > 50 else "orange" if current_hp > 20 else "red"
    if bar_width > 0:
        screen.draw.filled_rect(Rect((x + 101, y + 46), (bar_width, 13)), color)

def draw_move_menu():
    options = get_options("Harry")[:4]
    for i, spell in enumerate(options):
        x = 40 + (i % 2) * 380
        y = 440 + (i // 2) * 60
        screen.draw.rect(Rect((x, y), (350, 50)), "white")
        screen.draw.text(f"> {spell['spell'].upper()}", (x + 20, y + 15), fontsize=30)

# --- Input ---

def on_mouse_down(pos):
    if game_active and waiting_for_input:
        options = get_options("Harry")[:4]
        for i in range(len(options)):
            x = 40 + (i % 2) * 380
            y = 440 + (i // 2) * 60
            if Rect((x, y), (350, 50)).collidepoint(pos):
                player_choice(options[i])

pgzrun.go()