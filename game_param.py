class GameParam():
    def __init__(self, num_players, rounds, ante, away_choice):
        self.num_players = num_players
        self.rounds = rounds
        self.ante = ante
        self.away_choice = away_choice
        self.pickle_string = "game"
