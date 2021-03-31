import pgzrun
from random import randint

TITLE = "Balloon Flight"
WIDTH = 800
HEIGHT = 600

balloon = Actor("balloon")
balloon.pos = 400, 300

bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)

house = Actor("house")
house.pos = randint(800, 1600), 460

tree = Actor("tree")
tree.pos = randint(800, 1600), 460

clouds = []
cloud1 = Actor("cloud1")
cloud1.pos = randint(0, 800), randint(50, 200)
clouds.append(cloud1)

cloud2 = Actor("cloud2")
cloud2.pos = randint(0, 800), randint(50, 200)
clouds.append(cloud2)

cloud3 = Actor("cloud3")
cloud3.pos = randint(0, 800), randint(50, 200)
clouds.append(cloud3)

bird_up = True
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
    screen.draw.text("HIGH SCORES", (350, 150), color="black")
    y = 175
    position = 1
    for score in high_scores:
        screen.draw.text(str(position) + ". " + str(score), (350, y), color="black")
        y += 25
        position += 1


def draw():
    screen.blit("background", (0,0))
    if not game_over:
        for cloud in clouds:
            cloud.draw()
        balloon.draw()
        bird.draw()
        house.draw()
        tree.draw()

        screen.draw.text("Score: " + str(score), (700,5), color="navy blue")
    else:
        display_high_score()
        screen.draw.text("GAME OVER!", center=(WIDTH/2, 50), color = "red", fontsize=50)


def on_mouse_down():
    global up
    up = True
    balloon.y -= 50

def on_mouse_up():
    global up
    up = False

def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True

def update():
    global game_over, score, number_of_updates

    if not game_over:
        if not up:
            balloon.y += 1
        
        if bird.x > 0:
            bird.x -= 4
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            score += 1
            number_of_updates = 0
        
        for cloud in clouds:
            if cloud.right > 0:
                cloud.x -= 1
            else:
                cloud.pos = randint(800, 1600), randint(100, 300)
        
        if house.right > 0:
            house.x -= 2
        else:
            house.x = randint(800, 1600)
            score += 1

        if tree.right > 0:
            tree.x -= 4
        else:
            tree.x = randint(800, 1600)
            score += 1

        if balloon.top < 0 or balloon.bottom > 560:
            game_over = True
            update_high_score()
        
        if balloon.collidepoint(bird.x, bird.y) or balloon.collidepoint(house.x, house.y) or balloon.collidepoint(tree.x, tree.y):
            game_over = True
            update_high_score()
            

pgzrun.go()


