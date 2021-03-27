import random

# Set the screen dimensions
WIDTH = 540
HEIGHT = 540

# Colour variables
c_grass = (0, 153, 76)
c_road = (204, 136, 0)

# Lists to hold pieces 
road = [] # To be drawn on screen
queue = [] # To be added when scrolling

# Height of my road pieces
block_size = 2

# Player actor and a speed to move it at
player = Actor("car.png", (int(WIDTH/2 - 16), 390), anchor=("left", "top"))
speed = 5

# Initial population of the road and queue
buffer = int(WIDTH/4)
for i in range(HEIGHT-block_size, -block_size, -block_size):
    block = Rect((buffer, i), (int(WIDTH/2), block_size))
    road.append(block)
for i in range(0, 200, block_size):
    block = Rect((buffer, 0), (int(WIDTH/2), block_size))
    queue.append(block)

# Function that will scroll the road
def scroll_road():
    global road, queue
    for piece in road: # Move all the pieces down by 2
        piece.top += block_size
    road.append(queue.pop(0)) # Move piece from queue to road
    road.pop(0) # Remove the bottom road piece
    road[-1].top = 0 # An index of -1 is the last item in a list
    if len(queue) < 5:
        update_path() # If the queue is getting low update the path

# Scroll the road at a set interval - 60 scrolls (frames) per second
frame_rate = 1/60
clock.schedule_interval(scroll_road, frame_rate) 

# Road should not go any closer than 50 pixels to the edge
min_buffer = 50

# Make sure the road doesn't exceed my buffer
def clamp_road(x):
    if x < min_buffer: 
        x = min_buffer
    if x > int(WIDTH/2) - min_buffer:
        x = int(WIDTH/2) - min_buffer
    return x

min_turn = 200
turn_gap = 200

def update_path():
    global road, queue
    choice = random.randint(0, 1) # Right or left turn
    current_pos_x = queue[-1].left
    if choice == 0: 
        # Turn left
        modifier = -1
        if current_pos_x - min_turn > min_buffer:
            turn = random.randint(min_turn, current_pos_x - 5)
        else:
            turn = current_pos_x - min_buffer
    else: 
        # Turn right
        modifier = 1
        if int(WIDTH/2) - current_pos_x - min_buffer > min_turn:
            turn = random.randint(min_turn, int(WIDTH/2) - current_pos_x - min_buffer)
        else:
            turn = int(WIDTH/2) - current_pos_x - min_buffer
    # Choose how long my turn will take
    height = random.randint(200, 400)
    # Move a percentage of the turn for each block in height
    for y in range(block_size, height, block_size):
        x = turn/height * y * modifier
        new_x = clamp_road(current_pos_x + x)
        block = Rect((new_x, 0), (int(WIDTH/2), block_size))
        queue.append(block)
    # Find the last x co-ordinate of the turn
    current_pos_x = queue[-1].left
    # Add some straight to the road
    for i in range(0, turn_gap, block_size):
        block = Rect((current_pos_x, 0), (int(WIDTH/2), block_size))
        queue.append(block)

def update():
    # Player movement
    global player
    player_momentum = 0
    if keyboard.left:
        player_momentum = -speed
    elif keyboard.right:
        player_momentum = speed
    else:
        player_momentum = 0
    new_pos = player.x + player_momentum
    collision = False
    for i in range(16):
        if new_pos > road[75+i].left and new_pos + player.width < road[75+i].x + road[75+i].width:
            collision = True
    if collision == True:
        player.x = new_pos

def draw():
    screen.fill(c_grass)
    for piece in road:
        screen.draw.rect(piece, c_road) 
    player.draw()