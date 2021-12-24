
def ScreenPositionUpdate(player, screenPosition):
    if player.centre[1] - screenPosition < 150:
        screenPosition = player.centre[1] - 150
    elif player.centre[1] - screenPosition > 600 - 150:
        screenPosition = player.centre[1] - (600 - 150)
        if screenPosition > 0:
            screenPosition = 0
    return screenPosition

