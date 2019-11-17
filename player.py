from random import randint


class Player():
    def __init__(self, name, cash):
        self.pickle_string = ""
        self.p = None
        self.name = name
        self.cash = cash
        self.rolled = False
        self.roll = []
        self.roll_total = 0
        self.remaining_rolls = 6
        self.my_turn = False
        self.finished = False
        self.result = {
            "winner": False,
            "push": False,
            "loser": False
        }

    def roll_dice(self):
        self.roll.clear()
        for i in range(5):
            self.roll.append(randint(1, 6))

    def get_points(self, away_choice, point_value):
        if int(away_choice) != self.roll[point_value]:
            self.roll_total += self.roll[point_value]

    def reset(self):
        self.pickle_string = ""
        self.rolled = False
        self.roll = []
        self.roll_total = 0
        self.remaining_rolls = 6
        self.my_turn = False
        self.finished = False
        for r in self.result:
            r = False
