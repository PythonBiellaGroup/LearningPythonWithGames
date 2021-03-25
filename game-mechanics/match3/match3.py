from random import randint

WHITE = 255,255,255

# board screen position and tile size
boardx = 40
boardy = 40
tilesize = 40

# board size
columns = 8
rows = 12

# number of different tile colours
numberoftiles = 9

# calculate window size
WIDTH = (boardx * 2) + (tilesize * columns)
HEIGHT = (boardy * 2) + (tilesize * rows)

# build the board
# start with the same tile in all positions
tiles = [[1] * columns for j in range(rows)]
# ensure there are no matches initially
for r in range(rows):
    for c in range(columns):
        tiles[r][c] = randint(1, numberoftiles-1)
        # replace a tile if it is the same as either
        # the tile above or to the left
        while (r>0 and tiles[r][c] == tiles[r - 1][c]) or (c > 0 and tiles[r][c] == tiles[r][c - 1]):
            tiles[r][c] = randint(1, numberoftiles - 1)

# selected tile cursor left-most position
selected = [0,0]

# check for matches of 3 or more tiles on the board
# and return a list of lists of tile positions
def checkmatches():
    matches = []
    # check vertical matches
    for c in range(columns):
        currentmatch = []
        for r in range(rows):
            # add a tile as a match if it's the same colour as the
            # previous tile, or if it's the start of a new match
            if currentmatch == [] or tiles[r][c] == tiles[r - 1][c]:
                currentmatch.append((r,c))
            else:
                # if not, add the current match to the list of matches...
                if len(currentmatch) >= 3:
                    matches.append(currentmatch)
                # ...and start a new match list
                currentmatch = [(r,c)]
        # add the final match
        if len(currentmatch) >= 3:
            matches.append(currentmatch)
    # check horizontal matches
    for r in range(rows): #columns
        currentmatch = []
        for c in range(columns):
            if currentmatch == [] or tiles[r][c] == tiles[r][c - 1]:
                currentmatch.append((r,c))
            else:
                if len(currentmatch) >= 3:
                    matches.append(currentmatch)
                currentmatch = [(r,c)]
        if len(currentmatch) >= 3:
            matches.append(currentmatch)

    return matches

# set each tile in a match to 'None'
def clearmatches(matches):
    for match in matches:
        for position in match:
            tiles[position[0]][position[1]] = None

# fill empty board spaces with a tile
def fillboard():
    # check each column
    for c in range(columns):
        # check each row
        for r in range(rows):
            if tiles[r][c] == None:
                # if a board space is empty, move the tile above
                # into the empty space, and cascade upwards
                for rr in range(r,0,-1):
                    tiles[rr][c] = tiles[rr - 1][c]
                tiles[0][c] = randint(1, numberoftiles - 1)
                # ensure the new tile doesn't make a match with tiles
                # above, or to the left or right
                while tiles[0][c] == tiles[1][c] or (c > 0 and tiles[0][c] == tiles[0][c-1]) or (c<columns-1 and tiles[0][c] == tiles[0][c+1]):
                    tiles[0][c] = randint(1, numberoftiles - 1)

def on_key_up(key):
    # arrow keys change the selected tile
    if key == keys.LEFT:
        selected[0] = max(0,selected[0] - 1)
    if key == keys.RIGHT:
        selected[0] = min(selected[0] + 1,columns - 2)
    if key == keys.UP:
        selected[1] = max(0,selected[1] - 1)
    if key == keys.DOWN:
        selected[1] = min(selected[1] + 1,rows - 1)
    # space swaps the two selected tiles
    # checks for matches, deletes them and
    # fill any empty spaces on the board
    if key == keys.SPACE:
        tiles[selected[1]][selected[0]], tiles[selected[1]][selected[0] + 1] = tiles[selected[1]][selected[0] + 1], tiles[selected[1]][selected[0]]
        matches = checkmatches()
        clearmatches(matches)
        fillboard()

def draw():
    screen.clear()
    # draw the board
    for r in range(rows):
        for c in range(columns):
            screen.blit(str(tiles[r][c]), (boardx + (c * tilesize), boardy + (r * tilesize)))
    # draw the selected tiles
    screen.blit('selected',(boardx+(selected[0] * tilesize), boardy + (selected[1] * tilesize)))
