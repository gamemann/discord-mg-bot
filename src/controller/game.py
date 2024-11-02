import discord
import threading
import time

from datetime import datetime

from server import Server

class GameController():
    def __init__(self):
        self.servers = dict[int, Server]
        
        self.game_check_time = 30.0
        
    def game_thread(self):
        while True:
            # Get currentr date time.
            now = datetime.now()
            
            # Loop through all servers and check
            for k, srv in self.servers.items():
                # If we aren't ready for a new game, ignore.
                if srv.cur_game is not None or srv.next_game_cooldown < 1 and now < (srv.last_game + srv.next_game_cooldown):
                    continue
                
                try:
                    # Start new game.
                    srv.start_new_game()
                except Exception as e:
                    print(f"Failed to start new game for server ID '{k}' due to exception.")
                    print(e)
                
            # Sleep.
            time.sleep(self.game_check_time)
        
    def process_msg(self, msg: discord.Message):
        # Make sure this is from within a server.
        if msg.guild is None:
            return
        
        # Extract server ID
        sid = msg.guild.id
        
        # Make sure we exist in servers.
        if sid not in self.servers:
            self.servers[sid] = Server()
            
        srv = self.servers[sid]