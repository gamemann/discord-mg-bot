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
            CREATE TABLE IF NOT EXISTS discord_users (
                id BIGINT PRIMARY KEY,
                display_name VARCHAR (255),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            );
        """
        
        # Points table.
        table_points = """
            CREATE TABLE IF NOT EXISTS points (
                id SERIAL PRIMARY KEY,
                uid BIGINT NOT NULL,
                sid BIGINT NOT NULL,
                game VARCHAR(255),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                points int NOT NULL DEFAULT 0,
                FOREIGN KEY (uid) REFERENCES discord_users(id) ON DELETE CASCADE,
                FOREIGN KEY (sid) REFERENCES servers(sid) ON DELETE CASCADE  
            );
        """
        
        # Execute queries.
        await self.db.execute(table_servers)
        await self.db.execute(table_users)
        await self.db.execute(table_points)
        
        await self.db.commit()
        
    async def drop_tables(self):
        await self.db.execute("DROP TABLE IF EXISTS discord_users")
        await self.db.execute("DROP TABLE IF EXISTS servers")
        await self.db.execute("DROP TABLE IF EXISTS points")

    async def get_cfg(self) -> Config:
        pass
    
    async def get_user_stats(self, sid: str, uid: str) -> UserStats:
        stats: UserStats = UserStats()
        
        q = """
            WITH ins_server AS (
                INSERT INTO servers (sid)
                VALUES (%s)
                ON CONFLICT (sid) DO NOTHING
            ),
            ins_user AS  (
                INSERT INTO discord_users (id)
                VALUES (%s)
                ON CONFLICT(id) DO NOTHING
            )
            SELECT
                COALESCE(SUM(CASE WHEN sid = %s THEN points END), 0) AS srv_points,
                COALESCE(SUM(points), 0) AS global_points
            FROM points
            WHERE uid = %s
        """
        
        cur = self.db.cursor()
        await cur.execute(q, (sid, uid, sid, uid))
        res = await cur.fetchone()
                
        if res is not None:
            stats.srv_points = int(res[0])                
            stats.global_points += int(res[1])
            
        await cur.close()
        
        return stats
    
    async def add_user_points(self, sid: str, uid: str, game: str = "unknown", points: int = 0):
        q = """
            WITH ins_server AS (
                INSERT INTO servers (sid)
                VALUES (%s)
                ON CONFLICT (sid) DO NOTHING
            ),
            ins_user AS (
                INSERT INTO discord_users (id)
                VALUES (%s)
                ON CONFLICT (id) DO NOTHING
            )
            INSERT INTO points (sid, uid, game, points)
            VALUES (%s, %s, %s, %s)
        """
        
        cur = self.db.cursor()
        await cur.execute(q, (sid, uid, sid, uid, game, points))
        
        await cur.close()
        
    async def close(self):
        await self.db.close()