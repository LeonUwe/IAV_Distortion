# RockPaperScissors_UI.py

from Minigames.Minigame import Minigame
from quart import Blueprint
from socketio import AsyncServer
import asyncio
import random

from RockPaperScissorsGame import RockPaperScissorsGame

class RockPaperScissors_UI(Minigame):
    def __init__(self, sio: AsyncServer, blueprint: Blueprint, name=__name__):
        super().__init__(sio, blueprint, name)
        self._players = []
        self._game_length = 5  # Zeit für die Auswahl in Sekunden

        # Initialisiere die Spiel-Logik
        self._game = RockPaperScissorsGame(self._game_length)

        # SocketIO-Ereignisse registrieren
        @self._sio.on('join_game')
        async def on_join_game(sid: str, data):
            player_id = data['player_id']
            if player_id in self._players:
                await self._sio.enter_room(sid, "RockPaperScissors")
                await self._sio.emit('joined', {'player_id': player_id}, room=player_id)

        @self._sio.on('make_choice')
        async def handle_choice(sid: str, data):
            player_id = data['player_id']
            choice = data['choice']  # 'rock', 'paper', oder 'scissors'
            self._game.set_choice(player_id, choice)
            await self._sio.emit('choice_made', {'player_id': player_id}, room="RockPaperScissors")

    def set_players(self, *players: str) -> list[str]:
        super().set_players()
        if not players or len(players) < 1:
            print("RockPaperScissors_UI: Keine Spieler angegeben.")
            return []
        self._players = list(players)
        self._game.set_players(self._players)
        # Wenn nur ein Spieler, füge einen Bot hinzu
        if len(self._players) == 1:
            self._players.append('bot')
            self._game.set_players(self._players)
        return self._players

    async def _play(self) -> str:
        # Starte das Spiel
        self._game.start()
        await self._sio.emit('start_game', {'game_length': self._game_length}, room="RockPaperScissors")

        # Bot-Logik
        if 'bot' in self._players:
            await asyncio.sleep(random.uniform(1, self._game_length))
            bot_choice = random.choice(['rock', 'paper', 'scissors'])
            self._game.set_choice('bot', bot_choice)
            await self._sio.emit('choice_made', {'player_id': 'bot'}, room="RockPaperScissors")

        # Warte bis die Zeit abgelaufen ist oder alle Spieler gewählt haben
        while not self._game._time_ran_out():
            if len(self._game._players_choices) == len(self._players):
                break
            await asyncio.sleep(0.1)

        # Ergebnis ermitteln
        result = self._game.get_result()

        # Spieler über das Ergebnis informieren
        await self._sio.emit('game_result', {'result': result}, room="RockPaperScissors")

        # Gewinner-ID zurückgeben
        if result == 'tie':
            return ''
        else:
            return result

    def description(self) -> str:
        return f"Klassisches Schere-Stein-Papier-Spiel. Triff deine Auswahl innerhalb von {self._game_length} Sekunden."

    def cancel(self):
        super().cancel()
        self._game = None  # Spiel zurücksetzen
