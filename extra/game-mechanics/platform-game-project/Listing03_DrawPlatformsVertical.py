# Draw platforms program:
# - Mouse click: add line to current platform
# - Delete or Backspace: delete last line
# - Return: add new platform
# - Space: print the platforms
# - Cursor up and down: move screen
import pgzrun
from pygame import image, Color, Surface

lines = [[]]

usePoint = False
lastPoint = (0,0)

screenPosition = 0

def draw():
    screen.clear()
    for line in lines:
        for i in range(1, len(line)):
            screen.draw.line((line[i-1][0],line[i-1][1]-screenPosition), (line[i][0],line[i][1]-screenPosition), (255,255,255))
    if usePoint and len(lines[-1]) > 0:
        screen.draw.line((lines[-1][-1][0],lines[-1][-1][1]-screenPosition), lastPoint, (255,255,255))

def update(dt):
    pass

def on_mouse_down(pos, button):
    global usePoint, lastPoint
    usePoint = True
    lastPoint = pos

def on_mouse_up(pos):
    global usePoint
    lines[-1].append((pos[0], pos[1]+screenPosition))
    usePoint = False

def on_mouse_move(pos):
    global lastPoint
    lastPoint = pos

def on_key_down(key):
    global screenPosition
    if key == keys.SPACE:
        print(str(lines))
    elif key == keys.RETURN:
        lines.append([])
    elif len(lines[-1]) > 0 and (key == keys.BACKSPACE or key == keys.DELETE):
        lines[-1].pop(len(lines[-1]) - 1)
    if key == keys.UP:
        screenPosition -= 100
    elif key == keys.DOWN:
        screenPosition += 100
        if screenPosition > 0:
            screenPosition = 0

pgzrun.go()
