import asyncio
from quart import Blueprint
from socketio import AsyncServer
from .Number_Guesser import Number_Guesser
from Minigames.Minigame import Minigame

class Number_Guesser_UI(Minigame):
    def __init__(self, sio: AsyncServer, blueprint: Blueprint, name=__name__):
        super().__init__(sio, blueprint, name)
        self.logic = Number_Guesser()

        # SocketIO Event Handlers
        @self._sio.on("set_number")
        async def handle_set_number(sid: str, data):
            player_id = data.get("player_id")
            number = data.get("number")
            try:
                self.logic.set_number(player_id, number)
                await self._sio.emit("number_set", {"success": True}, to=sid)
            except ValueError as e:
                await self._sio.emit("number_set", {"success": False, "error": str(e)}, to=sid)

        @self._sio.on("guess_number")
        async def handle_guess_number(sid: str, data):
            player_id = data.get("player_id")
            guess = data.get("guess")
            try:
                result = self.logic.guess_number(player_id, guess)
                response = {"result": result}
                if result == "correct":
                    response["winner"] = player_id
                elif result == "lose":
                    response["correct_number"] = self.logic.target_number
                await self._sio.emit("guess_result", response, to=sid)
            except ValueError as e:
                await self._sio.emit("guess_result", {"error": str(e)}, to=sid)

    async def _play(self, *players: str) -> str:
        super()._play(*players)
        self.logic.set_players(*players)
        await self._sio.emit("game_started", {"players": players})
        # Wait until game ends
        while True:
            if self.logic.target_number is None:
                await asyncio.sleep(1)
            else:
                break
        return self.logic.players[1]

    def description(self) -> str:
        super().description()
        return (
            "Number Guesser: Player 1 sets a number. "
            "Player 2 has 3 attempts to guess the number."
        )
