import discord

from datetime import datetime

from bot import Discord
from config import Config
from server import Server

class GameBase():
    def __init__(self,
        bot: Discord,
        cfg: Config,
        srv: Server,
        name: str = "Game",
        pick_weight = 50.0,
        channels: list[int] = []
    ):
        self.bot = bot
        self.cfg = cfg
        self.srv = srv
        self.name = name
        self.pick_weight = pick_weight
        self.channels = channels
        
    async def start(self):
        pass
    
    async def end(self):
        # Adjust last game time and current game.
        self.srv.last_game = datetime.now()
        self.srv.cur_game = None

    def process_msg(self, msg: discord.Message):
        pass
    