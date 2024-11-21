from Minigames.Minigame import Minigame

class RockPaperScissors(Minigame):
    """
    A Rock-Paper-Scissors minigame class inheriting from the base Minigame class.

    This class implements the required methods for a minigame:
    - `description()`: Provides a short description of the game.
    - `set_players(*players: str)`: Sets the players for the game.
    - `_play()`: Executes the game logic and determines the result.
    - `cancel()`: Cancels the game without declaring a winner.
    """

    def __init__(self):
        """
        Initializes the RockPaperScissors class.
        - `self.players`: A list to store player choices.
        - `self.result`: Stores the result of the game.
        """
        super().__init__()
        self.players = []  # Stores the choices of the players
        self.result = None  # Stores the result of the game

    def description(self) -> str:
        """
        Provides a short description of the game.

        Returns:
            str: A description of the game.
        """
        return "Play Rock, Paper, Scissors against another player or a bot."

    def set_players(self, *players: str):
        """
        Sets the players and their choices for the minigame.

        Parameters:
            *players (str): The choices of the players (e.g., "rock", "paper", "scissors").
        """
        self.players = players

    async def _play(self) -> str:
        """
        Starts the Rock-Paper-Scissors minigame.

        This method determines the winner based on the choices of the players.
        The game follows these rules:
        - Rock beats Scissors.
        - Scissors beats Paper.
        - Paper beats Rock.

        If both players choose the same symbol, it results in a draw.

        Returns:
            str: The result of the game (e.g., who won or if it was a draw).
        """
        if len(self.players) < 2:
            return "Two players are required to start the game."

        player1_choice = self.players[0]
        player2_choice = self.players[1]

        # Determine the result of the game
        if player1_choice == player2_choice:
            self.result = f"It's a draw! Both players chose {player1_choice}."
        elif (player1_choice == "rock" and player2_choice == "scissors") or \
             (player1_choice == "scissors" and player2_choice == "paper") or \
             (player1_choice == "paper" and player2_choice == "rock"):
            self.result = f"Player 1 wins: {player1_choice} beats {player2_choice}!"
        else:
            self.result = f"Player 2 wins: {player2_choice} beats {player1_choice}!"

        return self.result

    def cancel(self):
        """
        Cancels the game without a winner.

        This method is used to terminate the game early, marking it as canceled.
        """
        self.result = "The game was canceled."
