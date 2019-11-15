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
