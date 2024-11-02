import json

from utils import safe_write

class ConnectionApi():
    def __init__(self):
        self.enabled: bool = False
        self.host: str = "http://localhost"
        self.token: str = None
        
    def as_json(self):
        return {
            "enabled": self.enabled,
            "host": self.host,
            "token": self.token
        }
    
class ConnectionDb():
    def __init__(self):
        self.enabled: bool = False
        self.host: str = "localhost"
        self.port: int = 5432
        self.user: str = "root"
        self.password: str = ""
        
    def as_json(self):
        return {
            "enabled": self.enabled,
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password
        }

class Connections():
    def __init__(self):
        self.api: ConnectionApi = ConnectionApi()
        self.db: ConnectionDb = ConnectionDb()
        
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
    
class General():
    def as_json(self):
        return {}

class Server():
    def as_json(self):
        return {}

class Config():
    def __init__(self):
        self.connections: Connections = Connections()
        self.bot: Bot = Bot()
        self.general: General = General()
        self.servers: dict[str, Server] = {}
        
    def as_json(self):
        return {
            "connections": self.connections.as_json(),
            "bot": self.connections.as_json(),
            "general": self.general.as_json(),
            "servers": {k: v.as_json() for k, v in self.servers.items()}
        }
    
    def load_from_fs(self, path: str = "./conf.json"):
        data = {}
        
        with open(path) as f:
            data = json.load(f)
            
        if data is None:
            raise Exception("JSON data is None.")
            
        # Load connections.
        if "connections" in data:
            conns = data["connections"]
            
            # Load API.
            if "api" in conns:
                api = conns["api"]
                
                self.connections.api.enabled = api.get("enabled", self.connections.api.enabled)
                self.connections.api.host = api.get("host", self.connections.api.host)
                self.connections.api.token = api.get("token", self.connections.token)
                
            # Load database.
            if "db" in conns:
                db = conns["db"]
                
                self.connections.db.enabled = db.get("enabled", self.connections.db.enabled)
                self.connections.db.host = db.get("host", self.connections.db.host)
                self.connections.db.port = db.get("port", self.connections.db.port)
                self.connections.db.user = db.get("user", self.connections.db.user)
                self.connections.db.password = db.get("password", self.connections.db.password)
                
        # Load bot settings.
        if "bot" in data:
            bot = data["bot"]
            
            self.bot.token = bot.get("token", self.bot.token)

    def save_to_fs(self, path):
        contents = json.dump(self.as_json(), indent = 4)
        
        # Safely save to file system.
        safe_write(path, contents)
        
    def print(self):
        print("Settings")
        
        # General settings.
        print(f"\tGeneral")
        
        # Bot Settings.
        print(f"\tDiscord Bot")
        print(f"\t\tToken => {self.bot.token}")
        
        # Connections
        print(f"\tConnections")
        
        print(f"\t\tAPI")
        api = self.connections.api
        
        print(f"\t\t\tEnabled => {self.connections.api.enabled}")
        print(f"\t\t\tHost => {self.connections.api.host}")
        print(f"\t\t\tToken => {self.connections.api.token}")
        
        print(f"\t\tDatabase")
        db = self.connections.db
        
        print(f"\t\t\tEnabled => {db.enabled}")
        print(f"\t\t\tHost => {db.host}")
        print(f"\t\t\tPort => {db.port}")
        print(f"\t\t\tUser => {db.user}")
        print(f"\t\t\tPassword => {db.password}")
        
        
    