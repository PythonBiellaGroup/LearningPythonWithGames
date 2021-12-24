from pgzero.builtins import Actor
from shapely.geometry import LineString
from shapely.affinity import translate

from Listing18_EnemyNames import enemyNames
from Listing20_Enemies import enemies

enemyHalfSize = 12
enemyAccelerationDown = 0.5
enemyTerminalSpeed = 8
enemyLateralSpeed = 2
enemyFlyingVerticalSpeed = 1

class Enemy:
    def __init__(self, centreX, centreY, indexEnemy, directionX):
        self.centre = [centreX, centreY]
        self.centredLineString = LineString([(-enemyHalfSize,-enemyHalfSize),
                                             (-enemyHalfSize,enemyHalfSize),
                                             (enemyHalfSize,enemyHalfSize),
                                             (enemyHalfSize,-enemyHalfSize)])
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.speedX = directionX * enemyLateralSpeed
        self.speedY = 0
        if indexEnemy == 2:
            self.speedY = enemyFlyingVerticalSpeed
        self.index = indexEnemy
        self.actors = [Actor(name) for name in enemyNames[indexEnemy]]
        self.active = False
    def draw(self, screenPosition):
        if self.active and self.centre[1] - screenPosition > -enemyHalfSize and self.centre[1] - screenPosition < 600+enemyHalfSize:
            indexActor = ((self.centre[0]//6) % (len(enemyNames[self.index])//2))*2
            if self.speedX < 0:
                indexActor += 1
            self.actors[indexActor].x = self.centre[0]
            self.actors[indexActor].y = self.centre[1] - screenPosition
            self.actors[indexActor].draw()
    def update(self, allPlatforms, allRainbows, screenPosition):
        if self.centre[1] - screenPosition > -enemyHalfSize/2:
            self.active = True
        if not self.active or self.centre[1] - screenPosition > 600+enemyHalfSize:
            return
        if self.index == 0:
            if self.speedX > 0:
                lineIntersection = LineString([(self.centre[0]+enemyHalfSize, self.centre[1]-6),
                                               (self.centre[0]+enemyHalfSize, self.centre[1]+enemyHalfSize+16)])
            else:
                lineIntersection = LineString([(self.centre[0]-enemyHalfSize, self.centre[1]-6),
                                               (self.centre[0]-enemyHalfSize, self.centre[1]+enemyHalfSize+16)])
        else:
            lineIntersection = LineString([(self.centre[0]-enemyHalfSize, self.centre[1]-enemyHalfSize),
                                           (self.centre[0]-enemyHalfSize, self.centre[1]+enemyHalfSize+self.speedY+2),
                                           (self.centre[0]+enemyHalfSize, self.centre[1]+enemyHalfSize+self.speedY+2),
                                           (self.centre[0]+enemyHalfSize, self.centre[1]-enemyHalfSize)])
        intersectionFound = False
        for platform in allPlatforms.platformLineStrings:
            intersection = lineIntersection.intersection(platform)
            if not intersection.is_empty:
                if self.index != 2:
                    if intersection.geom_type == 'MultiPoint':
                        self.centre[1] = min(intersection.geoms, key=lambda x: x.coords[0][1]).coords[0][1] - enemyHalfSize
                    elif intersection.geom_type == 'Point':
                        self.centre[1] = intersection.coords[0][1] - enemyHalfSize
                intersectionFound = True
                if self.index != 2:
                    self.speedY = 0
        for rainbow in allRainbows.rainbows:
            intersection = lineIntersection.intersection(rainbow.lineString)
            if not intersection.is_empty:
                if self.index == 0 or self.index == 2:
                    self.speedX = -self.speedX
                elif self.index == 1 and self.speedY < 1:
                    self.speedX = -self.speedX
                else:
                    if intersection.geom_type == 'MultiPoint':
                        self.centre[1] = min(intersection.geoms, key=lambda x: x.coords[0][1]).coords[0][1] - enemyHalfSize
                    elif intersection.geom_type == 'Point':
                        self.centre[1] = intersection.coords[0][1] - enemyHalfSize
        if not intersectionFound and self.index == 0:
            self.speedX = -self.speedX
        elif intersectionFound and self.index == 2:
            self.speedY = -self.speedY
        elif self.centre[0] >= 800 - enemyHalfSize:
            self.speedX = -enemyLateralSpeed
        elif self.centre[0] <= enemyHalfSize:
            self.speedX = enemyLateralSpeed
        if self.centre[1] > 600 - enemyHalfSize:
            self.centre[1] = 600 - enemyHalfSize
            if self.index != 2:
                self.speedY = 0
        elif self.index == 1:
            self.speedY += enemyAccelerationDown
            if self.speedY > enemyTerminalSpeed:
                self.speedY = enemyTerminalSpeed
        self.centre[0] += self.speedX
        self.centre[1] += self.speedY
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])

class AllEnemies:
    def __init__(self):
        self.restart()
    def restart(self):
        self.enemies = [Enemy(enemies[i][2], enemies[i][3], enemies[i][0], enemies[i][1]) for i in range(len(enemies))]
    def draw(self, screenPosition):
        for enemy in self.enemies:
            enemy.draw(screenPosition)
    def update(self, allPlatforms, allRainbows, screenPosition):
        for enemy in self.enemies:
            enemy.update(allPlatforms, allRainbows, screenPosition)
    def killEnemy(self, index, allCollectables):
        allCollectables.addCollectable(self.enemies[index].centre[0], self.enemies[index].centre[1])
        del self.enemies[index]
    def enemyHalfSize(self):
        return enemyHalfSize

