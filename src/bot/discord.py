import bot

from controller import GameController

class Discord(bot.Client):
    def __init__(self,
        token: str,
        controller: GameController          
    ):
        self.token = token
        self.controller = controller
        
    def connect(self):
        self.run(self.token)
    
    async def on_ready(self):
        print("Discord bot loaded!")
        
    async def on_message(self, msg):    
        if msg.guild is None:
            return
    
        # Pass to controller
        self.controller.process_msg(str(msg.guild.id), msg)
        