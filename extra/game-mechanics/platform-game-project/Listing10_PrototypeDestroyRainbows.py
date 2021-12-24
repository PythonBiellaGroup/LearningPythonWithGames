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
rainbowTimeLife = 200
class Rainbow:
    def __init__(self, centreX, centreY):
        self.centre = [centreX, centreY]
        self.timeFromCreation = 0
        points = []
        for i in range(0, 180+20, 20):
            points.append((self.centre[0] + rainbowHalfSize*math.cos(math.pi*i/180)/2, self.centre[1] - rainbowHalfSize*math.sin(math.pi*i/180)))
        self.lineString = LineString(points)
    def draw(self):
        for i in range(1, len(self.lineString.coords)):
            screen.draw.line((self.lineString.coords[i-1][0], self.lineString.coords[i-1][1]-screenPosition),
                             (self.lineString.coords[i][0], self.lineString.coords[i][1]-screenPosition), (255,255,255))
    def update(self):
        self.timeFromCreation += 1

rainbowAccelerationDown = 1
class FallingRainbow:
    def __init__(self, centreX, centreY):
        self.centre = [centreX, centreY]
        self.speedY = 0
        points = []
        for i in range(0, 180+20, 20):
            points.append((self.centre[0] + rainbowHalfSize*math.cos(math.pi*i/180), self.centre[1] - rainbowHalfSize*math.sin(math.pi*i/180)))
        self.lineString = LineString(points)
    def draw(self):
        for i in range(1, len(self.lineString.coords)):
            screen.draw.line((self.lineString.coords[i-1][0], self.lineString.coords[i-1][1]-screenPosition),
                             (self.lineString.coords[i][0], self.lineString.coords[i][1]-screenPosition), (255,255,255))
    def update(self):
        self.speedY += rainbowAccelerationDown
        self.centre[1] += self.speedY
        points = []
        for i in range(0, 180+20, 20):
            points.append((self.centre[0] + rainbowHalfSize*math.cos(math.pi*i/180), self.centre[1] - rainbowHalfSize*math.sin(math.pi*i/180)))
        self.lineString = LineString(points)

class AllRainbows:
    def __init__(self):
        self.rainbows = []
        self.fallingRainbows = []
    def draw(self):
        for rainbow in self.rainbows:
            rainbow.draw()
        for fallingRainbow in self.fallingRainbows:
            fallingRainbow.draw()
    def update(self):
        for i in reversed(range(len(self.rainbows))):
            self.rainbows[i].update()
            if self.rainbows[i].timeFromCreation > rainbowTimeLife:
                self.rainbowFall(i)
        for i in reversed(range(len(self.fallingRainbows))):
            self.fallingRainbows[i].update()
            if self.fallingRainbows[i].centre[1]-screenPosition-rainbowHalfSize > 600:
                del self.fallingRainbows[i]
    def rainbowFall(self, index):
        self.fallingRainbows.append(FallingRainbow(self.rainbows[index].centre[0], self.rainbows[index].centre[1]))
        del self.rainbows[index]
    def append(self, posX, posY):
        self.rainbows.append(Rainbow(posX, posY))
        
    
allRainbows = AllRainbows()

playerHalfSize = 15
playerAccelerationDown = 0.5
playerJumpSpeed = 12
playerTerminalSpeed = 12
playerLateralSpeed = 4
coyoteTimeVerticalSpeed = 4
playerVerticalSpeedToDestroyRainbow = 2

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
    def intersectPlatform(self, platform, collidingObject):
        intersection = collidingObject.intersection(platform)
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
            return True
        return False
    def update(self):
        if self.speedY >= 0:
            if not self.jumping:
                collidingObject = self.polygon
            else:
                collidingObject = LineString([(self.centre[0]-playerHalfSize, self.centre[1]+playerHalfSize-2),
                                              (self.centre[0]-playerHalfSize, self.centre[1]+playerHalfSize+self.speedY+2),
                                              (self.centre[0]+playerHalfSize, self.centre[1]+playerHalfSize+self.speedY+2),
                                              (self.centre[0]+playerHalfSize, self.centre[1]+playerHalfSize-2)])
            for platform in surfaceLines:
                self.intersectPlatform(platform, collidingObject)
            previousSpeed = self.speedY
            for i in reversed(range(len(allRainbows.rainbows))):
                if self.intersectPlatform(allRainbows.rainbows[i].lineString, collidingObject):
                    if previousSpeed >= playerVerticalSpeedToDestroyRainbow:
                        allRainbows.rainbowFall(i)
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
    def stopJump(self):
        if self.jumping and self.speedY < -playerJumpSpeed/2:
            self.speedY = -playerJumpSpeed/2
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
        allRainbows.append(self.centre[0] + self.directionX * (rainbowHalfSize + playerHalfSize + 2), self.centre[1] + playerHalfSize)

player = Player()

def draw():
    screen.clear()
    for surface in surfaceLines:
        for i in range(1, len(surface.coords)):
            screen.draw.line((surface.coords[i-1][0], surface.coords[i-1][1]-screenPosition),
                             (surface.coords[i][0], surface.coords[i][1]-screenPosition), (255,255,255))
    player.draw()
    allRainbows.draw()

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
    else:
        player.stopJump()
    player.update()
    screenPositionUpdate(player)
    allRainbows.update()

def on_key_down(key):
    if key == keys.SPACE:
        player.shootRainbow()

pgzrun.go()
