import discord
import asyncio
import traceback

from datetime import datetime
from bot import Discord
from server import Server
from config import Config
from utils import debug_msg

class GameController():
    def __init__(self, bot: Discord, cfg: Config):
        self.bot = bot
        self.cfg = cfg
        self.servers: dict[int, Server] = {}
        
        # Parse servers.
        self.parse_servers()
                
        # Register events and commands.
        self.register_events()
        self.register_commands()
        
    def parse_servers(self):
        # Fill servers from config.
        for k, srv in self.cfg.servers.items():
            debug_msg(2, self.cfg, f"Setting up server #{k}...")
            
            # We need to handle our games first.
            games: dict[str, any] = {}
            
            for k2, game in srv.games.items():
                debug_msg(3, self.cfg, f"Adding game '{k2}' to server #{k}...")
                
                games[k2] = game
                                
            self.servers[int(k)] = Server(
                bot = self.bot,
                cfg = self.cfg,
                id = int(k),
                games = games,
                next_game_random = srv.next_game_random,
                next_game_cooldown = srv.next_game_cooldown,
                game_start_auto = srv.game_start_auto,
                game_start_cmd = srv.game_start_cmd,
                game_start_manual = srv.game_start_manual
            )
        
    async def game_thread(self):
        debug_msg(1, self.cfg, "Starting game controller thread...")
        
        while True:
            debug_msg(4, self.cfg, "Checking servers in game controller thread...")
            
            # Get currentr date time.
            now = datetime.now()
            
            # Loop through all servers and check
            for k, srv in self.servers.items():
                # If we aren't ready for a new game, ignore.
                if not srv.game_start_auto or srv.cur_game is not None or srv.next_game_cooldown < 1 or (srv.last_game is not None and now.timestamp() < (srv.last_game.timestamp() + srv.next_game_cooldown)):
                    continue
                
                debug_msg(4, self.cfg, f"Found server #{k} ready for a new game...")
                
                try:
                    # Start new game.
                    asyncio.create_task(srv.start_new_game())
                except Exception as e:
                    print(f"Failed to start new game for server ID '{k}' due to exception.")
                    print(e)
                    traceback.print_exc()
                
            # Sleep.
            await asyncio.sleep(self.cfg.general.game_check_interval)

    def register_events(self):
        @self.bot.event
        async def on_message(msg: discord.Message):
            # Make sure this is from within a server.
            if msg.guild is None:
                return
            
            # Extract server ID
            sid = msg.guild.id
            
            if sid not in self.servers:
                return
                
            srv = self.servers[sid]
                    
            if srv.cur_game is not None:
                await srv.cur_game.process_msg(msg)
                
    def register_commands(self):
        @self.bot.command("start")
        async def start(ctx):
            print("Executed start")
        
        @self.bot.command("stop")
        async def stop(ctx):
            print("Executed stop")