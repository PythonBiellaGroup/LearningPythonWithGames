import pgzrun

WIDTH = 400
HEIGHT = 400
TITLE = "🐍🐍 Ciao Alieno 🐍🐍"

# https://pygame-zero.readthedocs.io/en/stable/builtins.html#actors
alieno = Actor("alieno")
# pos riferisce al centro dell'immagine
alieno.pos = (200, 250)

def draw():
    screen.fill((0, 80, 125))
    alieno.draw()

def update():
    alieno.left += 2
    if alieno.left > WIDTH:
        alieno.right = 0

pgzrun.go()
