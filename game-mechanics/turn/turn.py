import random, time

class Action():
    def __init__(self, owner, opponent):
        self.owner = owner
        self.opponent = opponent

    def execute(self):
        pass


class Attack(Action):
    def __init__(self, owner, opponent):
        super().__init__(owner, opponent)

    def execute(self):
        self.owner.defending = False
        if self.opponent.defending:
            hit = random.randrange(10,20)
        else:
            hit = random.randrange(20,40)
        self.opponent.health -= hit
        print('{} is hit! (-{})'.format(self.opponent.name, hit))


class Defend(Action):
    def __init__(self, owner, opponent):
        super().__init__(owner, opponent)

    def execute(self):
        self.owner.defending = True
        print(self.owner.name, 'is defending!')


class Player():
    players = []

    def __init__(self, name, inputmethod):
        self.name = name
        self.inputmethod = inputmethod
        self.health = 100
        self.defending = False
        self.players.append(self)

    def __str__(self):
        description = "Player: {}\n{}\nHealth = {}\nDefending = {}\n".format(
            self.name,
            '-' * (8 + len(self.name)),
            self.health,
            self.defending
        )
        return(description)

    @classmethod
    def get_next_player(cls, p):
        # get the next player still in the game
        current_index = cls.players.index(p)
        current_index = (current_index + 1) % len(cls.players)
        while cls.players[current_index].health < 1:
            current_index = (current_index + 1) % len(cls.players)
        return cls.players[current_index]

    def choose_action(self):
        print(self.name, ': [a]ttack or [d]efend?')
        action_choice = self.inputmethod(['a', 'd'])
        if action_choice == 'a':
            print('Choose an opponent')
            # build up a list of possible opponents
            opponent_list = []
            for p in self.players:
                if p != self and p.health > 0:
                    print('[{}] {}'.format(self.players.index(p), p.name))
                    opponent_list.append(str(self.players.index(p)))
            # use input to get the opponent of player's action
            opponent = self.players[int(self.inputmethod(opponent_list))]
            return Attack(self, opponent)
        else:
            return Defend(self, None)


def human_input(choices):
    choice = input()
    while choice not in choices:
        print('Try again!')
        choice = input()
    return choice

def computer_input(choices):
    time.sleep(2)
    choice = random.choice(choices)
    print(choice)
    return choice

# add 2 players to the battle, with their own input method
hero = Player('The Hero', human_input)
enemy = Player('The Enemy', computer_input)

# the hero has the first turn
current_player = Player.players[0]
playing = True

# game loop
while playing:

    # print all players with health remaining
    for p in Player.players:
        if p.health > 0:
            print(p, end='\n\n')

    # current player's action executed
    action = current_player.choose_action()
    time.sleep(2)
    action.execute()

    # continue only if more than 1 player with health remaining
    if len([p for p in Player.players if p.health > 0]) > 1:
        current_player = Player.get_next_player(current_player)
        time.sleep(2)
    else:
        playing = False

for p in Player.players:
    if p.health > 0:
        print('**', p.name, 'wins!')
