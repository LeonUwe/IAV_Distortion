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
        self._config_handler = ConfigurationHandler()
        try:
            self._min_length = int(
                self._config_handler.get_configuration()
                ['minigame']['reaction-contest']['min-length'])
        except Exception:
            self._min_length = 2
            print("Reaction_Contest_UI: No (proper) Configuration found for \
                ['minigame']['reaction-contest']['min-length']. Using default value of 2 seconds.")
        try:
            self._max_length = int(
                self._config_handler.get_configuration()
                ['minigame']['reaction-contest']['max-length'])
        except Exception:
            self._max_length = 5
            print("Reaction_Contest_UI: No (proper) Configuration found for \
                ['minigame']['reaction-contest']['max-length']. Using default value of 5 seconds.")
        try:
            self._game_ends = int(
                self._config_handler.get_configuration()
                ['minigame']['reaction-contest']['game-ends'])
        except Exception:
            self._game_ends = 10
            print("Reaction_Contest_UI: No (proper) Configuration found for \
                ['minigame']['reaction-contest']['game-ends']. Using default value of 10 seconds.")

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
        super().set_players()
        if players is None or len(players) < 1:
            print("Reaction_Contest_UI: The given player list is None or not long enough.")
            return []
        self._game_length = random.randint(self._min_length, self._max_length)
        self._game = Reaction_Contest(self._game_length)

        self._players.append(players[0])
        if len(players) > 1:
            self._players.append(players[1])
        return self.get_players()

    async def _play(self) -> str:
        await self._start_game()

        if len(self._players) < 2:
            asyncio.create_task(self._play_as_bot())

        game_start_time = asyncio.get_event_loop().time()
        while self._game.get_winner() == -1:
            if asyncio.get_event_loop().time() - game_start_time > self._game_ends:
                await self._send_tie()
                self._players.clear()
                return ""
            await asyncio.sleep(0.1)

        winner_index = self._game.get_winner()
        winner = "bot" if winner_index == 1 else self._players[winner_index]
        self._players.clear()
        return winner

    async def _start_game(self):
        self._game.start()
        await self._sio.emit('start_game', {'game-length': self._game_length}, room="Reaction_Contest")
        await asyncio.sleep(self._game_length)
        await self._sio.emit('box_green', room="Reaction_Contest")
        await asyncio.sleep(self._game_length)

    async def _send_tie(self):
        await self._sio.emit('tie', to="Reaction_Contest")

    def description(self) -> str:
        return "First player to click the green box wins!"

    async def _play_as_bot(self):
        """
        Simuliert einen zweiten Spieler, der nach dem Erscheinen des grünen Buttons klickt.
        """
        
        while not self._game.is_box_green():
            await asyncio.sleep(0.1)

        delay = random.uniform(0, 1.5)
        await asyncio.sleep(delay)

        self._game.press_button(1)
