# RockPaperScissorsGame.py

import time
import random

class RockPaperScissorsGame:
    def __init__(self, game_length: int):
        self._game_length = game_length  # Dauer des Spiels in Sekunden
        self._players_choices = {}       # Speichert die Auswahl der Spieler
        self._start_time = None

    def start(self):
        self._start_time = time.time()
        self._players_choices.clear()

    def set_choice(self, player_id: str, choice: str):
        if self._time_ran_out():
            return False  # Spiel ist beendet
        self._players_choices[player_id] = choice
        return True

    def get_result(self):
        if not self._time_ran_out() and len(self._players_choices) < len(self._players):
            return None  # Spiel läuft noch oder nicht alle Spieler haben gewählt

        choices = list(self._players_choices.items())
        if len(choices) < 2:
            return None  # Nicht genug Spieler haben eine Auswahl getroffen

        player1_id, player1_choice = choices[0]
        player2_id, player2_choice = choices[1]

        if player1_choice == player2_choice:
            return "tie"
        elif (player1_choice == "rock" and player2_choice == "scissors") or \
                (player1_choice == "scissors" and player2_choice == "paper") or \
                (player1_choice == "paper" and player2_choice == "rock"):
            return player1_id
        else:
            return player2_id

    def _time_ran_out(self):
        return time.time() - self._start_time > self._game_length

    def set_players(self, players):
        self._players = players
