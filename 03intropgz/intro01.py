import pgzrun

WIDTH = 400
HEIGHT = 400
TITLE = "🐍🐍 Ciao Alieno 🐍🐍"

alieno = Actor("alieno")
alieno.pos = (200, 250)

def draw():
    screen.fill((0, 80, 125))
    alieno.draw()

def update():
    alieno.left += 2
    if alieno.left > WIDTH:
        alieno.right = 0

pgzrun.go()
