from connection import Connection
from config import Config
from misc import UserStats

class ConnectionDb(Connection):
    def __init__(self,
        host: str = "localhost",
        port: int = 5432,
        user: str = "root",
        password: str = ""
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
        # Load PostgreSQL connection.
        self.db = None
        
        super().__init__()

    def get_cfg(self) -> Config:
        pass
    
    def get_user_stats(self, sid: str, uid: str) -> UserStats:
        stats: UserStats = UserStats()
        
        # To Do: Get user stats from database.
        
        return stats
    
    def update_user_stats(self, sid: str, uid: str, stats: UserStats):
        # To Do: Update get stats in database.
        pass