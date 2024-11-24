from config import Config
from misc import UserStats

class Connection():
    def __init__(self):
        super().__init__()
    
    async def get_cfg(self) -> Config:
        pass
    
    async def get_user_stats(self, sid: str, uid: str) -> UserStats:
        pass
    
    async def add_user_points(self, sid: str, uid: str, game: str = "unknown", points: int = 0):
        pass