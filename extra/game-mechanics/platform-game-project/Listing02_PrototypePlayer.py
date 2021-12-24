# Player movement prototype program:
# - Cursor left-right: move player
# - Cursor up: player jump
import pgzrun
from pygame import image, Color, Surface
from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import translate

surfaces = [[(0, 561), (88, 556), (237, 543), (407, 548), (575, 561), (739, 557), (799, 555)],
            [(61, 452), (174, 446), (294, 446), (379, 445)],
            [(554, 446), (707, 443)],
            [(275, 336), (418, 332), (520, 332), (624, 327)],
            [(56, 241), (171, 233), (294, 236), (365, 236)],
            [(474, 228), (622, 219), (760, 224)],
            [(335, 167), (435, 166), (499, 151), (570, 105), (605, 61), (635, 61)],
            [(37, 180), (122, 179)],
            [(112, 180), (120, 144), (136, 116), (158, 104), (183, 103), (201, 109), (216, 129), (226, 172)]]
surfaceLines = [LineString(surfaces[i]) for i in range(len(surfaces))]

playerHalfSize = 15
playerAccelerationDown = 0.5
playerJumpSpeed = 12
playerTerminalSpeed = 12
playerLateralSpeed = 4

class Player:
    def __init__(self):
        self.centre = [400, 100]
        self.centredLineString = LineString([(-playerHalfSize,-playerHalfSize),
                                             (-playerHalfSize,playerHalfSize),
                                             (playerHalfSize,playerHalfSize),
                                             (playerHalfSize,-playerHalfSize)])
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.speedY = 0
        self.jumping = False
    def draw(self):
        for i in range(len(self.lineString.coords)):
            screen.draw.line(self.lineString.coords[i-1], self.lineString.coords[i], (255,0,0))
    def update(self, platforms):
        if self.speedY >= 0:
            boundingBox = LineString([(self.centre[0]-playerHalfSize, self.centre[1]-playerHalfSize),
                                      (self.centre[0]-playerHalfSize, self.centre[1]+playerHalfSize+self.speedY+2),
                                      (self.centre[0]+playerHalfSize, self.centre[1]+playerHalfSize+self.speedY+2),
                                      (self.centre[0]+playerHalfSize, self.centre[1]-playerHalfSize)])
            for platform in platforms:
                intersection = boundingBox.intersection(platform)
                if not intersection.is_empty:
                    if intersection.geom_type == 'MultiPoint':
                        self.centre[1] = min(intersection.geoms, key=lambda x: x.coords[0][1]).coords[0][1] - playerHalfSize
                    elif intersection.geom_type == 'Point':
                        self.centre[1] = intersection.coords[0][1] - playerHalfSize
                    self.speedY = 0
                    self.jumping = False
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
    def jump(self):
        if not self.jumping:
            self.speedY = -playerJumpSpeed
            self.jumping = True
    def left(self):
        self.centre[0] -= playerLateralSpeed
        if self.centre[0] < playerHalfSize:
            self.centre[0] = playerHalfSize
    def right(self):
        self.centre[0] += playerLateralSpeed
        if self.centre[0] > 800 - playerHalfSize:
            self.centre[0] = 800 - playerHalfSize

player = Player()

def draw():
    screen.clear()
    for surface in surfaces:
        for i in range(1, len(surface)):
            screen.draw.line(surface[i-1], surface[i], (255,255,255))
    player.draw()

def update(dt):
    if keyboard.left:
        player.left()
    elif keyboard.right:
        player.right()
    if keyboard.up:
        player.jump()
    player.update(surfaceLines)

pgzrun.go()
