from pgzero.builtins import Actor
from shapely.geometry import LineString
import math

from Listing23_IntersectionRectangles import RectanglesIntersect

rainbowHalfSize = 39
rainbowTimeLife = 200
class Rainbow:
    def __init__(self, centreX, centreY, creationTime):
        self.centre = [centreX, centreY]
        self.timeFromCreation = creationTime
        self.rainbowActor = Actor('rainbow', (centreX, centreY - rainbowHalfSize/2))
        points = []
        for i in range(0, 180+20, 20):
            points.append((self.centre[0] + rainbowHalfSize*math.cos(math.pi*i/180)*0.75, self.centre[1] - rainbowHalfSize*math.sin(math.pi*i/180)))
        self.lineString = LineString(points)
    def draw(self, screenPosition):
        if self.timeFromCreation >= 0:
            self.rainbowActor.y = self.centre[1] - rainbowHalfSize/2 - screenPosition
            self.rainbowActor.draw()
    def update(self, allEnemies, allCollectables):
        if self.timeFromCreation == 0:
            for i in reversed(range(len(allEnemies.enemies))):
                if self.lineString.intersects(allEnemies.enemies[i].lineString):
                    allEnemies.killEnemy(i, allCollectables)
        self.timeFromCreation += 1

rainbowAccelerationDown = 1
class FallingRainbow:
    def __init__(self, centreX, centreY):
        self.centre = [centreX, centreY]
        self.rainbowActor = Actor('falling_rainbow', (centreX, centreY - rainbowHalfSize/2))
        self.speedY = 0
    def draw(self, screenPosition):
        self.rainbowActor.y = self.centre[1] - rainbowHalfSize/2 - screenPosition
        self.rainbowActor.draw()
    def update(self, allEnemies, allRainbows, allCollectables):
        self.speedY += rainbowAccelerationDown
        self.centre[1] += self.speedY
        centerCollision = [self.centre[0], self.centre[1] + self.speedY * 2]
        halfSizeCollision = [rainbowHalfSize, (rainbowHalfSize + self.speedY) / 2]
        for i in reversed(range(len(allEnemies.enemies))):
            if RectanglesIntersect(centerCollision, halfSizeCollision, allEnemies.enemies[i].centre, [allEnemies.enemyHalfSize(), allEnemies.enemyHalfSize()]):
                allEnemies.killEnemy(i, allCollectables)
        for i in reversed(range(len(allRainbows.rainbows))):
            if RectanglesIntersect(centerCollision, halfSizeCollision, allRainbows.rainbows[i].centre, [rainbowHalfSize, rainbowHalfSize/2]):
                allRainbows.rainbowFall(i)

class AllRainbows:
    def __init__(self):
        self.rainbows = []
        self.fallingRainbows = []
    def restart(self):
        self.rainbows = []
        self.fallingRainbows = []
    def draw(self, screenPosition):
        for rainbow in self.rainbows:
            rainbow.draw(screenPosition)
        for fallingRainbow in self.fallingRainbows:
            fallingRainbow.draw(screenPosition)
    def update(self, allEnemies, allCollectables, screenPosition):
        for i in reversed(range(len(self.rainbows))):
            self.rainbows[i].update(allEnemies, allCollectables)
            if self.rainbows[i].timeFromCreation > rainbowTimeLife:
                self.rainbowFall(i)
        for i in reversed(range(len(self.fallingRainbows))):
            self.fallingRainbows[i].update(allEnemies, self, allCollectables)
            if self.fallingRainbows[i].centre[1]-screenPosition-rainbowHalfSize > 600:
                del self.fallingRainbows[i]
    def rainbowFall(self, index):
        self.fallingRainbows.append(FallingRainbow(self.rainbows[index].centre[0], self.rainbows[index].centre[1]))
        del self.rainbows[index]
    def append(self, posX, posY, time):
        self.rainbows.append(Rainbow(posX, posY, time))
    def addRainbows(self, numberOfRainbows, posX, posY, directionX):
        for i in range(numberOfRainbows):
            self.append(posX + directionX * rainbowHalfSize + directionX * i * (rainbowHalfSize-2)*2, posY, -i*10)

