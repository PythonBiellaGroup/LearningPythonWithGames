# https://github.com/Wireframe-Magazine/Wireframe57
# Wireframe #57: 

# Player movement prototype program:
# - Cursor left-right: move player
# - Cursor up: player jump
# - Space: shoot a rainbow

import pgzrun

from Listing22_PlatformsCode import AllPlatforms
from Listing24_Rainbows import AllRainbows
from Listing25_EnemiesCode import AllEnemies
from Listing26_Collectables import Collectables
from Listing27_Player import Player
from Listing28_ScreenPosition import ScreenPositionUpdate
from Listing29_BackgroundColour import BackgroundColour

allPlatforms = AllPlatforms()
allRainbows = AllRainbows()
player = Player()
allEnemies = AllEnemies()
allCollectables = Collectables()

screenPosition = 0
maxScreenPosition = allPlatforms.getMaxScreenPosition()

levelClear = False

def draw():
    screen.fill(BackgroundColour(screenPosition, maxScreenPosition))
    allPlatforms.draw()
    allEnemies.draw(screenPosition)
    allRainbows.draw(screenPosition)
    allCollectables.draw(screenPosition)
    player.draw(screenPosition)
    for i in range(player.lives):
        screen.blit('player_icon', (10+i*14, 10))
    if player.lives == 0:
        screen.draw.text("GAME OVER", center=(400, 260), fontsize=55, color=(255,0,0))
    if levelClear:
        screen.draw.text("LEVEL CLEAR", center=(400, 260), fontsize=55, color=(0,0,255))

def update(dt):
    global screenPosition, levelClear
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
    player.update(allPlatforms, allRainbows, allCollectables, allEnemies)
    screenPosition = ScreenPositionUpdate(player, screenPosition)
    allRainbows.update(allEnemies, allCollectables, screenPosition)
    allEnemies.update(allPlatforms, allRainbows, screenPosition)
    allCollectables.update(allPlatforms, player, screenPosition)
    allPlatforms.update(screenPosition)
    if player.centre[1] < -maxScreenPosition:
        levelClear = True

def on_key_down(key):
    if key == keys.SPACE:
        player.shootRainbow(allRainbows)

pgzrun.go()
