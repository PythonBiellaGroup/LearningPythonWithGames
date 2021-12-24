# Player movement prototype program:
# - Cursor left-right: move player
# - Cursor up: player jump
# - Space: shoot a collectable piece
import pgzrun
from random import randint
from pygame import image, Color, Surface
from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import translate
import math

surfaces = [[(0, 567), (135, 570), (312, 566), (566, 563), (731, 570), (799, 569)], [(85, 472), (188, 469), (287, 470)],
            [(457, 472), (592, 469), (705, 470)], [(247, 336), (370, 334), (489, 335)],
            [(73, 232), (153, 226), (264, 220), (357, 221)], [(437, 223), (606, 219), (727, 219)],
            [(150, 97), (53, 90), (0, 89)], [(603, 95), (715, 91), (799, 89)], [(288, 26), (421, 24), (521, 22)],
            [(61, -101), (188, -106), (326, -106)], [(447, -103), (601, -109), (757, -109)],
            [(271, -217), (388, -217), (520, -219)], [(221, -329), (87, -327), (0, -327)],
            [(532, -327), (693, -331), (799, -333)], [(184, -463), (344, -463), (516, -464), (652, -466)],
            [(193, -588), (104, -615), (29, -644), (0, -649)],
            [(618, -585), (722, -638), (789, -667), (799, -669)], [(0, -750), (799, -750)]]
surfaceLines = [LineString(surfaces[i]) for i in range(len(surfaces))]

playerHalfSize = 15
playerAccelerationDown = 0.5
playerJumpSpeed = 12
playerTerminalSpeed = 12
playerLateralSpeed = 4
coyoteTimeVerticalSpeed = 4

screenPosition = 0

collectableHalfSize = 10

class CollectableFlying:
    def __init__(self, startX, startY):
        self.centre = [startX, startY]
        self.speedX = randint(-startX,800-startX)/100
        self.speedY = randint(-6,-4)  #-5
        self.accelerationDown = 0.1
        #print(str(self.centre))
    def draw(self):
        points = [(self.centre[0]-collectableHalfSize, self.centre[1]),
                  (self.centre[0], self.centre[1]-collectableHalfSize),
                  (self.centre[0]+collectableHalfSize, self.centre[1]),
                  (self.centre[0], self.centre[1]+collectableHalfSize)]
        for i in range(len(points)):
            screen.draw.line((points[i-1][0], points[i-1][1]-screenPosition),
                             (points[i][0], points[i][1]-screenPosition), (32,32,255))
    def update(self):
        self.centre[0] += self.speedX
        if self.centre[0] < collectableHalfSize or self.centre[0] > 800 - collectableHalfSize:
            self.centre[0] -= self.speedX
            self.speedX = 0
        self.speedY += self.accelerationDown
        self.centre[1] += self.speedY
    def checkCollission(self):
        if self.speedY > 1:
            for platform in surfaceLines:
                bottomLine = LineString([(self.centre[0]-collectableHalfSize, self.centre[1]),
                                         (self.centre[0], self.centre[1]+collectableHalfSize),
                                         (self.centre[0]+collectableHalfSize, self.centre[1])])
                intersection = bottomLine.intersection(platform)
                if not intersection.is_empty:
                    point = [self.centre[0], self.centre[1]]
                    if intersection.geom_type == 'MultiPoint':
                        point[1] = min(intersection.geoms, key=lambda x: x.coords[0][1]).coords[0][1] - collectableHalfSize
                    elif intersection.geom_type == 'Point':
                        point[1] = intersection.coords[0][1] - collectableHalfSize
                    return True, point
        return False, [0,0]

class Collectable:
    def __init__(self, startX, startY):
        self.centre = [startX, startY]
        self.creationTime = 0
    def draw(self):
        points = [(self.centre[0]-collectableHalfSize, self.centre[1]),
                  (self.centre[0], self.centre[1]-collectableHalfSize),
                  (self.centre[0]+collectableHalfSize, self.centre[1]),
                  (self.centre[0], self.centre[1]+collectableHalfSize)]
        for i in range(len(points)):
            screen.draw.line((points[i-1][0], points[i-1][1]-screenPosition),
                             (points[i][0], points[i][1]-screenPosition), (128,128,255))
    def update(self):
        self.creationTime += 1

class Collectables:
    def __init__(self):
        self.collectablesFlying = []
        self.collectables = []
    def addCollectable(self, startX, startY):
        self.collectablesFlying.append(CollectableFlying(startX, startY))
    def draw(self):
        for collectable in self.collectablesFlying:
            collectable.draw()
        for collectable in self.collectables:
            collectable.draw()
    def update(self):
        for collectable in self.collectablesFlying:
            collectable.update()
        for collectable in self.collectables:
            collectable.update()
        for i in reversed(range(len(self.collectablesFlying))):
            collission, point = self.collectablesFlying[i].checkCollission()
            if collission:
                self.collectables.append(Collectable(point[0], point[1]))
                del self.collectablesFlying[i]
            elif self.collectablesFlying[i].centre[1] > 600 + collectableHalfSize:
                del self.collectablesFlying[i]
    
allCollectables = Collectables()

def shootCollectable(posX, posY):
    allCollectables.addCollectable(posX, posY)

class Player:
    def __init__(self):
        self.centre = [400, 500]
        self.centredLineString = LineString([(-playerHalfSize,-playerHalfSize*0),
                                             (-playerHalfSize,playerHalfSize),
                                             (playerHalfSize,playerHalfSize),
                                             (playerHalfSize,-playerHalfSize*0)])
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.polygon = Polygon(self.lineString)
        self.speedY = 0
        self.directionX = -1
        self.jumping = False
    def draw(self):
        #print(str(self.centre))
        for i in range(len(self.lineString.coords)):
            screen.draw.line((self.lineString.coords[i-1][0],self.lineString.coords[i-1][1]-screenPosition),
                             (self.lineString.coords[i][0],self.lineString.coords[i][1]-screenPosition), (255,0,0))
    def update(self, platforms):
        if self.speedY >= 0:
            for platform in platforms:
                if not self.jumping:
                    intersection = self.polygon.intersection(platform)
                else:
                    bottomLine = LineString([(self.centre[0]-playerHalfSize, self.centre[1]+playerHalfSize-2),
                                             (self.centre[0]-playerHalfSize, self.centre[1]+playerHalfSize+self.speedY+2),
                                             (self.centre[0]+playerHalfSize, self.centre[1]+playerHalfSize+self.speedY+2),
                                             (self.centre[0]+playerHalfSize, self.centre[1]+playerHalfSize-2)])
                    intersection = bottomLine.intersection(platform)
                if not intersection.is_empty:
                    newPositionY = self.centre[1]
                    if intersection.geom_type == 'MultiPoint':
                        newPositionY = min(intersection.geoms, key=lambda x: x.coords[0][1]).coords[0][1] - playerHalfSize
                    elif intersection.geom_type == 'Point':
                        newPositionY = intersection.coords[0][1] - playerHalfSize
                    elif intersection.geom_type == 'LineString':
                        newPositionY = min(intersection.coords, key=lambda x: x[1])[1] - playerHalfSize
                    if self.centre[1] > newPositionY:
                        self.centre[1] = newPositionY
                    self.speedY = 0
                    self.jumping = False
            if not self.jumping and self.speedY >= coyoteTimeVerticalSpeed:
                self.jumping = True
        if self.centre[1] > 600 - playerHalfSize:
            self.centre[1] = 600 - playerHalfSize
            self.speedY = 0
            self.jumping = False
        else:
            self.speedY += playerAccelerationDown
        if self.speedY > playerTerminalSpeed:
            self.speedY = playerTerminalSpeed
        self.centre[1] += self.speedY
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.polygon = Polygon(self.lineString)
    def jump(self):
        if not self.jumping:
            self.speedY = -playerJumpSpeed
            self.jumping = True
    def left(self):
        self.centre[0] -= playerLateralSpeed
        self.directionX = -1
        if self.centre[0] < playerHalfSize:
            self.centre[0] = playerHalfSize
    def right(self):
        self.centre[0] += playerLateralSpeed
        self.directionX = 1
        if self.centre[0] > 800 - playerHalfSize:
            self.centre[0] = 800 - playerHalfSize

player = Player()

def draw():
    screen.clear()
    for surface in surfaceLines:
        for i in range(1, len(surface.coords)):
            screen.draw.line((surface.coords[i-1][0], surface.coords[i-1][1]-screenPosition),
                             (surface.coords[i][0], surface.coords[i][1]-screenPosition), (255,255,255))
    player.draw()
    allCollectables.draw()

def screenPositionUpdate(player):
    global screenPosition
    if player.centre[1] - screenPosition < 150:
        screenPosition = player.centre[1] - 150
    elif player.centre[1] - screenPosition > 600 - 150:
        screenPosition = player.centre[1] - (600 - 150)
        if screenPosition > 0:
            screenPosition = 0

def update(dt):
    global screenPosition
    if keyboard.left:
        player.left()
    elif keyboard.right:
        player.right()
    if keyboard.up:
        player.jump()
    player.update(surfaceLines)
    allCollectables.update()
    screenPositionUpdate(player)

def on_key_down(key):
    if key == keys.SPACE:
        shootCollectable(player.centre[0], player.centre[1])

pgzrun.go()
