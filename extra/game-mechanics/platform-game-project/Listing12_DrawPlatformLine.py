# Draw platforms program:
# - Mouse click: add line to current platform
# - Delete or Backspace: delete last line
# - Cursor Left and Right: select previous or next platform
# - Space: print the platforms
import pgzrun
from pygame import image, Color, Surface

from Listing11_PlatformNames import platformNames

platforms = [Actor(platformNames[i], (800//2, 600//2)) for i in range(len(platformNames))]
lines = [[] for i in range(len(platformNames))]

activePlatform = 0
usePoint = False
lastPoint = (0,0)

def draw():
    screen.clear()
    platforms[activePlatform].draw()
    for i in range(1, len(lines[activePlatform])):
        screen.draw.line(lines[activePlatform][i-1], lines[activePlatform][i], (128,128,255))
    if usePoint and len(lines[activePlatform]) > 0:
        screen.draw.line(lines[activePlatform][len(lines[activePlatform])-1], lastPoint, (128,128,255))

def update(dt):
    pass

def on_mouse_down(pos, button):
    global usePoint, lastPoint
    usePoint = True
    lastPoint = pos

def on_mouse_up(pos):
    global usePoint
    lines[activePlatform].append(pos)
    usePoint = False

def on_mouse_move(pos):
    global lastPoint
    lastPoint = pos

def on_key_down(key):
    global activePlatform
    if key == keys.SPACE:
        displacedLines = [[(lines[i][j][0] - 400, lines[i][j][1] - 300) for j in range(len(lines[i]))] for i in range(len(lines))]
        print(str(displacedLines))
    elif key == keys.LEFT:
        activePlatform = (activePlatform - 1 + len(platformNames)) % len(platformNames);
    elif key == keys.RIGHT:
        activePlatform = (activePlatform + 1) % len(platformNames);
    elif len(lines[activePlatform]) > 0 and (key == keys.BACKSPACE or key == keys.DELETE):
        lines[activePlatform].pop(len(lines[activePlatform]) - 1)

pgzrun.go()
