from pgzero.builtins import Actor
from shapely.geometry import LineString, Polygon
from shapely.affinity import translate

from Listing23_IntersectionRectangles import RectanglesIntersect

playerHalfSizeX = 10
playerHalfSizeY = 18
playerAccelerationDown = 0.5
playerJumpSpeed = 14
playerTerminalSpeed = 12
playerLateralSpeed = 4
coyoteTimeVerticalSpeed = 4
playerVerticalSpeedToDestroyRainbow = 5
playerMinTimeBetweenRainbows = 16

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
    def draw(self, screenPosition):
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
    def intersectEnemy(self, allEnemies):
        for enemy in allEnemies.enemies:
            if enemy.active:
                if RectanglesIntersect(self.centre, [playerHalfSizeX, playerHalfSizeY], enemy.centre, [allEnemies.enemyHalfSize(), allEnemies.enemyHalfSize()]):
                    return True
        return False
    def addRainbow(self):
        if self.numberOfRainbows < 3:
            self.numberOfRainbows += 1
    def update(self, allPlatforms, allRainbows, allCollectables, allEnemies):
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
        if self.intersectEnemy(allEnemies):
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
    def playerHalfSize(self):
        return [playerHalfSizeX, playerHalfSizeY]
    def shootRainbow(self, allRainbows):
        if self.lastRainbowShot > playerMinTimeBetweenRainbows:
            self.lastRainbowShot = 0
            allRainbows.addRainbows(self.numberOfRainbows, self.centre[0] + self.directionX * (playerHalfSizeX + 2), self.centre[1] + playerHalfSizeY, self.directionX)

