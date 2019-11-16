from random import randint

class Player():
    def __init__(self, name, cash):
        self.p = -1
        self.name = name
        self.cash = cash
        self.rolled = False
        self.roll = []
        self.roll_total = 0
        self.remaining_rolls = 5
        self.pickle_string = ""

    def roll_dice(self):
        self.roll.clear()
        for i in range(5):
            self.roll.append(randint(1, 6))

    def get_points(self, away_choice, point_value):
        if int(away_choice) != self.roll[point_value]:
            self.roll_total += self.roll[point_value]
