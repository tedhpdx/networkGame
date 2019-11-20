from player import Player


class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.dice_player_0 = Player("", 0)
        self.dice_player_1 = Player("", 0)

    def get_opponent(self, dice_player):
        if dice_player.p == 0:
            return self.dice_player_1
        elif dice_player.p == 1:
            return self.dice_player_0

    def finished(self):
        if self.dice_player_0.finished and self.dice_player_1.finished:
            return True
        else:
            return False

    def update_object(self, dice_player):
        if dice_player.p == 0:
            self.dice_player_0 = dice_player
        elif dice_player.p == 1:
            self.dice_player_1 = dice_player

    def my_turn_yet(self, dice_player):
        if dice_player.p == 0:
            return self.dice_player_0.my_turn
        elif dice_player.p == 1:
            return self.dice_player_1.my_turn

    def get_winner(self):
        if self.dice_player_0.roll_total < self.dice_player_1.roll_total:
            self.dice_player_0.result["winner"] = True
            return self.dice_player_0
        elif self.dice_player_1.roll_total < self.dice_player_0.roll_total:
            self.dice_player_1.result["winner"] = True
            return self.dice_player_1
        else:  # then scores are equal
            self.dice_player_0.result["push"] = True
            self.dice_player_1.result["push"] = True
            return self.dice_player_0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def get_opponent_name(self, dice_player):
        if dice_player.p == 0:
            return self.dice_player_1.name
        elif dice_player.p == 1:
            return self.dice_player_0.name

    def play(self, player, move):

        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
