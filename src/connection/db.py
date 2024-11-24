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
        self.db: psycopg.AsyncConnection = None
        
        super().__init__()
        
    async def connect(self):
        info = f"host={self.host} port={self.port} dbname={self.name} user={self.user} password={self.password}"
        
        self.db = await psycopg.AsyncConnection.connect(
            conninfo = info
        )
        
    async def setup(self):
        # Servers table
        table_servers = """
            CREATE TABLE IF NOT EXISTS servers (
                sid BIGINT PRIMARY KEY  
            );
        """
        
        # Users table
        table_users = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                dis_uid BIGINT
            );
        """
        
        # Points table.
        table_points = """
            CREATE TABLE IF NOT EXISTS points (
                id SERIAL PRIMARY KEY,
                uid BIGINT NOT NULL,
                sid BIGINT NOT NULL,
                game TEXT NOT NULL,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                points int NOT NULL DEFAULT 0,
                FOREIGN KEY (uid) REFERENCES users(dis_uid) ON DELETE CASCADE,
                FOREIGN KEY (sid) REFERENCES servers(sid) ON DELETE CASCADE  
            );
        """
        
        # Execute queries.
        await self.db.execute(table_servers)
        await self.db.execute(table_users)
        await self.db.execute(table_points)
        
        await self.db.commit()
        
    async def drop_tables(self):
        await self.db.execute("DROP TABLE IF EXISTS users")
        await self.db.execute("DROP TABLE IF EXISTS servers")
        await self.db.execute("DROP TABLE IF EXISTS points")

    async def get_cfg(self) -> Config:
        pass
    
    async def get_user_stats(self, sid: str, uid: str) -> UserStats:
        stats: UserStats = UserStats()
        
        q = """
            WITH ins_server AS (
                INSERT INTO servers (sid)
                VALUES ($1)
                ON CONFLICT (sid) DO NOTHING
            ),
            ins_user AS  (
                INSERT INTO users (dis_uid)
                VALUES ($2)
                ON CONFLICT(dis_uid) DO NOTHING
            )
            SELECT
                COALESCE(SUM(CASE WHEN sid = $1 THEN points END), 0) AS srv_points,
                COALESCE(SUM(points), 0) AS global_points
            FROM points
            WHERE uid = $2
        """
        
        res = await self.db.fetchrow(q, sid, uid)
        
        if res is not None:
            stats.srv_points = int(res["srv_points"])                
            stats.global_points += int(res["global_points"]) 
        
        return stats
    
    async def add_user_points(self, sid: str, uid: str, game: str = "unknown", points: int = 0):
        q = """
            WITH ins_server AS (
                INSERT INTO servers (sid)
                VALUES ($1)
                ON CONFLICT (sid) DO NOTHING
            ),
            ins_user AS (
                INSERT INTO users (dis_uid)
                VALUES ($2)
                ON CONFLICT (dis_uid) DO NOTHING
            )
            INSERT INTO points (sid, uid, game, points)
            VALUES ($1, $2, $3, $4)
        """
        
        await self.db.execute(q, sid, uid, game, points)
        
    async def close(self):
        await self.db.close()