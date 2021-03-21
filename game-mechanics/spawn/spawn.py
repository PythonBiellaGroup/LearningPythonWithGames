# https://github.com/Wireframe-Magazine/Wireframe-10
# Wireframe #10: Recreate Pang's sprite spawning mechanic, pages 22-23
import pgzrun

class Enemy(Actor):
    # static list, to keep track of all enemies
    enemies = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # add enemy to the enemies list
        self.enemies.append(self)
    def destroy(self):
        # remove self from the enemies list
        self.enemies.remove(self)
        self = None

class LargeEnemy(Enemy):
    def __init__(self, **kwargs):
        # all large-sized enemies have the same image
        super().__init__(image='large_enemy', **kwargs)
    def destroy(self):
        # spawn 2 medium-sized enemies when destroying
        m1 = MediumEnemy(pos=(self.pos[0]-40,self.pos[1]-40))
        m2 = MediumEnemy(pos=(self.pos[0]+40,self.pos[1]+40))
        super().destroy()

class MediumEnemy(Enemy):
    def __init__(self, **kwargs):
        # all medium-sized enemies have the same image
        super().__init__(image='medium_enemy', **kwargs)
    def destroy(self):
        # spawn 2 small-sized enemies when destroying
        s1 = SmallEnemy(pos=(self.pos[0]-20,self.pos[1]-20))
        s2 = SmallEnemy(pos=(self.pos[0]+20,self.pos[1]+20))
        super().destroy()

class SmallEnemy(Enemy):
    def __init__(self, **kwargs):
        # all small-sized enemies have the same image
        super().__init__(image='small_enemy', **kwargs)

# start with 2 large-sized enemies
l1 = LargeEnemy(pos=(300,150))
l2 = LargeEnemy(pos=(150,300))

# destroy the first enemy in the enemies list
def on_key_down():
    if len(Enemy.enemies) > 0:
        Enemy.enemies[0].destroy()

# draw all enemies in static enemies list
def draw():
    screen.clear()
    for e in Enemy.enemies:
        e.draw()

pgzrun.go()