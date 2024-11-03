import sys
import traceback
import discord
import asyncio

from bot import Discord
from config import Config
from controller import GameController
from connection import ConnectionApi, ConnectionDb
from server import Server
from utils import debug_msg

HELP_MENU = f"""USAGE: python3 src/main.py [--cfg=<path> -l -h]
\t--cfg => The path to the config file.
\t-l --list => Whether to list config contents.
\t-h --help => Whether to print the help menu."""

async def main():
    # CLI arguments.
    cfg_path = "./conf.json"
    list = False
    help = False
    
    # Parse CLI.
    for k, arg in enumerate(sys.argv):
        # Handle config path.
        if arg.startswith("cfg="):
            cfg_path = arg.split('=')[1]
        elif arg == "--cfg" or arg == "c":
            val_idx = k + 1
            
            if val_idx < len(sys.argv):
                cfg_path = sys.argv[val_idx]
        
        # Handle list.
        if arg == "-l" or arg == "--list":
            list = True
            
        # Handle help menu.
        if arg == "-h" or arg == "--help":
            help = True
    
    # Print help menu if we need to.
    if help:
        print(HELP_MENU)
        
        sys.exit(0)
    
    # Load config.
    cfg = Config()
    
    try:
        cfg.load_from_fs(cfg_path)
    except Exception as e:
        print("Failed to load config!")
        print(e)
        
        # traceback.print_exc()
        
        sys.exit(1)
    
    # Check if we want to print the config.
    if list:
        cfg.print()
        
        sys.exit(0)
        
    # Create connection.
    conn = None
    save_to_fs = False
    
    # Check API connection.
    if cfg.connections.api.enabled:
        try:
            conn = ConnectionApi(cfg.connections.api.host, cfg.connections.api.token)
        except Exception as e:
            debug_msg(0, cfg, "Failed to setup API connection. Falling back to database if enabled.")
            debug_msg(0, cfg, e)
        
        # Check web config.
        if conn is not None and cfg.connections.api.web_config:
            try:
                conn.get_cfg()
                
                save_to_fs = True
            except Exception as e:
                debug_msg(0, cfg, "Failed to retrieve config through web API due to exception.")
                debug_msg(0, cfg, e)

    # Fallback to database.
    if conn is None and cfg.connections.db.enabled:
        try:
            conn = ConnectionDb(cfg.connections.db.host, cfg.connections.db.port, cfg.connections.db.user, cfg.connections.db.password)
        except Exception as e:
            debug_msg(0, cfg, "Failed to setup database due to exception. Web config and stats will be disabled!")
            debug_msg(0, cfg, e)
            
        # Check web config
        if conn is not None and cfg.connections.db.web_config:
            try:
                conn.get_cfg()
                
                save_to_fs = True
            except Exception as e:
                debug_msg(0, cfg, "Failed to retrieve config through the database due to exception.")
                debug_msg(0, cfg, e)
    
    # Check if we should save the config to our file system.
    if cfg.general.save_locally and save_to_fs:
        try:
            cfg.save_to_fs(cfg_path)
        except Exception as e:
            debug_msg(0, cfg, f"Failed to save config ({cfg_path}) to file system due to exception.")
            debug_msg(0, cfg, e)
    
    # Configure Discord intents.
    intents = discord.Intents.default()
    intents.message_content = True
    
    # Create Discord bot.
    try:
        bot = Discord(cfg.bot.token, intents)
        
        # Connect and run bot.
        asyncio.create_task(bot.connect_and_run())
    except Exception as e:
        debug_msg(0, cfg, "Failed to start and run Discord bot due to exception!")
        debug_msg(0, cfg, e)
        
        traceback.print_exc()
        
        sys.exit(1)

    debug_msg(1, cfg, "Connecting Discord bot...")
    
    # Wait for bot to become ready.
    while True:
        if bot.ready:
            break
        
        await asyncio.sleep(1)
        
    debug_msg(2, cfg, f"Discord bot connected successfully!")
    debug_msg(2, cfg, f"Creating game controller...")
    
    # Create controller and pass Discord bot.
    controller = GameController(bot, cfg)
    
    debug_msg(2, cfg, f"Starting game controller task...")
    
    # Create controller task for handling games.
    await asyncio.create_task(controller.game_thread())
    
    debug_msg(1, cfg, "Exiting program!")

if __name__ == "__main__":
    asyncio.run(main())