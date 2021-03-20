import datetime
import pgzrun
import random

WIDTH = 600
HEIGHT = 300
TEXT_COLOR = (255, 255, 0)
SKY_COLOR = (0, 0, 0)
NUMBER_OF_SNOWFLAKES = 10

snowflakes = []
for i in range(NUMBER_OF_SNOWFLAKES):
  s = Actor('snowflake', (random.randint(0, WIDTH), random.randint(0, HEIGHT)))
  snowflakes.append(s)

def draw():
  screen.fill(SKY_COLOR)
  now = datetime.datetime.now()
  xmas = datetime.datetime(now.year, 12, 25)
  difference = xmas - now

  seconds = str(difference.seconds % 60).zfill(2)
  minutes = str(int(difference.seconds / 60) % 60).zfill(2)
  hours = str(int(difference.seconds / (60 * 60))).zfill(2)
  days = str(difference.days)


  countdown = days + ":" + hours + ":" + minutes + ":" + seconds

  screen.draw.text(countdown, centerx = WIDTH / 2, fontsize = 80, color = TEXT_COLOR)
  for s in snowflakes:
    s.y = (s.y + 1) % HEIGHT
    s.x = (s.x + random.randint(0, 3)) % WIDTH
    s.angle += random.randint(0,1)
    s.draw()
  

pgzrun.go()

# Challenges:
# 1) Change the sky colour to blue
# 2) Make the snow blow across the screen faster
# 3) Add more snowflakes