# Player movement prototype program:
# - Cursor left-right: move player
# - Cursor up: player jump
# - Space: shoot a rainbow
import pgzrun
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

rainbowHalfSize = 39
class Rainbow:
    def __init__(self, centreX, centreY):
        self.centre = [centreX, centreY]
        self.timeFromCreation = 0
        points = []
        for i in range(0, 180+20, 20):
            points.append((self.centre[0] + rainbowHalfSize*math.cos(math.pi*i/180)/2, self.centre[1] - rainbowHalfSize*math.sin(math.pi*i/180)))
        surfaceLines.append(LineString(points))
    def draw(self):
        pass
    def update(self):
        self.timeFromCreation += 1
    
rainbows = []

playerHalfSize = 15
playerAccelerationDown = 0.5
playerJumpSpeed = 12
playerTerminalSpeed = 12
playerLateralSpeed = 4
coyoteTimeVerticalSpeed = 4

screenPosition = 0

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
                    #break
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
    def shootRainbow(self):
        rainbows.append(Rainbow(self.centre[0] + self.directionX * (rainbowHalfSize + playerHalfSize + 2), self.centre[1] + playerHalfSize))

player = Player()

def draw():
    screen.clear()
    for surface in surfaceLines:
        for i in range(1, len(surface.coords)):
            screen.draw.line((surface.coords[i-1][0], surface.coords[i-1][1]-screenPosition),
                             (surface.coords[i][0], surface.coords[i][1]-screenPosition), (255,255,255))
    player.draw()
    for rainbow in rainbows:
        rainbow.draw()

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
    screenPositionUpdate(player)
    for rainbow in rainbows:
        rainbow.update()

def on_key_down(key):
    if key == keys.SPACE:
        player.shootRainbow()

pgzrun.go()
