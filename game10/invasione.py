import pgzrun
from random import randint
import math

TITLE = "Invasione dallo spazio"
WIDTH = 800
HEIGHT = 700
CENTRO_X = WIDTH / 2
CENTRO_Y = HEIGHT / 2

aliens = []
lasers = []
move_sequence = 0
move_counter = 0
move_delay = 30
score = 0

initial_player_position = (400, 600)
player = Actor("player", initial_player_position)

def draw():
    screen.blit("sfondo", (0,0))
    player.image = player.images[math.floor(player.status/6)]
    player.draw()
    draw_aliens()
    draw_lasers()
    draw_lives()
    screen.draw.text(
        str(score), topright = (780,10), owidth=0.5,
        ocolor = (255,255,255), color=(0,64,255), fontsize=60
    )
    if len(aliens) == 0:
        draw_center_text("HAI VINTO!\nPremi INVIO per giocare ancora")
    if player.status >= 30:
        if player.lives == 0:
            draw_center_text("GAME OVER\nPremi INVIO per giocare ancora")
        else:
            draw_center_text("SEI STATO COLPITO\nPremi INVIO per il prossimo livello")

            
def draw_center_text(message):
    screen.draw.text(
        message, center = (CENTRO_X,CENTRO_Y),
        owidth = 0.5, ocolor = (255,255,255), color = (255,64,0),
        fontsize = 60
    )


def draw_lives():
    for lv in range(player.lives):
        screen.blit("vita", (10 + (lv*32), 10))


def update():
    global move_counter, lasers
    if player.status < 30 and len(aliens) > 0:
        check_keys()
        update_lasers()
        move_counter += 1
        if move_counter == move_delay:
            update_aliens()
            move_counter = 0
        if player.status > 0:
            player.status += 1
            if player.status == 30:
                player.lives -= 1
    else:
        if keyboard.RETURN:
            if player.lives > 0:
                lasers = []
                player.pos = initial_player_position
                player.status = 0
            if player.lives == 0 or len(aliens) == 0:
                init_game()

def check_keys():
    global lasers
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5
    if keyboard.space:
        if player.laser_active == 1:
            player.laser_active = 0
            sounds.laser.play()
            clock.schedule(make_laser_active, 1.0)
            l = len(lasers)
            lasers.append(Actor("laser2",(player.x, player.y-32)))
            lasers[l].status = 0
            lasers[l].type = 1

def make_laser_active():
    player.laser_active = 1


def draw_lasers():
    for laser in lasers:
        laser.draw()


def update_lasers():
    global lasers, aliens
    for laser in lasers:
        if laser.type == 0:
            alien_laser_hit(laser)
            laser.y += 2
            if laser.y > HEIGHT:
                laser.status = 1
        if laser.type == 1:
            player_laser_hit(laser)
            laser.y -= 5
            if laser.y < 10:
                laser.status = 1

    aliens = list_clean_up(aliens)
    lasers = list_clean_up(lasers)


def list_clean_up(l):
    new_list = []
    for i in range(len(l)):
        if l[i].status == 0: new_list.append(l[i])
    return new_list

def player_laser_hit(laser):
    global score
    for alien in aliens:
        if alien.collidepoint(laser.x, laser.y):
            sounds.eep.play()
            laser.status = 1
            alien.status = 1
            score += 1000


def alien_laser_hit(laser):
    if player.collidepoint(laser.x, laser.y):
        player.status = 1
        laser.status = 1
        sounds.explosion.play()


def init_aliens():
    global aliens
    aliens = []
    for a in range(18):
        alienX = 210 + (a % 6) * 80
        alienY = 100 + int(a/6) * 64
        aliens.append(Actor("alien1", (alienX, alienY)))
        aliens[a].status = 0


def draw_aliens():
    for alien in aliens:
        alien.draw()


def update_aliens():
    global move_sequence, lasers
    move_x = move_y = 0
    if move_sequence < 10 or move_sequence > 30:
        move_x = -15
    if move_sequence == 10 or move_sequence == 30:
        move_y = 50
    if move_sequence > 10 and move_sequence < 30:
        move_x = 15

    for alien in aliens:
        animate(
            alien, pos=(alien.x + move_x, alien.y + move_y),
            duration = 0.5, tween = "linear"
        )
        if randint(0,1) == 0:
            alien.image = "alien1"
        else:
            alien.image = "alien1b"
            if randint(0, 10) == 0:
                l = len(lasers)
                lasers.append(Actor("laser1", midtop=alien.midbottom))
                lasers[l].status = 0
                lasers[l].type = 0
    
    move_sequence += 1
    if move_sequence == 40:
        move_sequence = 0


def init_game():
    global lasers
    player.lives = 3
    player.laser_active = 1
    player.status = 0
    player.pos = initial_player_position
    player.images = ["player","explosion1","explosion2","explosion3","explosion4","explosion5"]
    init_aliens()
    lasers = []


init_game()
pgzrun.go()