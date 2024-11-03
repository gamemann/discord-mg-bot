import json

from utils import safe_write

class Debug():
    def __init__(self):
        self.verbose = 1
        self.log_to_file = False
        self.log_dir = "./logs"
        
    def as_json(self):
        return {
            "verbose": self.verbose,
            "log_to_file": self.log_to_file,
            "log_dir": self.log_dir
        }
        
class General():
    def __init__(self):
        self.save_locally = True
        self.game_check_interval = 120.0

    def as_json(self):
        return {
            "save_locally": self.save_locally,
            "game_check_interval": self.game_check_interval
        }

class ConnectionApi():
    def __init__(self):
        self.enabled = False
        self.host = "http://localhost"
        self.token = None
        self.web_config = True
        
    def as_json(self):
        return {
            "enabled": self.enabled,
            "host": self.host,
            "token": self.token,
            "web_config": self.web_config
        }
    
class ConnectionDb():
    def __init__(self):
        self.enabled = False
        self.host = "localhost"
        self.port = 5432
        self.user = "root"
        self.password = ""
        self.web_config = True
        
    def as_json(self):
        return {
            "enabled": self.enabled,
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "web_config": self.web_config
        }

class Connections():
    def __init__(self):
        self.api = ConnectionApi()
        self.db = ConnectionDb()
        
    def as_json(self):
        return {
            "api": self.api.as_json(),
            "db": self.db.as_json()
        }
    
class Bot():
    def __init__(self):
        self.token: str = None
        
    def as_json(self):
        return {
            "token": self.token
        }

class Server():
    def __init__(self):
        self.games: dict[str, any] = {}
        
        self.next_game_cooldown = 120.0
        self.next_game_random = True
        
        self.game_start_auto = False
        self.game_start_cmd = True
        self.game_start_manual = True
        
    def as_json(self):
        return {
            "games": self.games,
            "next_game_cooldown": self.next_game_cooldown,
            "next_game_random": self.next_game_random,
            "game_start_auto": self.game_start_auto,
            "game_start_cmd": self.game_start_cmd,
            "game_start_manual": self.game_start_manual
        }

class Config():
    def __init__(self):
        self.debug = Debug()
        self.general = General()
        self.connections = Connections()
        self.bot = Bot()
        self.servers: dict[int, Server] = {}
        
    def as_json(self):
        return {
            "debug": self.debug.as_json(),
            "general": self.general.as_json(),
            "connections": self.connections.as_json(),
            "bot": self.connections.as_json(),
            "servers": {k: v.as_json() for k, v in self.servers.items()}
        }
    
    def load_from_fs(self, path: str = "./conf.json"):
        data = {}
        
        with open(path) as f:
            data = json.load(f)
            
        if data is None:
            raise Exception("JSON data is None.")
        
        # Debug settings.
        if "debug" in data:
            debug = data["debug"]
            
            self.debug.verbose = debug.get("verbose", self.debug.verbose)
            self.debug.log_to_file = debug.get("log_to_file", self.debug.log_to_file)
            self.debug.log_dir = debug.get("log_dir", self.debug.log_dir)
        
        # General settings.
        if "general" in data:
            general = data["general"]
            
            self.general.save_locally = general.get("save_locally", self.general.save_locally)
            self.general.game_check_interval = general.get("game_check_interval", self.general.game_check_interval)
            
        # Load connections.
        if "connections" in data:
            conns = data["connections"]
            
            # Load API.
            if "api" in conns:
                api = conns["api"]
                
                self.connections.api.enabled = api.get("enabled", self.connections.api.enabled)
                self.connections.api.host = api.get("host", self.connections.api.host)
                self.connections.api.token = api.get("token", self.connections.token)
                self.connections.api.web_config = api.get("web_config", self.connections.api.web_config)
                
            # Load database.
            if "db" in conns:
                db = conns["db"]
                
                self.connections.db.enabled = db.get("enabled", self.connections.db.enabled)
                self.connections.db.host = db.get("host", self.connections.db.host)
                self.connections.db.port = db.get("port", self.connections.db.port)
                self.connections.db.user = db.get("user", self.connections.db.user)
                self.connections.db.password = db.get("password", self.connections.db.password)
                self.connections.db.web_config = db.get("web_config", self.connections.db.web_config)
                
        # Load bot settings.
        if "bot" in data:
            bot = data["bot"]
            
            self.bot.token = bot.get("token", self.bot.token)
            
        if "servers" in data:
            servers = data["servers"]
            
            for id, srv in servers.items():
                val = Server()
                
                val.next_game_random = srv.get("next_game_random", val.next_game_random)
                val.next_game_cooldown = srv.get("next_game_cooldown", val.next_game_cooldown)
                
                val.game_start_auto = srv.get("game_start_auto", val.game_start_auto)
                val.game_start_cmd = srv.get("game_start_cmd", val.game_start_cmd)
                val.game_start_manual = srv.get("game_start_manual", val.game_start_manual)
                
                # Check for games.
                if "games" in srv:
                    games = srv["games"]
                    
                    for k, v in games.items():
                        val.games[k] = v
                
                self.servers[int(id)] = val

    def save_to_fs(self, path: str):
        contents = json.dump(self.as_json(), indent = 4)
        
        # Safely save to file system.
        safe_write(path, contents)
        
    def print(self):
        print("Settings")
        
        print("\tDebug")
        debug = self.debug
        
        print(f"\t\tVerbose => {debug.verbose}")
        print(f"\t\tLog To File => {debug.log_to_file}")
        print(f"\t\tLog Directory => {debug.log_dir}")
        
        # General settings
        print(f"\tGeneral")
        
        print(f"\t\tSave Config Locally => {self.general.save_locally}")
        print(f"\t\tGame Check Interval => {self.general.game_check_interval}")
        
        # Bot settings
        print(f"\tDiscord Bot")
        print(f"\t\tToken => {self.bot.token}")
        
        # Connection settings
        print(f"\tConnections")
        
        print(f"\t\tAPI")
        api = self.connections.api
        
        print(f"\t\t\tEnabled => {api.enabled}")
        print(f"\t\t\tHost => {api.host}")
        print(f"\t\t\tToken => {api.token}")
        print(f"\t\t\tWeb Config => {api.web_config}")
        
        print(f"\t\tDatabase")
        db = self.connections.db
        
        print(f"\t\t\tEnabled => {db.enabled}")
        print(f"\t\t\tHost => {db.host}")
        print(f"\t\t\tPort => {db.port}")
        print(f"\t\t\tUser => {db.user}")
        print(f"\t\t\tPassword => {db.password}")
        print(f"\t\t\tWeb Config => {db.web_config}")
        
        # Server settings
        print(f"\t\tServers")
        
        for k, v in self.servers.items():
            print(f"\t\t\tServer #{k}")
            
            print(f"\t\t\t\tNext Game Random => {v.next_game_random}")
            print(f"\t\t\t\tNext Game Cooldown => {v.next_game_cooldown}")
            
            print(f"\t\t\t\tGame Start Auto => {v.game_start_auto}")
            print(f"\t\t\t\tGame Start Command => {v.game_start_cmd}")
            print(f"\t\t\t\tGame Start Manual => {v.game_start_manual}")
            
            if len(v.games) > 0:
                print(f"\t\t\t\tGames")
                
                for k, v in v.games.items():
                    print(f"\t\t\t\t\t{k}:")
                    
                    for k2, v2 in v.items():
                        print(f"\t\t\t\t\t\t{k2} => {v2}")