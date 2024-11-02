from bot import Discord    

class GameBase():
    bot: Discord = None
    name: str = None
    
    pick_weight: float = 50.0
    
    def __init__(self,
        bot: Discord,
        name: str,
        pick_weight: float = 50.0             
    ):
        self.bot = bot
        self.name = name
        self.pick_weight = pick_weight
        
        super().__init__()
        
    def start():
        pass
    
    def end():
        pass
    