class RockPaperScissorsGame:
    def __init__(self):
        self.player_choices = {}
        self.choices = ["rock", "paper", "scissors"]

    def set_player_choice(self, player_id, choice):
        if choice in self.choices:
            self.player_choices[player_id] = choice

    def all_players_chosen(self, num_players=2):
        return len(self.player_choices) == num_players

    def determine_winner(self):
        if len(self.player_choices) < 2:
            return None
        player_ids = list(self.player_choices.keys())
        p1_choice = self.player_choices[player_ids[0]]
        p2_choice = self.player_choices[player_ids[1]]

        if p1_choice == p2_choice:
            return "draw"

        # Regeln: Rock schlägt Scissors, Paper schlägt Rock, Scissors schlägt Paper
        if (p1_choice == "rock" and p2_choice == "scissors") or \
                (p1_choice == "paper" and p2_choice == "rock") or \
                (p1_choice == "scissors" and p2_choice == "paper"):
            return player_ids[0]
        else:
            return player_ids[1]

    def reset_game(self):
        self.player_choices.clear()