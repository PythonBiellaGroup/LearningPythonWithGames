# Place platforms on play area
# - Mouse click: add the current enemy
# - Mouse secondary click: select next enemy
# - Cursor Left and Right: select previous or next enemy
# - Cursor Up and Down: displace the screen
# - Space: print the enemy positions
import pgzrun
from pygame import image, Color, Surface

from Listing11_PlatformNames import platformNames
from Listing15_Platforms import platforms

from Listing18_EnemyNames import enemyNames

platformImages = [Actor(platformNames[i]) for i in range(len(platformNames))]

enemyImages = [Actor(enemyNames[i // 2][i % 2]) for i in range(len(enemyNames) * 2)]
enemies = []


activeEnemy = 0
currentPosition = (0,0)
currentY = 0

def draw():
    screen.clear()
    for platform in platforms:
        platformImages[platform[0]].x = platform[1]
        platformImages[platform[0]].y = platform[2] - currentY
        platformImages[platform[0]].draw()
    for enemy in enemies:
        enemy.draw()
    enemyImages[activeEnemy].draw()

def update(dt):
    enemyImages[activeEnemy].pos = currentPosition

def on_mouse_down(pos, button):
    global activeEnemy
    if mouse.LEFT == button:
        enemies.append(Actor(enemyNames[activeEnemy // 2][activeEnemy % 2], currentPosition))
    elif mouse.RIGHT == button:
        activeEnemy = (activeEnemy + 1) % len(enemyImages)

def on_mouse_move(pos):
    global currentPosition
    currentPosition = pos

def on_key_down(key):
    global currentY, activeEnemy
    if key == keys.UP:
        currentY -= 100
        for enemy in enemies:
            enemy.pos = (enemy.pos[0], enemy.pos[1] + 100)
    elif key == keys.DOWN and currentY < 0:
        currentY += 100
        for enemy in enemies:
            enemy.pos = (enemy.pos[0], enemy.pos[1] - 100)
    elif key == keys.RIGHT:
        activeEnemy = (activeEnemy + 1) % len(enemyImages)
    elif key == keys.LEFT:
        activeEnemy = (activeEnemy + len(enemyImages) - 1) % len(enemyImages)
    elif key == keys.SPACE:
        for enemy in enemies:
            indexEnemy = 0
            direction = 1
            for i in range(len(enemyNames)):
                if enemy.image in enemyNames[i]:
                    indexEnemy = i
                    direction = enemyNames[i].index(enemy.image)
                    break
            print("("+str(indexEnemy)+","+str(1-direction*2)+","+
                  str(round(enemy.pos[0]))+","+
                  str(round(enemy.pos[1] + currentY))+"),")

pgzrun.go()

