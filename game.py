from player import Player


class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.dice_player_0 = Player("", 0)
        self.dice_player_1 = Player("", 0)
        self.dice_players = {}
        self.number_of_players = 0
        self.rounds = 0
        self.ante = 0
        self.away_choice = 0
        self.active_players = 0
        self.top_total = 100

    def update_game(self, game_params):
        self.number_of_players = game_params.num_players
        self.rounds = game_params.rounds
        self.ante = game_params.ante
        self.away_choice = game_params.away_choice

    def update_top_total(self, t_t):
        if t_t < self.top_total:
            self.top_total = t_t

    def get_opponent(self, dice_player):
        if dice_player.p == 0:
            return self.dice_player_1
        elif dice_player.p == 1:
            return self.dice_player_0
        elif dice_player.p == 2:
            return self.dice_players[0]

    def get_opp_dict(self):
        return self.dice_players

    def finished(self):
        for d in self.dice_players:
            if d and self.dice_players[d].finished is not True:
                return False
        return True

    def add_active_player(self):
        self.active_players += 1

    def update_object(self, dice_player):
        self.dice_players[dice_player.p] = dice_player
        if dice_player.remaining_rolls == 0 and dice_player.final_total < self.top_total:
            self.top_total = dice_player.roll_total

        if dice_player.p == 0:
            self.dice_player_0 = dice_player
        elif dice_player.p == 1:
            self.dice_player_1 = dice_player

    def my_turn_yet(self, dice_player):
        for d in self.dice_players:
            if self.dice_players[d].my_turn is True:
                return False
        return True

    def get_winner(self):
        for d in self.dice_players:
            if d and self.top_total == self.dice_players[d].roll_total:
                self.dice_players[d].result["winner"] = True
                return self.dice_players[d]
        '''
        
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
        '''

    def connected(self):
        for d in self.dice_players:
            if self.active_players < 1:
                return False
            if d and self.dice_players[d].ready is False:
                return False
        return True
