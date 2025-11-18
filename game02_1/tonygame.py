from pgzero.actor import Actor
from pgzero.clock import clock
from pgzero.keyboard import keyboard
import pgzrun
from random import randint

TITLE = "tony alla ricerca della musica"
WIDTH = 600
HEIGHT = 500

punteggio = 0
ha_preso_nota = False
game_over = False

tony = Actor("tony")
tony.pos = 100, 100

nota = Actor("nota musicale")


def draw():
    screen.blit("sfondo", (0, 0))
    nota.draw()
    tony.draw()
    screen.draw.text(
        "Note imparate: " + str(punteggio), color="black", topleft=(10, 10)
    )

    if game_over:
        screen.fill("pink")
        screen.draw.text(
            "Tempo scaduto! Note messe insieme: " + str(punteggio),
            midtop=(WIDTH / 2, 10),
            fontsize=40,
            color="red",
        )


def piazza_nota():
    nota.x = randint(70, (WIDTH - 70))
    nota.y = randint(70, (HEIGHT - 70))


def tempo_scaduto():
    global game_over
    game_over = True


def torna_concentrato():
    tony.image = "tony"


def update():
    global punteggio

    if keyboard.left:
        tony.x -= 5
    if keyboard.right:
        tony.x += 5
    if keyboard.up:
        tony.y -= 5
    if keyboard.down:
        tony.y += 5

    nota_presa = tony.colliderect(nota)

    if nota_presa:
        punteggio += 1
        tony.image = "tony2"
        sounds.tonyaudio2.play()
        piazza_nota()
        clock.schedule(torna_concentrato, 1.0)


piazza_nota()
clock.schedule(tempo_scaduto, 60.0)
pgzrun.go()
