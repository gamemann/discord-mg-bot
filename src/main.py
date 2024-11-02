import sys

from config import Config

def main():
    cfg_path = "./conf.json"
    
    # To Do: Parse CLI.
    
    # Load config.
    cfg = Config()
    
    try:
        cfg.load_from_fs(cfg_path)
    except Exception as e:
        print("Failed to load config!")
        print(e)
        
        sys.exit(1)
        
    cfg.print()

if __name__ == "__main__":
    main()