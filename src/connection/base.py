from config import Config
from misc import UserStats

class Connection():
    def __init__(self):
        super().__init__()
    
    def get_cfg(self) -> Config:
        pass
    
    def get_user_stats(self, sid: str, uid: str) -> UserStats:
        pass
    
    def update_user_stats(self, sid: str, uid: str, stats: UserStats):
        pass
    
    
    
    