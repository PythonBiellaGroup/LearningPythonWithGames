class State():
    def __init__(self):
        # a dictionary containing possible states,
        # and rules for moving to them
        self.rules = {}
    # adds a state:rule pair to the 'rules' dictionary
    def addrule(self, state, rule):
        self.rules[state] = rule
    def update(self):
        pass
    def draw(self):
        pass

class StateMachine():
    def __init__(self):
        self.current = None
        self.frame = 0
    def update(self):
        # only update current state if one exists
        if self.current == None:
            return
        # increment the frame
        self.frame += 0.01
        # if any rule evaluates to 'True' then
        # switch to that state (and reset the timer)
        for s, r in self.current.rules.items():
            if r():
                self.current = s
                self.frame = 0
        # call the current state's update() method
        self.current.update()
    # call the current state's update() method
    def draw(self):
        if self.current == None:
            return
        self.current.draw()

sm = StateMachine()

def drawtitle():
    screen.draw.text("Title screen", (50, 50), fontsize=40, color="white")
    screen.draw.text("Press [space] to start", (50, 80), fontsize=40, color="white")
titlescreen = State()
titlescreen.draw = drawtitle

def drawgame():
    screen.draw.text("Game screen", (50, 50), fontsize=40, color="white")
    screen.draw.text("Press [e] to end game", (50, 80), fontsize=40, color="white")
gamescreen = State()
gamescreen.draw = drawgame

def drawcontinue():
    screen.draw.text("Continue  screen", (50, 50), fontsize=40, color="white")
    screen.draw.text("Press [space] to play again", (50, 80), fontsize=40, color="white")
    # display the time remaining until 10 seconds have passed
    screen.draw.text(str(int(10 - sm.frame)+1), (50, 110), fontsize=40, color="white")
continuescreen = State()
continuescreen.draw = drawcontinue

titlescreen.addrule(gamescreen, lambda: keyboard.space)
gamescreen.addrule(continuescreen, lambda: keyboard.e)
continuescreen.addrule(titlescreen, lambda: sm.frame >= 10)
continuescreen.addrule(gamescreen, lambda: keyboard.space)

sm.current = titlescreen

def update():
    sm.update()

def draw():
    screen.clear()
    sm.draw()
