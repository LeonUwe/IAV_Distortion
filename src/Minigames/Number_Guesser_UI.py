from quart import Blueprint
from socketio import AsyncServer
from Minigames.Minigame import Minigame
from .Number_Guesser import Number_Guesser

class Number_Guesser_UI(Minigame):
    def __init__(self, sio: AsyncServer, blueprint: Blueprint, name=__name__):
        super().__init__(sio, blueprint, name)
        self.logic = Number_Guesser(sio, blueprint, name)
        self.sio = sio

        @self.sio.on('join_game')
        async def on_join_game(sid: str, data):
            await self.logic._sio.on('join_game')(sid, data)

        @self.sio.on('set_number')
        async def set_number(sid: str, data):
            await self.logic._sio.on('set_number')(sid, data)

        @self.sio.on('guess_number')
        async def guess_number(sid: str, data):
            await self.logic._sio.on('guess_number')(sid, data)
