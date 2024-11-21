from flask import Blueprint, render_template, request, jsonify

# Blueprint for the Rock-Paper-Scissors minigame
# This allows modularity and easy integration of routes into the main project.
rock_paper_scissors_ui = Blueprint('rock_paper_scissors', __name__)

@rock_paper_scissors_ui.route('/rock_paper_scissors', methods=['GET'])
def index():
    """
    Route for the main page of the minigame.

    This function renders the 'rock_paper_scissors.html' file,
    which provides the user interface for the minigame.

    Returns:
        - Rendered HTML page with the game UI.
    """
    return render_template('rock_paper_scissors.html')

@rock_paper_scissors_ui.route('/rock_paper_scissors/play', methods=['POST'])
def play():
    """
    Route for the gameplay logic.
    This function is triggered when a player makes a selection.

    Process:
        1. Expects a JSON payload with the following fields:
           - player1: The choice of player 1 (e.g., "rock", "paper", "scissors").
           - player2: The choice of player 2 (or a bot-generated choice).
        2. Implements the game logic to determine the winner.
        3. Returns the result as a JSON response.

    Returns:
        - JSON object with the game result.
          Example: {"result": "Player 1 wins: Rock beats Scissors!"}
    """
    # Retrieve the JSON data from the request
    data = request.json
    player1_choice = data.get('player1')  # Choice of Player 1
    player2_choice = data.get('player2')  # Choice of Player 2 or the bot

    # Rock-Paper-Scissors game logic
    if player1_choice == player2_choice:
        # It's a tie if both players make the same choice
        result = f"Tie! Both players chose {player1_choice}."
    elif (player1_choice == "rock" and player2_choice == "scissors") or \
         (player1_choice == "scissors" and player2_choice == "paper") or \
         (player1_choice == "paper" and player2_choice == "rock"):
        # Player 1 wins
        result = f"Player 1 wins: {player1_choice} beats {player2_choice}!"
    else:
        # Player 2 wins
        result = f"Player 2 wins: {player2_choice} beats {player1_choice}!"

    # Return the result as a JSON response
    return jsonify({"result": result})
