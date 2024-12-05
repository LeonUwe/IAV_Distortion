from quart import Blueprint
import asyncio
import random
from socketio import AsyncServer
from Minigames.Minigame import Minigame
from Minigames.Reaction_Contest import Reaction_Contest
from EnvironmentManagement.ConfigurationHandler import ConfigurationHandler

class Reaction_Contest_UI(Minigame):
    def __init__(self, sio: AsyncServer, blueprint: Blueprint, name=__name__):
        super().__init__(sio, blueprint, name)
        self._players: list[str] = []
        self._config_handler = ConfigurationHandler()
        try:
            self._min_length = int(
                self._config_handler.get_configuration()
                ['minigame']['reaction-contest']['min-length'])
        except Exception:
            self._min_length = 2
            print("Reaction_Contest_UI: No (proper) Configuration found for \
                ['minigame']['reaction-contest']['min-length']. Using default value of 5 seconds.")
        try:
            self._max_length = int(
                self._config_handler.get_configuration()
                ['minigame']['reaction-contest']['max-length'])
        except Exception:
            self._max_length = 5
            print("Reaction_Contest_UI: No (proper) Configuration found for \
                ['minigame']['reaction-contest']['max-length']. Using default value of 5 seconds.")
        
        self._game_length = random.randint(self._min_length, self._max_length)

        @self._sio.on('join_game')
        async def on_join_game(sid: str, data):
            player_id = data['player_id']
            if player_id in self._players:
                await self._sio.enter_room(sid, "Reaction_Contest")
                await self._sio.emit('joined', {'player_id': player_id}, room=player_id)

        @self._sio.on('click')
        async def handle_click(sid: str, data):
            player_id = data['player_id']
            player_index = self._players.index(player_id)
            self._game.press_button(player_index)

    def set_players(self, *players: str) -> list[str]:
        self._players.clear()
        self._players.extend(players[:2])
        self._game = Reaction_Contest(self._game_length)
        return self._players

    async def _play(self) -> str:
        await self._start_game()

        while self._game.get_winner() == -1:
            await asyncio.sleep(0.1)

        winner_index = self._game.get_winner()
        winner = self._players[winner_index]
        self._players.clear()
        return winner

    async def _start_game(self):
        self._game.start()
        await self._sio.emit('start_game', {'game-length': self._game_length}, room="Reaction_Contest")
        await asyncio.sleep(self._game_length)
        await self._sio.emit('box_green', room="Reaction_Contest")

    def description(self) -> str:
        return "First player to click the green box wins!"