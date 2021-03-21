# https://github.com/Wireframe-Magazine/Wireframe-5cd 
# Wireframe #5 Source 
# A retro style high score table, pages 32-33

# highscore list is initially filled with low scores
highscores = [(0,'Player') for i in range(10)]

# 'addscore()' function takes a score and (if high enough)
# adds to the list in the correct position, along with a name
def addscore(score):
    global highscores
    # only add the score if it is greater than the
    # current lowest score in the highscores list
    if score < highscores[9][0]:
        return
    # get the player's name
    name = input('High score! What is your name? ')
    # starting at 0, increment the 'pos' variable
    # until it's at the position to insert the score
    pos = 0
    while pos < len(highscores) and score <= highscores[pos][0]:
        pos += 1
    # add the (score, name) tuple
    # at the correct place in the list
    highscores = highscores[:pos] + [(score,name)] + highscores[pos:]
    # only store the top 10 scores in the list
    highscores = highscores[:10]

# prints the table to standard output
def drawtabletext():
    # print the table headings
    print('Score\tName')
    # print each score and name pair in order
    for s in highscores:
        print("{0}\t{1}".format(s[0],s[1]))

# prints the table in Pygame Zero
def drawtablepygame():
    # print the table headings
    screen.draw.text('Score', topleft=(50,50), fontsize=40)
    screen.draw.text('Name', topleft=(150,50), fontsize=40)
    # using 'enumerate()' gives the position of each tuple in the list
    # which is used to calculate the vertical draw position of the data
    for pos,data in enumerate(highscores):
        screen.draw.text(str(data[0]), topleft=(50,100+(pos*50)), fontsize=40)
        screen.draw.text(data[1], topleft=(150,100+(pos*50)), fontsize=40)

def draw():
    drawtablepygame()

# use the 'addscore()' function to add some scores
addscore(64)
addscore(30)
addscore(87)

# print the populated table
drawtabletext()
