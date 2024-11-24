from quart import Blueprint
from socketio import AsyncServer
import asyncio

class Number_Guesser:
    def __init__(self, sio: AsyncServer, blueprint: Blueprint, name=__name__):
        self._sio = sio
        self._blueprint = blueprint
        self._name = name
        self._players = []
        self._target_number = None
        self._max_tries = 3
        self._current_try = 0

        @self._sio.on('join_game')
        async def on_join_game(sid: str, data):
            player_id = data['player_id']
            if len(self._players) < 2:
                self._players.append(player_id)
                await self._sio.emit('player_joined', {'player_id': player_id}, room=sid)

                if len(self._players) == 2:
                    await self._sio.emit('ready', {'players': self._players}, room="Number_Guesser")
            else:
                await self._sio.emit('game_full', {'message': 'Spiel ist bereits voll.'}, room=sid)

        @self._sio.on('set_number')
        async def set_number(sid: str, data):
            if sid != self._players[0]:
                await self._sio.emit('error', {'message': 'Nur der erste Spieler kann die Zahl setzen.'}, room=sid)
                return

            try:
                number = int(data['number'])
                if not (1 <= number <= 10):
                    await self._sio.emit('error', {'message': 'Die Zahl muss zwischen 1 und 10 liegen.'}, room=sid)
                    return

                self._target_number = number
                await self._sio.emit('number_set', {'message': 'Zahl wurde gesetzt!'}, room="Number_Guesser")
            except ValueError:
                await self._sio.emit('error', {'message': 'Ungültige Eingabe.'}, room=sid)

        @self._sio.on('guess_number')
        async def guess_number(sid: str, data):
            if sid != self._players[1]:
                await self._sio.emit('error', {'message': 'Nur der zweite Spieler kann raten.'}, room=sid)
                return

            if self._current_try >= self._max_tries:
                await self._sio.emit('game_over', {'message': 'Keine Versuche mehr übrig.'}, room="Number_Guesser")
                return

            try:
                guess = int(data['guess'])
                self._current_try += 1

                if guess < self._target_number:
                    await self._sio.emit('hint', {'hint': 'zu niedrig'}, room=sid)
                elif guess > self._target_number:
                    await self._sio.emit('hint', {'hint': 'zu hoch'}, room=sid)
                else:
                    await self._sio.emit('winner', {'message': f'{self._players[1]} hat die Zahl erraten!'}, room="Number_Guesser")
                    self.reset_game()
                    return

                if self._current_try == self._max_tries:
                    await self._sio.emit(
                        'game_over',
                        {'message': f'Game Over! Die Zahl war {self._target_number}.'},
                        room="Number_Guesser"
                    )
                    self.reset_game()
            except ValueError:
                await self._sio.emit('error', {'message': 'Ungültige Eingabe.'}, room=sid)

    def reset_game(self):
        """Setzt den Spielzustand zurück."""
        self._players.clear()
        self._target_number = None
        self._current_try = 0
