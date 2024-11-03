import sys
# import traceback

from bot import Discord
from config import Config
from controller import GameController

HELP_MENU = f"""USAGE: python3 src/main.py [--cfg=<path> -l -h]
\t--cfg => The path to the config file.
\t-l --list => Whether to list config contents.
\t-h --help => Whether to print the help menu."""

def main():
    cfg_path = "./conf.json"
    list = False
    help = False
    
    # Parse CLI.
    for arg in sys.argv:
        # Handle config path.
        if arg.startswith("cfg="):
            cfg_path = arg.split('=')[1]
        
        # Handle list.
        if arg.startswith("-l") or arg.startswith("--list"):
            list = True
            
        # Handle help menu.
        if arg.startswith("-h") or arg.startswith("--help"):
            help = True
            
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
        
    # We need to configure the game controller before passing to Discord bot.
    controller = GameController()
    
    # Create Discord bot.
    bot = Discord(cfg.bot.token, controller)
    
    # Connect and run bot.
    bot.connect()

if __name__ == "__main__":
    main()