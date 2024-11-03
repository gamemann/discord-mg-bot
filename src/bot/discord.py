import discord
from discord.ext import commands

class Discord(commands.Bot):
    def __init__(self,
        token: str,
        intents: discord.Intents
    ):
        self.token = token
        
        super().__init__(command_prefix = '/', intents = intents)
        
    async def connect_and_run(self):
        await self.start(token = self.token, reconnect = True)