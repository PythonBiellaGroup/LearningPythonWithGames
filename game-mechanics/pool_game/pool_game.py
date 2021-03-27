import math
import time

WIDTH = 760
HEIGHT = 380

class Ball:
    def __init__(self, image, pos):
        self.actor = Actor(image, center=pos, anchor=("center", "center"))
        self.movement = [0, 0]
        self.pocketed = False 
    
    def move(self):
        self.actor.x += self.movement[0]
        self.actor.y += self.movement[1]
        if self.pocketed == False:
            if self.actor.y < playArea.top + 16 or self.actor.y > playArea.bottom-16:
                self.movement[1] = -self.movement[1]
                self.actor.y = clamp(self.actor.y, playArea.top+16, playArea.bottom-16)
            if self.actor.x < playArea.left+16 or self.actor.x > playArea.right-16:
                self.movement[0] = -self.movement[0]
                self.actor.x = clamp(self.actor.x, playArea.left+16, playArea.right-16)      
        else:
            self.actor.x += self.movement[0]
            self.actor.y += self.movement[1]
        self.resistance()
    
    def resistance(self):
        # Slow the ball down
        self.movement[0] *= 0.95
        self.movement[1] *= 0.95

        if abs(self.movement[0]) + abs(self.movement[1]) < 0.4:
            self.movement = [0, 0]
    
    def collide(self, ball):
        collision_normal = [ball.actor.x - self.actor.x, ball.actor.y - self.actor.y]
        ball_speed = math.sqrt(collision_normal[0]**2 + collision_normal[1]**2)
        self_speed  = math.sqrt(self.movement[0]**2 + self.movement[1]**2)
        if self.movement[0] == 0 and self.movement[1] == 0:
            ball.movement[0] = -ball.movement[0]
            ball.movement[1] = -ball.movement[1]
        elif ball_speed > 0:
            collision_normal[0] *= 1/ball_speed
            collision_normal[1] *= 1/ball_speed
            ball.movement[0] = collision_normal[0] * self_speed
            ball.movement[1] = collision_normal[1] * self_speed


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest)) 

playArea = Actor("playarea.png", center=(WIDTH//2, HEIGHT//2))

balls = []       
cue_ball = Ball("cue_ball.png", (WIDTH//2, HEIGHT//2))
balls.append(cue_ball)
balls.append(Ball("ball_1.png", (WIDTH//2 - 75, HEIGHT//2)))
balls.append(Ball("ball_2.png", (WIDTH//2 - 150, HEIGHT//2)))

pockets = []
pockets.append(Actor("pocket.png", topleft=(playArea.left, playArea.top), anchor=("left", "top")))
# I create one of these actors for each pocket, they are not drawn
pockets.append(Actor("pocket.png", bottomleft=(playArea.left, playArea.bottom), anchor=("left", "bottom")))
pockets.append(Actor("pocket.png", bottomright=(playArea.right, playArea.bottom), anchor=("right", "bottom")))
pockets.append(Actor("pocket.png", topright=(playArea.right, playArea.top), anchor=("right", "top")))

shot_rotation = 270.0 # Start pointing up table
turn_speed = 1
line = [] # To hold the points on my line
line_gap = 1/12
max_line_length = 400

shot = False
ball_speed = 30

def update():
    global shot_rotation, shot, line, cue_ball, balls
    
    ## Rotate your aim
    if keyboard[keys.LEFT] and not shot:
        shot_rotation -= 1 * turn_speed
    if keyboard[keys.RIGHT] and not shot:
        shot_rotation += 1 * turn_speed

    

    # Make the rotation wrap around
    if shot_rotation > 360:
        shot_rotation -= 360
    if shot_rotation < 0:
        shot_rotation += 360

    # Work out the Vector that corresponds to the rotation
    rot_radians = shot_rotation * (math.pi/180) 

    x = math.sin(rot_radians)
    y = -math.cos(rot_radians)

    ## Inside update
    ## Shoot the ball with the space bar
    if keyboard[keys.SPACE] and not shot:
        shot = True
        cue_ball.movement = [x*ball_speed, y*ball_speed]
    
    if not shot:
        current_x = cue_ball.actor.x
        current_y = cue_ball.actor.y 
        length = 0
        line = []
        while length < max_line_length:
            hit = False
            if current_y < playArea.top or current_y > playArea.bottom:
                y = -y
                hit = True
            if current_x < playArea.left or current_x > playArea.right:
                x = -x
                hit = True
            if hit == True:
                line.append((current_x-(x*line_gap), current_y-(y*line_gap)))
            length += math.sqrt(((x*line_gap)**2)+((y*line_gap)**2) )
            current_x += x*line_gap
            current_y += y*line_gap
        line.append((current_x-(x*line_gap), current_y-(y*line_gap)))
    # Shoot the ball and move all the balls on the table
    else:
        shot = False
        balls_pocketed = []
        collisions = []
        for b in balls:
            # Move each ball
            b.move()
            print(b.movement)
            if abs(b.movement[0]) + abs(b.movement[1]) > 0:
                shot = True
            # Check for collisions
            for other in balls:
                if other != b and b.actor.colliderect(other.actor):
                    collisions.append((b, other))
            # Did it sink in the hole?
            in_pocket = b.actor.collidelistall(pockets)
            if len(in_pocket) > 0 and b.pocketed == False:
                if b != cue_ball:
                    b.movement[0] = (pockets[in_pocket[0]].x - b.actor.x) / 20
                    b.movement[1] = (pockets[in_pocket[0]].y - b.actor.y) / 20
                    b.pocketed = True
                    balls_pocketed.append(b)
                else:
                    b.x = WIDTH//2
                    b.y = HEIGHT//2 
        for col in collisions:
            col[0].collide(col[1])
        if shot == False:
            for b in balls_pocketed:
                balls.remove(b)


def draw():
    global line
    screen.blit('table.png', (0, 0))
    playArea.draw()
    if not shot:
        screen.draw.line(cue_ball.actor.pos, line[0], (255, 255, 255))
        for l in range(len(line) - 1):
            screen.draw.line(line[l], line[l+1], (255, 255, 255))
    for ball in balls:
        if ball.pocketed == False:
            ball.actor.draw()
    