from connection import Connection
from config import Config
from misc import UserStats

import psycopg

class ConnectionDb(Connection):
    def __init__(self,
        host: str = "localhost",
        port: int = 5432,
        name: str = "discord_mg",
        user: str = "root",
        password: str = ""
    ):
        self.host = host
        self.port = port
        self.name = name
        self.user = user
        self.password = password
        
        # Load PostgreSQL connection.
        self.db = None
        
        super().__init__()
        
    async def connect(self):
        info = f"host={self.host} port={self.port} dbname={self.name} user={self.user} password={self.password}"
        
        self.db = await psycopg.AsyncConnection.connect(
            conninfo = info
        )
        
    async def setup(self):
        pass

    def get_cfg(self) -> Config:
        pass
    
    def get_user_stats(self, sid: str, uid: str) -> UserStats:
        stats: UserStats = UserStats()
        
        # To Do: Get user stats from database.
        
        return stats
    
    def update_user_stats(self, sid: str, uid: str, stats: UserStats):
        # To Do: Update get stats in database.
        pass