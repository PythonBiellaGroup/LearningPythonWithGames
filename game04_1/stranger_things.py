import pgzrun
import random
import math

TITLE = "Stranger Python"
FONT_COLOR = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
CENTRO_X = WIDTH / 2
CENTRO_Y = HEIGHT / 2
CENTRO = (CENTRO_X, CENTRO_Y)

LIVELLO_FINALE = 8

PERSONAGGI = ["dustin", "lucas", "mike", "undici", "will"]

game_over = False
game_completato = False
livello_corrente = 1
selezione_iniziale = True

personaggio_target = None
personaggi_scelta = []
stelle = []


def draw():
    screen.clear()
    screen.blit("sfondo", (-150, -50))

    if game_over:
        mostra_messaggio("GAME OVER", "Prova di nuovo...")
        return

    if game_completato:
        mostra_messaggio("HAI VINTO!", "Complimenti!")
        return

    if selezione_iniziale:
        screen.draw.text(
            "Scegli il tuo personaggio",
            center=(CENTRO_X, 100),
            fontsize=40,
            color="white",
        )
        for p in personaggi_scelta:
            p.draw()
        return

    for s in stelle:
        s.draw()


def update():
    global stelle, selezione_iniziale, game_over

    if selezione_iniziale:
        return

    if len(stelle) == 0:
        stelle = genera_stelle(livello_corrente)
        return

    for s in stelle:
        # Movimento verticale
        s.y += s.vy

        # Movimento orizzontale + oscillazione sinusoidale
        oscillazione = math.sin(s.timer * 0.1) * s.osc_amp
        s.x += s.vx + oscillazione

        s.timer += 1

        # Rimbalzo ai bordi
        if s.x < 0:
            s.x = 0
            s.vx = -s.vx
        if s.x > WIDTH:
            s.x = WIDTH
            s.vx = -s.vx

        # Cambio direzione casuale ogni tanto
        if random.random() < 0.01:
            s.vx = random.randint(-3, 3)

        # Se tocca il fondo → game over
        if s.y > HEIGHT:
            gestisci_game_over()


def genera_stelle(numero_extra):
    # lista: 1 target + numero_extra distrazioni
    lista = ottieni_personaggi_da_creare(numero_extra)
    nuove = []

    for nome in lista:
        a = Actor(nome)
        a.x = random.randint(100, WIDTH - 100)
        a.y = -50

        # velocità verticale
        a.vy = random.uniform(livello_corrente * 0.3, livello_corrente * 0.6)

        # velocità orizzontale
        a.vx = random.randint(-3, 3)

        # parametri oscillazione
        a.osc_amp = random.uniform(1, 4)
        a.timer = random.randint(0, 1000)

        nuove.append(a)

    return nuove


def ottieni_personaggi_da_creare(num_extra):
    lista = [personaggio_target]
    altri = [p for p in PERSONAGGI if p != personaggio_target]

    for _ in range(num_extra):
        lista.append(random.choice(altri))

    return lista


def on_mouse_down(pos):
    global selezione_iniziale, personaggio_target, livello_corrente, stelle

    if selezione_iniziale:
        for p in personaggi_scelta:
            if p.collidepoint(pos):
                personaggio_target = p.image
                selezione_iniziale = False
                return

    for s in stelle:
        if s.collidepoint(pos):
            if s.image == personaggio_target:
                click_su_target()
            else:
                gestisci_game_over()


def click_su_target():
    global livello_corrente, stelle, game_completato

    if livello_corrente == LIVELLO_FINALE:
        game_completato = True
    else:
        livello_corrente += 1
        stelle = []


def gestisci_game_over():
    global game_over
    game_over = True


def mostra_messaggio(titolo, sottotitolo):
    screen.draw.text(titolo, fontsize=60, center=CENTRO, color=FONT_COLOR)
    screen.draw.text(
        sottotitolo, fontsize=30, center=(CENTRO_X, CENTRO_Y + 30), color=FONT_COLOR
    )


def mostra_schermata_scelta():
    global personaggi_scelta
    personaggi_scelta = []
    distanza = WIDTH / (len(PERSONAGGI) + 1)

    for i, nome in enumerate(PERSONAGGI):
        a = Actor(nome)
        a.x = (i + 1) * distanza
        a.y = HEIGHT / 2
        personaggi_scelta.append(a)


mostra_schermata_scelta()
pgzrun.go()
