from player import Player

class Game:
    def __init__(self,id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
        self.p0Name = ""
        self.p1Name = ""

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def get_opponent_name(self, p):
        if p == 0:
            return self.p1Name
        elif p == 1:
            return self.p0Name

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

    def winner(self):

        p1 = self.moves[0] #gets roll value for player 1
        p2 = self.moves[1] #gets roll value for player 2
        p1 = p1[1]
        p2 = p2[1]

        winner = -1
        if p1 > p2:
            winner = 0
        elif p1 == p2:
            winner = -1
        else:
            winner = 1
        return winner


    def resetWent(self):
        self.p1Went = False
        self.p2Went = False



