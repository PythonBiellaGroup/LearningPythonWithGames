import pgzrun

WIDTH = 400
HEIGHT = 400
TITLE = "🐍🐍 Ciao alieno 🐍🐍"

alieno = Actor("alieno")
alieno.pos = (200, 250)

hit = False

def draw():
    screen.fill((0, 80, 125))
    if hit:
        screen.draw.textbox("Ahia!", (100, 100, 200, 50))
    alieno.draw()

def update():
    alieno.left += 2
    if alieno.left > WIDTH:
        alieno.right = 0

def on_mouse_down(pos):
    if alieno.collidepoint(pos):
        set_alieno_ferito()

def set_alieno_ferito():
    global hit
    alieno.image = "alieno_ferito"
    hit = True
    # https://pygame-zero.readthedocs.io/en/stable/builtins.html#clock
    clock.schedule_unique(set_alieno_normale, 1.0)

def set_alieno_normale():
    global hit
    alieno.image = "alieno"
    hit = False

pgzrun.go()
