import random


class Number_Guesser:
    def __init__(self):
        self.target_number = None
        self.max_tries = 3
        self.players = []

    def description(self) -> str:
        """Returns a brief description of the game."""
        return (
            "'Number Guesser' Game:\n"
            "The first player chooses a number between 1 and 10.\n"
            "The second player has three attempts to guess the number.\n"
            "After each wrong attempt, they will receive a hint ('higher' or 'lower').\n"
            "If the second player guesses correctly, they win. Otherwise, they lose after using all attempts."
        )

    def set_players(self, *players: str):
        """Sets the players for the game."""
        if len(players) != 2:
            raise ValueError("There must be exactly two players.")
        self.players = players

    def play(self) -> str:
        """Main game logic."""
        if len(self.players) != 2:
            raise ValueError("Two players must be set before starting the game.")

        # Player 1 chooses the target number
        while True:
            try:
                self.target_number = int(input(f"{self.players[0]}, choose a number between 1 and 10: "))
                if 1 <= self.target_number <= 10:
                    break
                else:
                    print("The number must be between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")


        # Player 2 tries to guess the number
        for attempt in range(1, self.max_tries + 1):
            try:
                guess = int(input(f"{self.players[1]}, guess the number (Attempt {attempt} of {self.max_tries}): "))

                if guess < self.target_number:
                    print("Too low! Try again.")
                elif guess > self.target_number:
                    print("Too high! Try again.")
                else:
                    return f"{self.players[1]} guessed the number! You win!"
            except ValueError:
                print("Please enter a valid number.")

        # Player 2 did not guess correctly
        return f"{self.players[1]}, you lost. The correct number was {self.target_number}."


if __name__ == "__main__":
    game = Number_Guesser()
    print(game.description())

    # Set the players
    game.set_players("Player 1", "Player 2")

    # Start the game
    result = game.play()
    print(result)
