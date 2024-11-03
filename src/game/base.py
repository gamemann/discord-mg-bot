import discord
import random

from bot import Discord
from config import Config

class GameBase():
    def __init__(self,
        bot: Discord,
        cfg: Config,
        name: str = "Game",
        pick_weight = 50.0
    ):
        self.bot = bot
        self.cfg = cfg
        self.name = name
        self.pick_weight = pick_weight
        
    def start(self):
        pass
    
    def end(self):
        pass

    def process_msg(self, msg: discord.Message):
        pass
    