import pgzrun
from random import randint

TITLE = "Mongolfiera"
WIDTH = 800
HEIGHT = 600

mongolfiera = Actor("mongolfiera")
mongolfiera.pos = 400, 300

uccello = Actor("uccello-up")
uccello.pos = randint(800, 1600), randint(10, 200)

casa = Actor("casa")
casa.pos = randint(800, 1600), 460

albero = Actor("albero")
albero.pos = randint(800, 1600), 460

nuvole = []
nuvola1 = Actor("nuvola1")
nuvola1.pos = randint(0, 800), randint(50, 200)
nuvole.append(nuvola1)

nuvola2 = Actor("nuvola2")
nuvola2.pos = randint(0, 800), randint(50, 200)
nuvole.append(nuvola2)

nuvola3 = Actor("nuvola3")
nuvola3.pos = randint(0, 800), randint(50, 200)
nuvole.append(nuvola3)

uccello_up = True
up = False
game_over = False
score = 0
number_of_updates = 0

high_scores = []

def update_high_score():
    global score, high_scores
    high_scores = []
    file_name = "high-score.txt"

    try:
        with open(file_name, "r") as hsFile:
            for line in hsFile:
                high_scores.append(int(line.rstrip()))
    except:
        pass

    high_scores.append(score)
    high_scores.sort(reverse=True)

    with open(file_name, "w") as hsFile:
        for high_score in high_scores:
            hsFile.write(str(high_score) + "\n")

def display_high_score():
    global high_scores
    screen.draw.text("PUNTEGGI MIGLIORI", (350, 150), color="black")
    y = 175
    position = 1
    for score in high_scores:
        screen.draw.text(str(position) + ". " + str(score), (350, y), color="black")
        y += 25
        position += 1


def draw():
    screen.blit("sfondo", (0,0))
    if not game_over:
        for nuvola in nuvole:
            nuvola.draw()
        mongolfiera.draw()
        uccello.draw()
        casa.draw()
        albero.draw()

        screen.draw.text("Punteggio: " + str(score), (700,5), color="navy blue")
    else:
        display_high_score()
        screen.draw.text("GAME OVER!", center=(WIDTH/2, 50), color = "red", fontsize=50)


def on_mouse_down():
    global up
    up = True
    mongolfiera.y -= 50

def on_mouse_up():
    global up
    up = False

def flap():
    global uccello_up
    if uccello_up:
        uccello.image = "uccello-down"
        uccello_up = False
    else:
        uccello.image = "uccello-up"
        uccello_up = True

def update():
    global game_over, score, number_of_updates

    if not game_over:
        if not up:
            mongolfiera.y += 1
        
        if uccello.x > 0:
            uccello.x -= 4
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            uccello.x = randint(800, 1600)
            uccello.y = randint(10, 200)
            score += 1
            number_of_updates = 0
        
        for nuvola in nuvole:
            if nuvola.right > 0:
                nuvola.x -= 1
            else:
                nuvola.pos = randint(800, 1600), randint(100, 300)
        
        if casa.right > 0:
            casa.x -= 2
        else:
            casa.x = randint(800, 1600)
            score += 1

        if albero.right > 0:
            albero.x -= 4
        else:
            albero.x = randint(800, 1600)
            score += 1

        if mongolfiera.top < 0 or mongolfiera.bottom > 560:
            game_over = True
            update_high_score()
        
        if mongolfiera.collidepoint(uccello.x, uccello.y) or mongolfiera.collidepoint(casa.x, casa.y) or mongolfiera.collidepoint(albero.x, albero.y):
            game_over = True
            update_high_score()
            

pgzrun.go()

