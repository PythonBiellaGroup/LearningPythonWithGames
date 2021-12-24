from pgzero.builtins import Actor
from shapely.geometry import LineString
from random import randint

from Listing23_IntersectionRectangles import RectanglesIntersect

collectableNames = ['collectable_1', 'collectable_2', 'collectable_3', 'collectable_4', 'collectable_5', 'collectable_rainbow']
flyingCollectableNames = ['flying_candy_1', 'flying_candy_2', 'flying_candy_3', 'flying_candy_4']

collectableHalfSize = 10

class CollectableFlying:
    def __init__(self, startX, startY):
        self.centre = [startX, startY]
        self.speedX = randint(-startX,800-startX)/100
        self.speedY = randint(-6,-4)
        self.accelerationDown = 0.1
        self.actors = [Actor(name, (startX, startY)) for name in flyingCollectableNames]
        self.indexActor = 0
    def draw(self, screenPosition):
        index = (self.indexActor // 4) % len(flyingCollectableNames)
        self.actors[index].x = self.centre[0]
        self.actors[index].y = self.centre[1] - screenPosition
        self.actors[index].draw()
    def update(self, screenPosition):
        self.centre[0] += self.speedX
        if self.centre[0] < collectableHalfSize or self.centre[0] > 800 - collectableHalfSize:
            self.centre[0] -= self.speedX
            self.speedX = 0
        self.speedY += self.accelerationDown
        self.centre[1] += self.speedY
        self.indexActor += 1
    def checkCollission(self, allPlatforms):
        if self.speedY > 1:
            bottomLine = LineString([(self.centre[0]-collectableHalfSize, self.centre[1]),
                                     (self.centre[0], self.centre[1]+collectableHalfSize),
                                     (self.centre[0]+collectableHalfSize, self.centre[1])])
            for platform in allPlatforms.platformLineStrings:
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
        self.actor = Actor(collectableNames[randint(0, 5)], (startX, startY))
    def draw(self, screenPosition):
        self.actor.y = self.centre[1] - screenPosition
        self.actor.draw()
    def update(self):
        self.creationTime += 1
    def isRainbow(self):
        if self.actor.image == 'collectable_rainbow':
            return True
        return False

class Collectables:
    def __init__(self):
        self.collectablesFlying = []
        self.collectables = []
    def restart(self):
        self.collectablesFlying = []
        self.collectables = []
    def addCollectable(self, startX, startY):
        self.collectablesFlying.append(CollectableFlying(startX, startY))
    def draw(self, screenPosition):
        for collectable in self.collectablesFlying:
            collectable.draw(screenPosition)
        for collectable in self.collectables:
            collectable.draw(screenPosition)
    def update(self, allPlatforms, player, screenPosition):
        for collectable in self.collectablesFlying:
            collectable.update(screenPosition)
        for collectable in self.collectables:
            collectable.update()
        for i in reversed(range(len(self.collectablesFlying))):
            collission, point = self.collectablesFlying[i].checkCollission(allPlatforms)
            if collission:
                self.collectables.append(Collectable(point[0], point[1]))
                del self.collectablesFlying[i]
            elif self.collectablesFlying[i].centre[1] > 600 + collectableHalfSize:
                del self.collectablesFlying[i]
        for i in reversed(range(len(self.collectables))):
            if RectanglesIntersect(player.centre, player.playerHalfSize(), self.collectables[i].centre, [collectableHalfSize, collectableHalfSize]):
                if self.collectables[i].isRainbow():
                    player.addRainbow()
                self.removeCollectable(i)
    def removeCollectable(self, index):
        del self.collectables[index]

