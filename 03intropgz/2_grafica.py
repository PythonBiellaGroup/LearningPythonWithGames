import pgzrun
# Larghezza
WIDTH = 500
# Altezza
HEIGHT = 500

def draw():
    screen.clear()
    screen.draw.circle((250, 250), 50, "white")
    screen.draw.filled_circle((250, 100), 50, "red")
    screen.draw.line((150, 20), (150, 450), "purple")
    screen.draw.line((150, 20), (350, 20), "purple")

# Fa partire il programma
pgzrun.go()

'''
ESERCIZIO
Finisci di disegnare il semaforo
'''