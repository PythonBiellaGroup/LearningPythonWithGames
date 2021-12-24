# Player movement prototype program:
# - Cursor left-right: move player
# - Cursor up: player jump
# - Space: shoot a rainbow
import pgzrun
from pygame import image, Color, Surface
from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import translate
import math

from Listing11_PlatformNames import platformNames
from Listing13_PlatformLines import platformLines
from Listing15_Platforms import platforms

maxHeightPlatform = 124
class AllPlatforms():
    def __init__(self):
        self.platformActors = [Actor(platformNames[platforms[i][0]], (platforms[i][1], platforms[i][2])) for i in range(len(platforms))]
        self.platformLineStrings = []
        for i in range(len(platforms)):
            points = [(platformLines[platforms[i][0]][j][0] + platforms[i][1],
                       platformLines[platforms[i][0]][j][1] + platforms[i][2])
                      for j in range(len(platformLines[platforms[i][0]]))]
            self.platformLineStrings.append(LineString(points))
    def draw(self):
        for platform in self.platformActors:
            if platform.y > -maxHeightPlatform/2 and platform.y < 600+maxHeightPlatform/2:
                platform.draw()
        for line in self.platformLineStrings:
            for i in range(1, len(line.coords)):
                screen.draw.line((line.coords[i-1][0], line.coords[i-1][1]-screenPosition),
                                 (line.coords[i][0], line.coords[i][1]-screenPosition), (128,128,255))
    def update(self, newScreenPosition):
        for i in range(len(platforms)):
            self.platformActors[i].x = platforms[i][1]
            self.platformActors[i].y = platforms[i][2] - screenPosition

allPlatforms = AllPlatforms()

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
playerJumpSpeed = 14
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
            for platform in allPlatforms.platformLineStrings:
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

backgroundBaseColour = (95, 148, 255)
backgroundColour = (0,0,0)

maxScreenPosition = -platforms[-1][2]

def backgroundColourUpdate(backgroundBaseColour, screenPosition):
    colourScale = -screenPosition / maxScreenPosition
    if colourScale > 1:
        colourScale = 1
    return (backgroundBaseColour[0]*colourScale,
            backgroundBaseColour[1]*colourScale,
            backgroundBaseColour[2]*colourScale)

def draw():
    screen.fill(backgroundColour)
    allPlatforms.draw()
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
    global screenPosition, backgroundColour
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
    backgroundColour = backgroundColourUpdate(backgroundBaseColour, screenPosition)
    allRainbows.update()
    allPlatforms.update(screenPosition)

def on_key_down(key):
    if key == keys.SPACE:
        player.shootRainbow()

pgzrun.go()
