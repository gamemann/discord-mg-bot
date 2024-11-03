import discord

class Discord(discord.Client):
    def __init__(self,
        token: str,
        intents: discord.Intents
    ):
        self.token = token
        
        super().__init__(intents = intents)
        
    async def connect_and_run(self):
        await self.start(token = self.token, reconnect = True)
        
    async def on_message(self, msg): 
        from bot import discord_chan
                   
        if msg.guild is None:
            return
            
        # Send message and signal.
        await discord_chan.emit(msg)
        