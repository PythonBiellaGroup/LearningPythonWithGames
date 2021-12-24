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
            [(37, 180), (122, 179)]]
surfaceLines = [LineString(surfaces[i]) for i in range(len(surfaces))]

enemyHalfSize = 12
enemyAccelerationDown = 0.5
enemyTerminalSpeed = 8
enemyLateralSpeed = 3

class Enemy:
    def __init__(self, centreX, centreY):
        self.centre = [centreX, centreY]
        self.centredLineString = LineString([(-enemyHalfSize,-enemyHalfSize),
                                             (-enemyHalfSize,enemyHalfSize),
                                             (enemyHalfSize,enemyHalfSize),
                                             (enemyHalfSize,-enemyHalfSize)])
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.speedX = enemyLateralSpeed
        self.speedY = 0
    def draw(self):
        for i in range(len(self.lineString.coords)):
            screen.draw.line(self.lineString.coords[i-1], self.lineString.coords[i], (255,0,0))
    def update(self, platforms):
        if self.speedY >= 0:
            bottomLine = LineString([(self.centre[0]-enemyHalfSize, self.centre[1]-enemyHalfSize),
                                     (self.centre[0]-enemyHalfSize, self.centre[1]+enemyHalfSize+self.speedY+2),
                                     (self.centre[0]+enemyHalfSize, self.centre[1]+enemyHalfSize+self.speedY+2),
                                     (self.centre[0]+enemyHalfSize, self.centre[1]-enemyHalfSize)])
            for platform in platforms:
                intersection = bottomLine.intersection(platform)                    
                if not intersection.is_empty:
                    if intersection.geom_type == 'MultiPoint':
                        self.centre[1] = min(intersection.geoms, key=lambda x: x.coords[0][1]).coords[0][1] - enemyHalfSize
                    elif intersection.geom_type == 'Point':
                        self.centre[1] = intersection.coords[0][1] - enemyHalfSize
                    self.speedY = 0
                    break
        if self.centre[0] >= 800 - enemyHalfSize:
            self.speedX = -enemyLateralSpeed
        elif self.centre[0] <= enemyHalfSize:
            self.speedX = enemyLateralSpeed
        if self.centre[1] > 600 - enemyHalfSize:
            self.centre[1] = 600 - enemyHalfSize
            self.speedY = 0
        else:
            self.speedY += enemyAccelerationDown
        if self.speedY > enemyTerminalSpeed:
            self.speedY = enemyTerminalSpeed
        self.centre[0] += self.speedX
        self.centre[1] += self.speedY
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])

enemy1 = Enemy(410, 535)
enemy2 = Enemy(320, 435)
enemy3 = Enemy(600, 435)
enemy4 = Enemy(530, 325)
enemy5 = Enemy(500, 130)

def draw():
    screen.clear()
    for surface in surfaces:
        for i in range(1, len(surface)):
            screen.draw.line(surface[i-1], surface[i], (255,255,255))
    enemy1.draw()
    enemy2.draw()
    enemy3.draw()
    enemy4.draw()
    enemy5.draw()

def update(dt):
    enemy1.update(surfaceLines)
    enemy2.update(surfaceLines)
    enemy3.update(surfaceLines)
    enemy4.update(surfaceLines)
    enemy5.update(surfaceLines)

pgzrun.go()
