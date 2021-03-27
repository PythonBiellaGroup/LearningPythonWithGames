# Game code is gonna go here!!!!!!
import pygame as pg
import math

WIDTH = 860
HEIGHT = 540

bg = pg.image.load("images/arena.png").convert()
play_Area = Rect((150, 75), (560, 390))

player = Actor("treads.png", center=(WIDTH//2, HEIGHT//2), anchor=('center', 'center'))
turret = Actor("turret.png", center=(player.x, player.y), anchor=('center', 'center'))
pl_movement = [0, 0]
pl_move_speed = 5

pl_rotation = [0, 0]
current_rotation = 0
turn_speed = 5

shooting = False

bullets = []
bullet_speed = 150
fire_rate = 0.15
fire_timer = 0

def on_key_down(key, unicode):
    global shooting
    # Movement
    if key == keys.RIGHT:
        pl_movement[0] += 1

    if key == keys.LEFT:
        pl_movement[0] += -1

    if key == keys.UP:
        pl_movement[1] += -1

    if key == keys.DOWN:
        pl_movement[1] += 1

    if key == keys.D:
        pl_rotation[0] = 1

    if key == keys.A:
        pl_rotation[0] = -1

    if key == keys.W:
        pl_rotation[1] = -1

    if key == keys.S:
        pl_rotation[1] = 1

    print(pl_rotation)
    
def on_key_up(key):
    global shooting
    # Movement
    if key == keys.RIGHT:
        pl_movement[0] = 0

    if key == keys.LEFT:
        pl_movement[0] = 0

    if key == keys.UP:
        pl_movement[1] = 0
        
    if key == keys.DOWN:
        pl_movement[1] = 0
    
    if key == keys.D:
        pl_rotation[0] = 0

    if key == keys.A:
        pl_rotation[0] = 0

    if key == keys.W:
        pl_rotation[1] = 0

    if key == keys.S:
        pl_rotation[1] = 0


def update(dt):
    global shooting, bullets, fire_timer

    # Movement every frame
    player.x += pl_movement[0] * pl_move_speed
    player.y += pl_movement[1] * pl_move_speed

    # Clamp the position
    if player.y - 16 < play_Area.top:
        player.y = play_Area.top + 16
    elif player.y + 16 > play_Area.bottom:
        player.y = play_Area.bottom - 16
    if player.x - 16 < play_Area.left:
        player.x = play_Area.left + 16
    elif player.x + 16 > play_Area.right:
        player.x = play_Area.right - 16
    
    turret.pos = player.pos

    if any([keyboard[keys.W], keyboard[keys.A], keyboard[keys.S], keyboard[keys.D]]):
        shooting = True
    else:
        shooting = False
        fire_timer = fire_rate
    

    if shooting == True:
        # Rotate the turret 
        desired_angle = (math.atan2(-pl_rotation[1], pl_rotation[0]) / (math.pi/180)) - 90
        turret.angle = desired_angle
        fire_timer += dt
        if fire_timer > fire_rate:
            bullet = {}
            bullet["actor"] = Actor("bullet.png", center=player.pos, anchor=('center', 'center'))
            bullet["direction"] = pl_rotation.copy()
            bullet["actor"].x += pl_rotation[0] * 4
            bullet["actor"].y += pl_rotation[1] * 4
            bullets.append(bullet)
            fire_timer = 0
    
    bullets_to_remove = []
    for b in bullets:
        b["actor"].x += b["direction"][0] * bullet_speed * dt
        b["actor"].y += b["direction"][1] * bullet_speed * dt
        if not b["actor"].colliderect(play_Area):
            bullets_to_remove.append(b)
    
    for b in bullets_to_remove:
        bullets.remove(b)


def draw():
    screen.blit(bg, (0, 0))
    player.draw()
    turret.draw()
    for b in bullets:
        b["actor"].draw()