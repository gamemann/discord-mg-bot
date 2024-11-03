import random
import importlib

from datetime import datetime
from bot import Discord

class Server():    
    def __init__(self, bot: Discord, id: int, games: dict[str, any]):
        self.bot = bot
        self.id = id
        
        self.games: dict[str, any] = {}
        
        for k, v in games.items():
            settings = v
            
            # We'll want to load the custom game class.
            # To Do: FIND A BETTER WAY TO DO THIS WITHOUT IMPORTING THE GAME MODULE FOR EVERY SERVER'S GAME.
            try:
                m = importlib.import_module(f"game.{k}")
                game_cl = m.Game(bot = self.bot, **settings)
            except Exception as e:
                print(f"Failed to load game '{k}' for server '{self.id}' due to exception.")
                print(e)
                
                continue
            
            self.games[k] = game_cl
        
        self.cur_game = None
        self.last_game: datetime = None
        self.next_game_cooldown = 120.0
        
        self.next_game_random = True
        
    def get_next_game_key(self):
        # Check for random.
        if self.next_game_random:
            next_key = random.choice(list(self.games.keys()))
            
            return next_key
        
        # Return next game in dictionary.
        keys = self.games.keys()
        cur_key = self.cur_game
        
        if cur_key not in self.games:
            raise Exception("Current game is not in games dictionary.")
        
        cur_idx = keys.index(cur_key)
        
        next_idx = (cur_idx + 1) % len(keys)
            
        return keys[next_idx]
    
    def start_new_game(self):
        # Get next game and start.
        next_game = self.get_next_game_key()
        
        self.cur_game = self.games[next_game]
        
        self.cur_game.start()