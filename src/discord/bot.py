import discord

from controller import GameController

class Discord(discord.Client):
    token: str
    
    game_controller: GameController
        
    def __init__(self,
        token: str,
        game_controller: GameController          
    ):
        self.token = token
        self.game_controller = game_controller
        
    def connect(self):
        self.run(self.token)
    
    async def on_ready(self):
        print("Discord bot loaded!")
        
    async def on_message(self, msg):
        pass
        