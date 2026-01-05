import random
import polars as pl
import pgzrun
from types import SimpleNamespace

WIDTH = 800
HEIGHT = 600
TITLE = "Wizarding Duel: The Final Battle"

# --- State ---
hp = {"Harry": 100, "Voldemort": 100}
display = SimpleNamespace(Harry=100, Voldemort=100)

# Sprites (Ensure harry.png and voldemort.png are in the 'images' folder)
harry_sprite = Actor('harry', (200, 320))
voldy_sprite = Actor('voldemort', (600, 150))

message = "A wild VOLDEMORT appeared!"
sub_message = "What will HARRY do?"
waiting_for_input = True 
game_active = True

# --- Load Data ---
spells_df = pl.read_csv(r"C:\Users\alema\Desktop\pythonbiella\LearningPythonWithGames\game11\spells.csv")

def get_options(character):
    return spells_df.filter(pl.col("character") == character)

# --- Visual Effects ---

def flash_hurt(sprite):
    """Blinks the sprite and shakes it slightly."""
    original_x = sprite.x
    # Quick shake
    animate(sprite, duration=0.1, x=original_x + 10, tween='bounce_end')
    # Blink
    for i in range(3):
        clock.schedule_unique(lambda: setattr(sprite, 'opacity', 0), i * 0.2)
        clock.schedule_unique(lambda: setattr(sprite, 'opacity', 255), i * 0.2 + 0.1)
    # Reset position
    clock.schedule_unique(lambda: setattr(sprite, 'x', original_x), 0.3)

# --- Logic Core ---

def execute_move(attacker_name, defender_name, spell_df, spell_index):
    global message, sub_message, game_active
    
    dmg = float(spell_df[spell_index, "damage"])
    precision = float(spell_df[spell_index, "precision"])
    message = f"{attacker_name.upper()} used {spell_df[spell_index, 'spell'].upper()}!"
    a = random.random()
    spell_successful = a < precision 
    print(a, precision)
    if spell_successful:
        if dmg < 0: # Healing
            amt = abs(dmg)
            hp[attacker_name] = min(100, hp[attacker_name] + amt)
            sub_message = f"It recovered {amt} HP!"
            animate(display, duration=0.6, **{attacker_name: hp[attacker_name]})
        else: # Attacking
            hp[defender_name] = max(0, hp[defender_name] - dmg)
            sub_message = f"It dealt {dmg} damage!"
            # Visual hurt effect
            target_sprite = voldy_sprite if defender_name == "Voldemort" else harry_sprite
            flash_hurt(target_sprite)
            animate(display, duration=0.6, **{defender_name: hp[defender_name]})
    else:
        sub_message = f"The spell did not work!"

    if hp[defender_name] <= 0:
        game_active = False
        message = f"{defender_name.upper()} fainted!"
        sub_message = "The duel is over."

# --- Turn Handlers ---

def voldemort_phase():
    """Voldemort picks a random spell and casts it."""
    global message, sub_message
    if not game_active: return

    options = get_options("Voldemort")
    spell_index = random.randint(1, len(options)) - 1
    execute_move("Voldemort", "Harry", options, spell_index)
    
    # After Voldemort moves, wait 2 seconds then let Harry play
    if game_active:
        clock.schedule_unique(ready_harry, 2.0)

def ready_harry():
    """Resets the UI so Harry can choose a spell."""
    global message, sub_message, waiting_for_input
    message = "What will HARRY do?"
    sub_message = "Select a spell..."
    waiting_for_input = True

def on_mouse_down(pos):
    global waiting_for_input
    
    if game_active and waiting_for_input:
        options = get_options("Harry")[:4]
        for i in range(len(options)):
            x = 40 + (i % 2) * 380
            y = 440 + (i // 2) * 60
            if Rect((x, y), (350, 50)).collidepoint(pos):
                # Harry's action
                waiting_for_input = False
                execute_move("Harry", "Voldemort", options, i)
                
                # If Voldemort is still alive, he takes his turn in 2 seconds
                if game_active:
                    clock.schedule_unique(voldemort_phase, 2.0)

# --- Draw Functions ---

def draw():
    screen.clear()
    screen.draw.filled_rect(Rect((0, 0), (800, 400)), (200, 230, 255)) 
    screen.draw.filled_rect(Rect((0, 400), (800, 200)), (120, 180, 120)) 

    voldy_sprite.draw()
    harry_sprite.draw()

    draw_status_box("VOLDEMORT", display.Voldemort, 50, 50)
    draw_status_box("HARRY", display.Harry, 450, 250)
    
    # Dialogue Box
    screen.draw.filled_rect(Rect((10, 410), (780, 180)), (50, 50, 60))
    screen.draw.rect(Rect((10, 410), (780, 180)), "white")

    if waiting_for_input and game_active:
        draw_move_menu()
    else:
        screen.draw.text(message, (40, 450), fontsize=40, color="white")
        screen.draw.text(sub_message, (40, 510), fontsize=30, color="lightgray")

def draw_status_box(name, val, x, y):
    screen.draw.filled_rect(Rect((x, y), (300, 80)), "white")
    screen.draw.rect(Rect((x, y), (300, 80)), "black")
    screen.draw.text(name, (x+20, y+15), color="black", fontsize=30)
    screen.draw.rect(Rect((x+100, y+45), (160, 15)), "black")
    bw = (val / 100) * 158
    c = "green" if val > 50 else "orange" if val > 20 else "red"
    if bw > 0: screen.draw.filled_rect(Rect((x+101, y+46), (bw, 13)), c)

def draw_move_menu():
    opts = get_options("Harry")[:4]
    for i in range(len(opts)):
        x, y = 40 + (i%2)*380, 440 + (i//2)*60
        screen.draw.rect(Rect((x, y), (350, 50)), "white")
        screen.draw.text(f"> {opts[i, 'spell'].upper()}", (x+20, y+15), fontsize=30)

pgzrun.go()