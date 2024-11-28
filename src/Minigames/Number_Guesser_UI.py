from quart import Blueprint
import asyncio
from socketio import AsyncServer
from Minigames.Minigame import Minigame
from .Number_Guesser import Number_Guesser

class Number_Guesser_UI(Minigame):
    def __init__(self, sio: AsyncServer, blueprint: Blueprint, name=__name__):
        super().__init__(sio, blueprint, name)
        self._game = None

        @self._sio.on('join_game')
        async def on_join_game(sid: str, data):
            player_id = data['player_id']
            if len(self.get_players()) < 2 and player_id not in self.get_players():
                self._players.append(player_id)
                await self._sio.enter_room(sid, self.get_name())
                await self._sio.emit('joined', {'player_id': player_id}, room=sid)

        @self._sio.on('set_number')
        async def on_set_number(sid: str, data):
            player_id = data['player_id']
            if player_id == self._players[0]:  # Only the first player sets the number
                number = data.get('number')
                try:
                    self._game.set_number(number)
                    await self._sio.emit('number_set', {'status': 'success'}, room=self.get_name())
                except ValueError as e:
                    await self._sio.emit('number_set', {'status': 'error', 'message': str(e)}, room=sid)

        @self._sio.on('guess_number')
        async def on_guess_number(sid: str, data):
            player_id = data['player_id']
            if player_id == self._players[1]:  # Only the second player guesses
                guess = data.get('guess')
                try:
                    result = self._game.guess_number(guess)
                    await self._sio.emit('guess_result', {'result': result}, room=self.get_name())
                    if result['status'] == 'won' or result['status'] == 'lost':
                        self.cancel()
                except ValueError as e:
                    await self._sio.emit('guess_result', {'status': 'error', 'message': str(e)}, room=sid)

    def set_players(self, *players: str) -> list[str]:
        super().set_players()
        if len(players) < 2:
            print("Number_Guesser_UI: At least two players are required.")
            return []
        self._players = list(players[:2])
        self._game = Number_Guesser()  # Initialize a new game instance
        return self.get_players()

    async def _play(self) -> str:
        if not self._game:
            return "Game not initialized."
        await self._sio.emit('game_ready', room=self.get_name())
        while not self._game.is_over():
            await asyncio.sleep(1)  # Polling for game updates
        return self._players[1] if self._game.is_winner() else self._players[0]

    def description(self) -> str:
        return "A guessing game where one player sets a number, and the other tries to guess it within a limited number of attempts."

    def cancel(self) -> None:
        super().cancel()
        self._game = None
        asyncio.create_task(self._sio.emit('game_cancelled', room=self.get_name()))
