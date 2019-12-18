from random import randint


class Player():
    def __init__(self, name, cash):
        self.pickle_string = "player"
        self.global_id = 0
        self.p = 0
        self.ready = False
        self.name = name
        self.cash = cash
        self.rolled = False
        self.rolling = False
        self.roll = []
        self.roll_total = 0
        self.final_total = 0
        self.remaining_rolls = 6
        self.my_turn = False
        self.finished = False
        self.roll_reduction = 0
        self.busted = False
        self.killed_game = False
        self.left_game = False
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

    def reset(self, n=0):
        self.pickle_string = "player"
        self.ready = False
        self.rolled = False
        self.rolling = False
        self.roll = []
        self.roll_total = 0
        self.final_total = 0
        self.remaining_rolls = 6
        if (n == 0):
            self.my_turn = False
        self.finished = False
        self.roll_reduction = 0
        self.busted = False
        self.killed_game = False
        self.left_game = False
        for r in self.result:
            r = False
