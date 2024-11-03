import discord
import asyncio

from datetime import datetime
from bot import Discord, discord_chan
from server import Server
from config import Config
from utils import debug_msg

class Game():
    def __init__(self, obj: any):
        self.obj = obj

class GameController():
    def __init__(self, bot: Discord, cfg: Config, servers: dict[int, Server]):
        self.bot = bot
        self.cfg = cfg
        self.servers: dict[int, Server] = servers
        
        self.game_check_time = 30.0
        
        # Subscribe to message channel.
        discord_chan.subscribe(self.process_msg)
        
    async def game_thread(self):
        debug_msg(1, self.cfg, "Starting game controller thread...")
        
        while True:
            debug_msg(4, self.cfg, "Checking servers in game controller thread...")
            
            # Get currentr date time.
            now = datetime.now()
            
            # Loop through all servers and check
            for k, srv in self.servers.items():
                # If we aren't ready for a new game, ignore.
                if srv.cur_game is not None or srv.next_game_cooldown < 1 and (srv.last_game is not None and now < (srv.last_game + srv.next_game_cooldown)):
                    continue
                
                debug_msg(4, self.cfg, f"Found server #{k} ready for a new game...")
                
                try:
                    # Start new game.
                    srv.start_new_game()
                except Exception as e:
                    print(f"Failed to start new game for server ID '{k}' due to exception.")
                    print(e)
                
            # Sleep.
            await asyncio.sleep(self.game_check_time)
        
    def process_msg(self, msg: discord.Message):
        # Make sure this is from within a server.
        if msg.guild is None:
            return
        
        # Extract server ID
        sid = msg.guild.id
        
        if sid not in self.servers:
            return
            
        srv = self.servers[sid]
                
        if srv.cur_game is not None:
            srv.cur_game.process_msg(msg)