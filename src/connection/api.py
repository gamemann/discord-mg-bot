from connection import Connection
from config import Config
from misc import UserStats

class ConnectionApi(Connection):
    def __init__(self,
        host: str,
        token: str
    ):
        self.host = host
        self.token = token
        
        # Load HTTP listener.
        self.listener = None
        
        super().__init__()
        
    async def get_cfg(self) -> Config:
        # To Do: Get config from REST API.
        pass
    
    async def get_user_stats(self, sid: str, uid: str) -> UserStats:
        stats: UserStats = UserStats()
        
        # To Do: Get user stats from REST API.
        
        return stats
    
    async def add_user_points(self, sid: str, uid: str, game: str = "unknown", points: int = 0):
        # To Do: Update user stats via REST API.
        pass
