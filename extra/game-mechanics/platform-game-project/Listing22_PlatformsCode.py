from pgzero.builtins import Actor
from shapely.geometry import LineString

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
    def update(self, screenPosition):
        for i in range(len(platforms)):
            self.platformActors[i].x = platforms[i][1]
            self.platformActors[i].y = platforms[i][2] - screenPosition
    def getMaxScreenPosition(self):
        return -platforms[-1][2] - maxHeightPlatform/2

