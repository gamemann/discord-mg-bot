import random

from datetime import datetime

class Server():    
    def __init__(self, id: str):
        self.id = id
        
        self.games = dict[str, any]
        
        self.cur_game: str = None
        self.last_game: datetime = datetime.now()
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
        

            
                
        
        
        
        
        
    
        