import pgzrun
#Larghezza
WIDTH = 300
#Altezza
HEIGHT = 300

#Disegna lo schermo
def draw():
    # (rosso, verde, blu)
    screen.fill((128, 0, 0))

#Fa partire il programma
pgzrun.go()

# Esempio di assets.json
# {
#   "images": {
#     "ficco": {
#       "src": "https://raw.githubusercontent.com/PythonBiellaGroup/LearningPythonWithGames/main/01/images/snowflake.png"
#     }
#   }
# }