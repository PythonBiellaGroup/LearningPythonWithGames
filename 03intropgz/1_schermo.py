import pgzrun
# Larghezza
WIDTH = 300
# Altezza
HEIGHT = 300

# Disegna lo schermo
# https://pygame-zero.readthedocs.io/en/stable/builtins.html#screen
def draw():
    # (rosso, verde, blu)
    # https://www.w3schools.com/colors/colors_rgb.asp
    screen.fill((128, 0, 0))

# Fa partire il programma
pgzrun.go()