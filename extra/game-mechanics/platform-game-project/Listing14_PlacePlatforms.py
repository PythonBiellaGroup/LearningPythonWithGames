# Place platforms on play area
# - Mouse click: add the current platform
# - Mouse secondary click: select next platform
# - Cursor Left and Right: select previous or next platform
# - Cursor Up and Down: displace the screen
# - Space: print the platform positions
import pgzrun
from pygame import image, Color, Surface

from Listing11_PlatformNames import platformNames

platformImages = [Actor(platformNames[i]) for i in range(len(platformNames))]
platforms = []

activePlatform = 0
currentPosition = (0,0)
currentY = 0

def draw():
    screen.clear()
    for platform in platforms:
        platform.draw()
    platformImages[activePlatform].draw()

def update(dt):
    platformImages[activePlatform].pos = currentPosition

def on_mouse_down(pos, button):
    global activePlatform
    if mouse.LEFT == button:
        platforms.append(Actor(platformNames[activePlatform], currentPosition))
    elif mouse.RIGHT == button:
        activePlatform = (activePlatform + 1) % len(platformNames)

def on_mouse_move(pos):
    global currentPosition
    currentPosition = pos

def on_key_down(key):
    global currentY, activePlatform
    if key == keys.UP:
        currentY -= 100
        for platform in platforms:
            platform.pos = (platform.pos[0], platform.pos[1] + 100)
    elif key == keys.DOWN and currentY < 0:
        currentY += 100
        for platform in platforms:
            platform.pos = (platform.pos[0], platform.pos[1] - 100)
    elif key == keys.RIGHT:
        activePlatform = (activePlatform + 1) % len(platformNames)
    elif key == keys.LEFT:
        activePlatform = (activePlatform + len(platformNames) - 1) % len(platformNames)
    elif key == keys.SPACE:
        for platform in platforms:
            print("("+str(platformNames.index(platform.image))+","+
                  str(round(platform.pos[0]))+","+
                  str(round(platform.pos[1] + currentY))+"),")

pgzrun.go()

