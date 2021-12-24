# Draw platforms program:
# - Mouse click: add line to current platform
# - Delete or Backspace: delete last line
# - Return: add new platform
# - Space: print the platforms
import pgzrun
from pygame import image, Color, Surface

lines = [[]]

usePoint = False
lastPoint = (0,0)

def draw():
    screen.clear()
    for line in lines:
        for i in range(1, len(line)):
            screen.draw.line(line[i-1], line[i], (255,255,255))
    if usePoint and len(lines[-1]) > 0:
        screen.draw.line(lines[-1][-1], lastPoint, (255,255,255))

def update(dt):
    pass

def on_mouse_down(pos, button):
    global usePoint, lastPoint
    usePoint = True
    lastPoint = pos

def on_mouse_up(pos):
    global usePoint
    lines[-1].append(pos)
    usePoint = False

def on_mouse_move(pos):
    global lastPoint
    lastPoint = pos

def on_key_down(key):
    if key == keys.SPACE:
        print(str(lines))
    elif key == keys.RETURN:
        lines.append([])
    elif len(lines[-1]) > 0 and (key == keys.BACKSPACE or key == keys.DELETE):
        lines[-1].pop(len(lines[-1]) - 1)

pgzrun.go()
