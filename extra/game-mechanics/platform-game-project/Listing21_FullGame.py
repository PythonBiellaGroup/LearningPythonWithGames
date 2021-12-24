# Player movement prototype program:
# - Cursor left-right: move player
# - Cursor up: player jump
# - Space: shoot a rainbow
import pgzrun
from pygame import image, Color, Surface
from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import translate
from random import randint
import math

from Listing11_PlatformNames import platformNames
from Listing13_PlatformLines import platformLines
from Listing15_Platforms import platforms
from Listing18_EnemyNames import enemyNames
from Listing20_Enemies import enemies

drawLines = False

def RectanglesIntersect(centreA, halfSizeA, centreB, halfSizeB):
    if centreA[0] - halfSizeA[0] < centreB[0] + halfSizeB[0] and centreA[0] + halfSizeA[0] > centreB[0] - halfSizeB[0]:
        if centreA[1] - halfSizeA[1] < centreB[1] + halfSizeB[1] and centreA[1] + halfSizeA[1] > centreB[1] - halfSizeB[1]:
            return True
    return False        

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
        if drawLines:
            for line in self.platformLineStrings:
                for i in range(1, len(line.coords)):
                    screen.draw.line((line.coords[i-1][0], line.coords[i-1][1]-screenPosition),
                                     (line.coords[i][0], line.coords[i][1]-screenPosition), (255,255,255))
    def update(self, newScreenPosition):
        for i in range(len(platforms)):
            self.platformActors[i].x = platforms[i][1]
            self.platformActors[i].y = platforms[i][2] - screenPosition

allPlatforms = AllPlatforms()

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
    def draw(self):
        if self.timeFromCreation >= 0:
            self.rainbowActor.y = self.centre[1] - rainbowHalfSize/2 - screenPosition
            self.rainbowActor.draw()
            if drawLines:
                for i in range(1, len(self.lineString.coords)):
                    screen.draw.line((self.lineString.coords[i-1][0], self.lineString.coords[i-1][1]-screenPosition),
                                     (self.lineString.coords[i][0], self.lineString.coords[i][1]-screenPosition), (255,255,255))
    def update(self):
        if self.timeFromCreation == 0:
            for i in reversed(range(len(allEnemies.enemies))):
                enemyLine = LineString([(allEnemies.enemies[i].centre[0] - enemyHalfSize, allEnemies.enemies[i].centre[1] - enemyHalfSize),
                                        (allEnemies.enemies[i].centre[0] - enemyHalfSize, allEnemies.enemies[i].centre[1] + enemyHalfSize),
                                        (allEnemies.enemies[i].centre[0] + enemyHalfSize, allEnemies.enemies[i].centre[1] + enemyHalfSize),
                                        (allEnemies.enemies[i].centre[0] + enemyHalfSize, allEnemies.enemies[i].centre[1] - enemyHalfSize)])
                if self.lineString.intersects(enemyLine):
                    allEnemies.killEnemy(i)
        self.timeFromCreation += 1

rainbowAccelerationDown = 1
class FallingRainbow:
    def __init__(self, centreX, centreY):
        self.centre = [centreX, centreY]
        self.rainbowActor = Actor('falling_rainbow', (centreX, centreY - rainbowHalfSize/2))
        self.speedY = 0
    def draw(self):
        self.rainbowActor.y = self.centre[1] - rainbowHalfSize/2 - screenPosition
        self.rainbowActor.draw()
        if drawLines:
            screen.draw.line((self.centre[0] - rainbowHalfSize, self.centre[1] - screenPosition - rainbowHalfSize//2),
                             (self.centre[0] + rainbowHalfSize, self.centre[1] - screenPosition - rainbowHalfSize//2), (255,255,255))
            screen.draw.line((self.centre[0] + rainbowHalfSize, self.centre[1] - screenPosition - rainbowHalfSize//2),
                             (self.centre[0] + rainbowHalfSize, self.centre[1] - screenPosition + rainbowHalfSize + self.speedY), (255,255,255))
            screen.draw.line((self.centre[0] + rainbowHalfSize, self.centre[1] - screenPosition + rainbowHalfSize + self.speedY),
                             (self.centre[0] - rainbowHalfSize, self.centre[1] - screenPosition + rainbowHalfSize + self.speedY), (255,255,255))
            screen.draw.line((self.centre[0] - rainbowHalfSize, self.centre[1] - screenPosition + rainbowHalfSize + self.speedY),
                             (self.centre[0] - rainbowHalfSize, self.centre[1] - screenPosition - rainbowHalfSize//2), (255,255,255))
    def update(self):
        self.speedY += rainbowAccelerationDown
        self.centre[1] += self.speedY
        centerCollision = [self.centre[0], self.centre[1] + self.speedY * 2]
        halfSizeCollision = [rainbowHalfSize, (rainbowHalfSize + self.speedY) / 2]
        for i in reversed(range(len(allEnemies.enemies))):
            if RectanglesIntersect(centerCollision, halfSizeCollision, allEnemies.enemies[i].centre, [enemyHalfSize, enemyHalfSize]):
                allEnemies.killEnemy(i)
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
    def append(self, posX, posY, time):
        self.rainbows.append(Rainbow(posX, posY, time))
        
    
allRainbows = AllRainbows()

playerHalfSizeX = 10
playerHalfSizeY = 18
playerAccelerationDown = 0.5
playerJumpSpeed = 14
playerTerminalSpeed = 12
playerLateralSpeed = 4
coyoteTimeVerticalSpeed = 4
playerVerticalSpeedToDestroyRainbow = 5
playerMinTimeBetweenRainbows = 16

screenPosition = 0

playerImageNames = ['player_stand_right', 'player_walk_1_right', 'player_stand_right', 'player_walk_2_right', 'player_jump_up_right', 'player_jump_down_right',
                    'player_stand_left', 'player_walk_1_left', 'player_stand_left', 'player_walk_2_left', 'player_jump_up_left', 'player_jump_down_left',
                    'player_collided_1', 'player_collided_2']
class Player:
    def __init__(self):
        self.centre = [400, 500]
        self.centredLineString = LineString([(-playerHalfSizeX,-playerHalfSizeY*0),
                                             (-playerHalfSizeX,playerHalfSizeY),
                                             (playerHalfSizeX,playerHalfSizeY),
                                             (playerHalfSizeX,-playerHalfSizeY*0)])
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.polygon = Polygon(self.lineString)
        self.speedY = 0
        self.walking = False
        self.directionX = -1
        self.jumping = False
        self.actors = [Actor(name) for name in playerImageNames]
        self.numberOfRainbows = 1
        self.lastRainbowShot = playerMinTimeBetweenRainbows
        self.active = True
        self.lives = 3
    def draw(self):
        indexImage = 0
        if self.active:
            if self.jumping:
                if self.speedY < 0:
                    indexImage = 4
                else:
                    indexImage = 5
            elif self.walking:
                indexImage = (self.centre[0]//13) % 4
            if self.directionX < 0:
                indexImage += 6
        else:
            indexImage = 12 + (self.centre[0]//13) % 2
        self.actors[indexImage].x = self.centre[0]
        self.actors[indexImage].y = self.centre[1] - screenPosition
        self.actors[indexImage].draw()
        if drawLines:
            for i in range(len(self.lineString.coords)):
                screen.draw.line((self.lineString.coords[i-1][0],self.lineString.coords[i-1][1]-screenPosition),
                                 (self.lineString.coords[i][0],self.lineString.coords[i][1]-screenPosition), (255,0,0))
    def intersectPlatform(self, platform, collidingObject):
        intersection = collidingObject.intersection(platform)
        if not intersection.is_empty:
            newPositionY = self.centre[1]
            if intersection.geom_type == 'MultiPoint':
                newPositionY = min(intersection.geoms, key=lambda x: x.coords[0][1]).coords[0][1] - playerHalfSizeY
            elif intersection.geom_type == 'Point':
                newPositionY = intersection.coords[0][1] - playerHalfSizeY
            elif intersection.geom_type == 'LineString':
                newPositionY = min(intersection.coords, key=lambda x: x[1])[1] - playerHalfSizeY
            if self.centre[1] > newPositionY:
                self.centre[1] = newPositionY
            self.speedY = 0
            self.jumping = False
            return True
        return False
    def intersectEnemy(self, enemies):
        for enemy in enemies:
            if enemy.active:
                if RectanglesIntersect(self.centre, [playerHalfSizeX, playerHalfSizeY], enemy.centre, [enemyHalfSize, enemyHalfSize]):
                    return True
        return False
    def addRainbow(self):
        if self.numberOfRainbows < 3:
            self.numberOfRainbows += 1
    def update(self):
        if self.lives == 0:
            return
        if not self.active:
            self.speedY += playerAccelerationDown
            self.centre[0] += self.speedX // 2
            self.centre[1] += self.speedY // 2
            if self.centre[1] > 600 + playerHalfSizeY*6:
                self.lives -= 1
                if self.lives > 0:
                    self.centre = [400, 500]
                    self.speedX = 0
                    self.speedY = 0
                    self.numberOfRainbows = 1
                    self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
                    self.polygon = Polygon(self.lineString)
                    allRainbows.restart()
                    allCollectables.restart()
                    allEnemies.restart()
                    self.active = True
            return
        if self.speedY >= 0:
            if not self.jumping:
                collidingObject = self.polygon
            else:
                collidingObject = LineString([(self.centre[0]-playerHalfSizeX, self.centre[1]+playerHalfSizeY-2),
                                              (self.centre[0]-playerHalfSizeX, self.centre[1]+playerHalfSizeY+self.speedY+2),
                                              (self.centre[0]+playerHalfSizeX, self.centre[1]+playerHalfSizeY+self.speedY+2),
                                              (self.centre[0]+playerHalfSizeX, self.centre[1]+playerHalfSizeY-2)])
            for platform in allPlatforms.platformLineStrings:
                self.intersectPlatform(platform, collidingObject)
            previousSpeed = self.speedY
            for i in reversed(range(len(allRainbows.rainbows))):
                if allRainbows.rainbows[i].timeFromCreation >= 0:
                    if self.intersectPlatform(allRainbows.rainbows[i].lineString, collidingObject):
                        if previousSpeed >= playerVerticalSpeedToDestroyRainbow:
                            allRainbows.rainbowFall(i)
            if not self.jumping and self.speedY >= coyoteTimeVerticalSpeed:
                self.jumping = True
        if self.centre[1] > 600 - playerHalfSizeY:
            self.centre[1] = 600 - playerHalfSizeY
            self.speedY = 0
            self.jumping = False
        else:
            self.speedY += playerAccelerationDown
        if self.speedY > playerTerminalSpeed:
            self.speedY = playerTerminalSpeed
        self.centre[1] += self.speedY
        if self.intersectEnemy(allEnemies.enemies):
            self.active = False
            self.speedY = -playerJumpSpeed
            if self.centre[0] > 400:
                self.speedX = -playerLateralSpeed
            else:
                self.speedX = playerLateralSpeed
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.polygon = Polygon(self.lineString)
        self.lastRainbowShot += 1
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
        if self.centre[0] < playerHalfSizeX:
            self.centre[0] = playerHalfSizeX
        self.walking = True
    def right(self):
        self.centre[0] += playerLateralSpeed
        self.directionX = 1
        if self.centre[0] > 800 - playerHalfSizeX:
            self.centre[0] = 800 - playerHalfSizeX
        self.walking = True
    def still(self):
        self.walking = False
    def shootRainbow(self):
        if self.lastRainbowShot > playerMinTimeBetweenRainbows:
            self.lastRainbowShot = 0
            for i in range(self.numberOfRainbows):
                allRainbows.append(self.centre[0] + self.directionX * ((rainbowHalfSize + playerHalfSizeX + 2) + i * (rainbowHalfSize-2)*2), self.centre[1] + playerHalfSizeY, -i*10)

player = Player()

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
    def draw(self):
        if self.active and self.centre[1] - screenPosition > -enemyHalfSize and self.centre[1] - screenPosition < 600+enemyHalfSize:
            indexActor = ((self.centre[0]//6) % (len(enemyNames[self.index])//2))*2
            if self.speedX < 0:
                indexActor += 1
            self.actors[indexActor].x = self.centre[0]
            self.actors[indexActor].y = self.centre[1] - screenPosition
            self.actors[indexActor].draw()
            if drawLines:
                for i in range(len(self.lineString.coords)):
                    screen.draw.line((self.lineString.coords[i-1][0], self.lineString.coords[i-1][1] - screenPosition),
                                     (self.lineString.coords[i][0], self.lineString.coords[i][1] - screenPosition), (255,0,0))
    def update(self):
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
    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
    def update(self):
        for enemy in self.enemies:
            enemy.update()
    def killEnemy(self, index):
        allCollectables.addCollectable(self.enemies[index].centre[0], self.enemies[index].centre[1])
        del self.enemies[index]

allEnemies = AllEnemies()


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
    def draw(self):
        index = (self.indexActor // 4) % len(flyingCollectableNames)
        self.actors[index].x = self.centre[0]
        self.actors[index].y = self.centre[1] - screenPosition
        self.actors[index].draw()
        if drawLines:
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
        self.indexActor += 1
    def checkCollission(self):
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
    def draw(self):
        self.actor.y = self.centre[1] - screenPosition
        self.actor.draw()
        if drawLines:
            points = [(self.centre[0]-collectableHalfSize, self.centre[1]),
                      (self.centre[0], self.centre[1]-collectableHalfSize),
                      (self.centre[0]+collectableHalfSize, self.centre[1]),
                      (self.centre[0], self.centre[1]+collectableHalfSize)]
            for i in range(len(points)):
                screen.draw.line((points[i-1][0], points[i-1][1]-screenPosition),
                                 (points[i][0], points[i][1]-screenPosition), (128,128,255))
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
        for i in reversed(range(len(self.collectables))):
            if RectanglesIntersect(player.centre, [playerHalfSizeX, playerHalfSizeY], self.collectables[i].centre, [collectableHalfSize, collectableHalfSize]):
                if self.collectables[i].isRainbow():
                    player.addRainbow()
                self.removeCollectable(i)
    def removeCollectable(self, index):
        del self.collectables[index]
    
allCollectables = Collectables()


backgroundBaseColour = (95, 148, 255)
backgroundColour = (0,0,0)

maxScreenPosition = -platforms[-1][2]

levelClear = False

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
    allEnemies.draw()
    allRainbows.draw()
    allCollectables.draw()
    player.draw()
    for i in range(player.lives):
        screen.blit('player_icon', (10+i*14, 10))
    if player.lives == 0:
        screen.draw.text("GAME OVER", center=(400, 260), fontsize=55, color=(255,0,0))
    if levelClear:
        screen.draw.text("LEVEL CLEAR", center=(400, 260), fontsize=55, color=(0,0,255))
        

def screenPositionUpdate(player):
    global screenPosition
    if player.centre[1] - screenPosition < 150:
        screenPosition = player.centre[1] - 150
    elif player.centre[1] - screenPosition > 600 - 150:
        screenPosition = player.centre[1] - (600 - 150)
        if screenPosition > 0:
            screenPosition = 0

def update(dt):
    global screenPosition, backgroundColour, levelClear
    if keyboard.left:
        player.left()
    elif keyboard.right:
        player.right()
    else:
        player.still()
    if keyboard.up:
        player.jump()
    else:
        player.stopJump()
    player.update()
    screenPositionUpdate(player)
    backgroundColour = backgroundColourUpdate(backgroundBaseColour, screenPosition)
    allRainbows.update()
    allEnemies.update()
    allCollectables.update()
    allPlatforms.update(screenPosition)
    if player.centre[1] < -maxScreenPosition - maxHeightPlatform/2:
        levelClear = True

def on_key_down(key):
    if key == keys.SPACE:
        player.shootRainbow()

pgzrun.go()
