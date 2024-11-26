class Number_Guesser:
    def __init__(self):
        self.target_number = None
        self.max_tries = 3
        self.current_attempts = 0
        self.active_player = None
        self.players = []

    def set_players(self, player1: str, player2: str):
        """Set the two players for the game."""
        self.players = [player1, player2]

    def set_number(self, player_id: str, number: int):
        """Set the target number by the first player."""
        if self.players[0] != player_id:
            raise ValueError("Only the first player can set the number.")
        if not (1 <= number <= 10):
            raise ValueError("The number must be between 1 and 10.")
        self.target_number = number
        self.current_attempts = 0
        self.active_player = self.players[1]

    def guess_number(self, player_id: str, guess: int) -> str:
        """Handle a guess by the second player."""
        if self.players[1] != player_id:
            raise ValueError("Only the second player can guess the number.")
        if self.target_number is None:
            raise ValueError("The target number has not been set yet.")
        if not (1 <= guess <= 10):
            raise ValueError("The guess must be between 1 and 10.")

        self.current_attempts += 1
        if guess == self.target_number:
            return "correct"
        if self.current_attempts >= self.max_tries:
            return "lose"
        return "higher" if guess < self.target_number else "lower"

    def reset(self):
        """Reset the game state."""
        self.target_number = None
        self.current_attempts = 0
        self.active_player = None
