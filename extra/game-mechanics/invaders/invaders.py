# https://github.com/Wireframe-Magazine/Wireframe-9
# Wireframe #9: Space Invaders' disintegrating shields, pages 32-33

import pgzrun
from random import randint

WIDTH,HEIGHT = 1200, 700 # Dimensions of the screen (pixels)
shots, to_delete, first_frame = [], [], True

def create_random_shot():
    shots.append({'pos': [randint(0, (WIDTH-images.shot.get_width())/10)*10, 0],
                  'sprite': images.shot,
                  'exploding': False})

# A shot will be created in a random position every half second
clock.schedule_interval(create_random_shot, 0.5) # Try reducing number to 0.1!

def draw():
    global first_frame, to_delete
    if first_frame:
        for x in range(50, WIDTH, 300):
            screen.blit(images.shield, [x, 500])
        first_frame = False

    for item in to_delete:
        screen.blit(item['sprite'], item['pos'])
    to_delete = []  # Clear list

    for shot in shots:
        screen.blit(shot['sprite'], shot['pos'])

def update(dt):
    # Step backwards through the shots list. This avoids errors that occur
    # when deleting items from the list during the for loop.
    for i in range(len(shots)-1, -1, -1):
        shot = shots[i]
        if shot['exploding']:
            shot['timer'] -= 1
            if shot['timer'] <= 0:
                to_delete.append({'pos':shot['pos'],'sprite':images.explode_black})
                del shots[i]
        else:
            # Before moving shot, add the current position to the to_delete list
            to_delete.append({'pos':shot['pos'].copy(),'sprite':images.shot_black})
            shot['pos'][1] += 20    # Move down the screen
            # Do collision detection based on the centre of the sprite
            half_width = shot['sprite'].get_width() // 2   # // = integer divide
            half_height = shot['sprite'].get_height() // 2
            if shot['pos'][1]+half_height >= HEIGHT:
                del shots[i]    # Gone off bottom of screen
            else:
                # Hit something? If so change to exploding sprite
                collide_check_pos = (shot['pos'][0]+half_width,
                                     shot['pos'][1]+half_height)
                if screen.surface.get_at(collide_check_pos) != (0,0,0):
                    shot['sprite'] = images.explode
                    shot['exploding'] = True
                    shot['timer'] = 5

pgzrun.go()