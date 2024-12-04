class Number_Guesser:
    def __init__(self, max_tries: int, number_range: list[int, int]):
        self.max_tries = max_tries
        self.number_range = number_range
        self.target_number = None
        self.current_attempts = 0
        self.ready_players = None
        self.players = []

    def set_number(self, player_id: str, number: int):
        """Set the target number by the first player."""
        if self.players[0] != player_id:
            raise ValueError("Only the first player can set the number.")
        if not (self.number_range[0] <= number <= self.number_range[1]):
            raise ValueError("The number must be between 1 and 10.")
        self.target_number = number
        self.current_attempts = 0
        self.ready_players = self.players[1]

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
        self.ready_players = None


