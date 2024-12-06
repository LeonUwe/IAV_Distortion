from quart import Blueprint
import asyncio
from socketio import AsyncServer
from Minigames.Minigame import Minigame
from RockPaperScissorsGame import RockPaperScissorsGame
from EnvironmentManagement.ConfigurationHandler import ConfigurationHandler

class RockPaperScissors_UI(Minigame):
    def __init__(self, sio: AsyncServer, blueprint: Blueprint, name="RockPaperScissors"):
        super().__init__(sio, blueprint, name)
        self._config_handler = ConfigurationHandler()

        # Lese Zeitlimit aus der Config, falls vorhanden, sonst Standard 5 Sekunden
        try:
            self._time_limit = int(self._config_handler.get_configuration()['minigame']['rock-paper-scissors']['time_limit'])
        except:
            self._time_limit = 5

        self._game = RockPaperScissorsGame()

        @self._sio.on('join_game')
        async def on_join_game(sid: str, data):
            player_id = data['player_id']
            if player_id in self._players:
                await self._sio.enter_room(sid, self.get_name())
                await self._sio.emit('joined', {'player_id': player_id}, room=player_id)

        @self._sio.on('player_choice')
        async def on_player_choice(sid: str, data):
            player_id = data['player_id']
            choice = data['choice']
            self._game.set_player_choice(player_id, choice)
            # Falls alle Spieler vor Ablauf der Zeit gewählt haben, Spiel sofort auswerten
            if self._game.all_players_chosen(num_players=len(self._players)):
                await self._finish_game_early()

    def set_players(self, *players: str) -> list[str]:
        super().set_players(*players)
        self._players.clear()
        for p in players:
            self._players.append(p)
        return self.get_players()

    async def _play(self) -> str:
        # Informiere Spieler über Spielstart
        await self._sio.emit('start_game', {'time_limit': self._time_limit}, room=self.get_name())

        # Warte auf Spielerentscheidungen oder bis Timeout erreicht ist
        try:
            await asyncio.wait_for(self._wait_for_choices(), timeout=self._time_limit)
        except asyncio.TimeoutError:
            # Nicht alle Spieler haben in der Zeit gewählt
            winner = self._handle_timeout()
            if winner is not None:
                await self._sio.emit('end_game', {'winner': winner}, room=self.get_name())
                self._players.clear()
                return winner
            else:
                # Beide haben nicht gewählt -> kein Gewinner
                await self._sio.emit('end_game', {'winner': None}, room=self.get_name())
                self._players.clear()
                return ""

        # Alle Spieler haben gewählt
        winner = self._game.determine_winner()
        if winner == "draw":
            await self._sio.emit('end_game', {'winner': "draw"}, room=self.get_name())
            self._players.clear()
            return ""
        else:
            await self._sio.emit('end_game', {'winner': winner}, room=self.get_name())
            self._players.clear()
            return winner

    async def _finish_game_early(self):
        # Wenn alle Spieler frühzeitig gewählt haben, direkt auswerten
        winner = self._game.determine_winner()
        if winner == "draw":
            await self._sio.emit('end_game', {'winner': "draw"}, room=self.get_name())
            self._players.clear()
        else:
            await self._sio.emit('end_game', {'winner': winner}, room=self.get_name())
            self._players.clear()

    async def _wait_for_choices(self):
        while not self._game.all_players_chosen(num_players=len(self._players)):
            await asyncio.sleep(0.1)

    def _handle_timeout(self):
        chosen_ids = self._game.player_choices.keys()
        # Einer hat gewählt, der andere nicht -> der Wähler gewinnt
        if len(chosen_ids) == 1:
            return list(chosen_ids)[0]
        # Kein Spieler hat gewählt
        return None

    def description(self) -> str:
        return "Rock-Paper-Scissors: Choose your move before time runs out!"
