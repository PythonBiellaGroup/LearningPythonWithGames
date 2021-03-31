import pgzrun
from random import randint

TITLE = "Karate Training"
WIDTH = 800
HEIGHT = 600

CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
CENTER = (CENTER_X, CENTER_Y)

move_list = []
display_list = []

score = 0
current_move = 0
count = 4
fight_length = 4

say_fight = False
show_countdown = False
moves_complete = False
game_over = False
game_start = False
rounds = 0

karate_kid = Actor("karate-start")
karate_kid.pos = CENTER_X, CENTER_Y + 100

up = Actor("up")
up.pos = CENTER_X, CENTER_Y - 230
right = Actor("right")
right.pos = CENTER_X + 60, CENTER_Y - 170
down = Actor("down")
down.pos = CENTER_X, CENTER_Y - 100
left = Actor("left")
left.pos = CENTER_X - 60, CENTER_Y - 170

def draw():
    global game_over, score, say_fight, count, show_countdown, game_start
    screen.clear()
    screen.blit("stage", (0,0))
    karate_kid.draw()
    up.draw()
    down.draw()
    left.draw()
    right.draw()
    screen.draw.text(
        "Score: " + str(score),
        color = "black", topleft = (10,10),
        fontsize = 30
    )
    if say_fight:
        screen.draw.text(
            "Fight!", color = "white",
            topleft = (CENTER_X - 65, CENTER_Y + 200),
            fontsize = 60
        )
    if show_countdown:
        screen.draw.text(
            str(count), color = "white",
            topleft = (CENTER_X - 8, CENTER_Y + 200),
            fontsize = 60
        )
    if not game_start and not game_over:
        screen.draw.text(
            "Press SPACE to Start", midbottom = CENTER,
            fontsize = 40, color = "orange", owidth = 0.5,
            ocolor = "black", shadow = (1,1), scolor = "black"
        )
    if game_over:
        game_start = False
        screen.draw.text(
            "Oops! Wrong Move.\nPress SPACE to play again",
            color = "orange",
            midbottom = CENTER, fontsize = 40, owidth = 0.5,
            ocolor = "black", shadow = (1,1), scolor = "black"
        )

def update():
    global game_over, current_move, moves_complete, game_start
    if not game_over:
        if moves_complete:
            generate_moves()
            moves_complete = False
            current_move = 0
    else:
        music.stop()

    if keyboard.SPACE and not game_start:
        reset_game()

def reset_game():
    global game_over, game_start, score, fight_length, current_move
    global move_list, display_list, rounds
    game_over = False
    game_start = True
    current_move = 0
    rounds = 0
    score = 0
    fight_length = 4
    move_list = []
    display_list = []
    reset_karate_kid()
    music.play("baseafterbase")
    generate_moves()

def reset_karate_kid():
    global game_over
    if not game_over:
        karate_kid.image = "karate-start"
        up.image = "up"
        right.image = "right"
        left.image = "left"
        down.image = "down"

def update_karate_kid(move):
    global game_over
    if not game_over:
        if move == 0:
            up.image = "up-lit"
            karate_kid.image = "karate-up"
            clock.schedule(reset_karate_kid, 0.5)
        elif move == 1:
            right.image = "right-lit"
            karate_kid.image = "karate-right"
            clock.schedule(reset_karate_kid, 0.5)
        elif move == 2:
            down.image = "down-lit"
            karate_kid.image = "karate-down"
            clock.schedule(reset_karate_kid, 0.5)
        else:
            left.image = "left-lit"
            karate_kid.image = "karate-left"
            clock.schedule(reset_karate_kid, 0.5)
        sounds.shout.play()

def generate_moves():
    global move_list, fight_length, count, show_countdown, say_fight, rounds
 
    count = 4
    move_list = []
    say_fight = False

    rounds += 1
    if rounds % 3 == 0:
        fight_length += 1

    for move in range(0, fight_length):
        rand_move = randint(0,3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    
    show_countdown = True
    countdown()

def display_moves():
    global move_list, display_list, fight_length
    global say_fight, show_countdown, current_move

    if display_list:
        this_move = display_list[0]
        display_list = display_list[1:]

        update_karate_kid(this_move)
        clock.schedule(display_moves, 1)
        # if this_move == 0:
        #     update_karate_kid(0)
        #     clock.schedule(display_moves, 1)
        # elif this_move == 1:
        #     update_karate_kid(1)
        #     clock.schedule(display_moves, 1)
        # elif this_move == 2:
        #     update_karate_kid(2)
        #     clock.schedule(display_moves, 1)
        # else:
        #     update_karate_kid(3)
        #     clock.schedule(display_moves, 1)
    else:
        say_fight = True
        show_countdown = False

def countdown():
    global count, game_over, show_countdown
    if count > 1:
        count -= 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()

def next_move():
    global fight_length, current_move, moves_complete
    if current_move < fight_length - 1:
        current_move += 1
    else:
        moves_complete = True

def on_key_down(key):
    global score, game_over, move_list, current_move
    if key == keys.UP:
        update_karate_kid(0)
        if move_list[current_move] == 0:
            score += 1
            next_move()
        else:
            game_over = True
    elif key == keys.RIGHT:
        update_karate_kid(1)
        if move_list[current_move] == 1:
            score += 1
            next_move()
        else:
            game_over = True
    elif key == keys.DOWN:
        update_karate_kid(2)
        if move_list[current_move] == 2:
            score += 1
            next_move()
        else:
            game_over = True
    elif key == keys.LEFT:
        update_karate_kid(3)
        if move_list[current_move] == 3:
            score += 1
            next_move()
        else:
            game_over = True

pgzrun.go()