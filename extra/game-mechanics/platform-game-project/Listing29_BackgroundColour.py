
backgroundBaseColour = (95, 148, 255)
backgroundColour = (0,0,0)

def BackgroundColour(screenPosition, maxScreenPosition):
    colourScale = -screenPosition / maxScreenPosition
    if colourScale > 1:
        colourScale = 1
    return (backgroundBaseColour[0]*colourScale,
            backgroundBaseColour[1]*colourScale,
            backgroundBaseColour[2]*colourScale)

