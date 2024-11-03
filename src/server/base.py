import random
import importlib

from datetime import datetime
from bot import Discord
from config import Config

class Server():    
    def __init__(self, bot: Discord, cfg: Config, id: int, games: dict[str, any], next_game_random = True, next_game_cooldown = 120.0, game_start_auto = False, game_start_cmd = True, game_start_manual = True):
        self.bot = bot
        self.id = id
        self.cfg = cfg
        
        self.cur_game = None
        self.last_game: datetime = None
        
        # Assign settings.
        self.next_game_cooldown = next_game_cooldown
        self.next_game_random = next_game_random
        
        self.game_start_auto = game_start_auto
        self.game_start_cmd = game_start_cmd
        self.game_start_manual = game_start_manual
        
        # Parse server games.
        self.games: dict[str, any] = {}
        
        for k, v in games.items():
            settings = v
            
            # We'll want to load the custom game class.
            # To Do: FIND A BETTER WAY TO DO THIS WITHOUT IMPORTING THE GAME MODULE FOR EVERY SERVER'S GAME.
            try:
                m = importlib.import_module(f"game.{k}")
                
                game_cl = m.Game(
                    bot = self.bot,
                    cfg = self.cfg,
                    srv = self,
                    **settings
                )
            except Exception as e:
                print(f"Failed to load game '{k}' for server '{self.id}' due to exception.")
                print(e)
                
                continue
            
            self.games[k] = game_cl
            
    def to_dict(self):
        return {
            "next_game_cooldown": self.next_game_cooldown,
            "next_game_random": self.next_game_random,
            "game_start_auto": self.game_start_auto,
            "game_start_cmd": self.game_start_cmd,
            "game_start_manual": self.game_start_manual,
            "games": self.games
        }
        
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
    
    async def start_new_game(self):
        # Get next game and start.
        next_game = self.get_next_game_key()
        
        self.cur_game = self.games[next_game]
        
        await self.cur_game.start()