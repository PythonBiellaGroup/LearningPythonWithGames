# Player movement prototype program:
# - Cursor left-right: move player
# - Cursor up: player jump
import pgzrun
from pygame import image, Color, Surface
from shapely.geometry import Point, Polygon, LineString
from shapely.affinity import translate

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
        self.centredLineString = LineString([(-playerHalfSize,-playerHalfSize),
                                             (-playerHalfSize,playerHalfSize),
                                             (playerHalfSize,playerHalfSize),
                                             (playerHalfSize,-playerHalfSize)])
        self.lineString = translate(self.centredLineString, self.centre[0], self.centre[1])
        self.speedY = 0
        self.jumping = False
    def draw(self):
        for i in range(len(self.lineString.coords)):
            screen.draw.line((self.lineString.coords[i-1][0],self.lineString.coords[i-1][1]-screenPosition),
                             (self.lineString.coords[i][0],self.lineString.coords[i][1]-screenPosition), (255,0,0))
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
                    break
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
            screen.draw.line((surface[i-1][0], surface[i-1][1]-screenPosition),
                             (surface[i][0], surface[i][1]-screenPosition), (255,255,255))
    player.draw()

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

pgzrun.go()
