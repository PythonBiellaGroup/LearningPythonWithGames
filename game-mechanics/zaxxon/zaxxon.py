# Zaxxon
import json

WIDTH = 400
HEIGHT = 500

gameState = count = shipHeight = 0

with open('mapdata.json') as json_file:
    mapData = json.load(json_file)
    mapBlocks = mapData['blocks']
    mapBlockTypes = mapData['blocktypes']
    mapWidth = mapData['width']
    mapLength = mapData['length']

mapPosX = 200 + (mapLength*32)
mapPosY = 150 - (mapLength*16)
shipPos = [50,300]

def draw():
    screen.fill((0,0,0))
    drawMap()
    screen.draw.text("PyGame Zero Zaxxon \nCursor Keys to Control", (10, 10), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=30)
    screen.draw.text("Altitude : "+ str(shipHeight), topright=(390, 460), owidth=0.5, ocolor=(255,0,0), color=(255,255,0) , fontsize=30)
    
def drawMap():
    global gameState
    shipBlock = getShipXY()
    shipFrame = "0"
    if keyboard.left: shipFrame = "-1"
    if keyboard.right: shipFrame = "1"
    for x in range(0, mapWidth):
        for y in range(0, mapLength):
            bx = (x*32) - (y*32) + mapPosX
            by = (y*16) + (x*16) + mapPosY
            if -64 <= bx < WIDTH + 32 and -64 <= by < HEIGHT + 64:        
                if mapBlocks[x][y] > 0:
                    if shipBlock == [x,y]:
                        if mapBlockTypes[mapBlocks[shipBlock[0]][shipBlock[1]]]['height'] > shipHeight+32 : gameState = 1
                    screen.blit(mapBlockTypes[mapBlocks[x][y]]['image'], (bx, by-mapBlockTypes[mapBlocks[x][y]]['height']))
                if shipBlock == [x-1,y-1]:
                    if(gameState == 0 or count%4 == 0):
                        screen.blit("shadow"+shipFrame,(shipPos[0],shipPos[1]+10))
                        screen.blit("ship"+shipFrame,(shipPos[0],shipPos[1]-shipHeight))
                    
    if shipBlock[1] >= mapLength-1 or shipBlock[1] < 0 or shipBlock[0] == mapWidth-1:
        screen.blit("shadow"+shipFrame,(shipPos[0],shipPos[1]+10))
        screen.blit("ship"+shipFrame,(shipPos[0],shipPos[1]-shipHeight))

def update():
    global count, gameState, mapPosX, mapPosY, shipHeight
    if gameState == 0:
        mapPosX -=1
        mapPosY +=0.5
        shipBlock = getShipXY()
        if keyboard.left:
            if shipBlock[0] > 0:
                shipPos[0] -=1
                shipPos[1] -=0.5
        if keyboard.right:
            if shipBlock[0] < mapWidth-1:
                shipPos[0] +=1
                shipPos[1] +=0.5
        if keyboard.up: shipHeight = max(min(85, shipHeight+1), 0)
        if keyboard.down: shipHeight = max(min(85, shipHeight-1), 0)
    count += 1

def getShipXY():
    x = ((shipPos[0]+82)/32)
    y = mapLength - ((shipPos[1]/16) + (mapPosY/16) + ((mapWidth/2)-x))-2
    return [int(x),int(y)]
