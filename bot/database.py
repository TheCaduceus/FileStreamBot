import asyncio
from redis.asyncio import Redis
from bot.config import Database
from typing import List, Union

class RedisClient:
    def __init__(self, host: str, port: int, password: str):
        self.db = Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True,
        )

    def s_l(self, text: str) -> List[str]:
        return text.split(" ")

    def l_s(self, lst: List[str]) -> str:
        return " ".join(lst).strip()

    def ensure_str(self, value: Union[str, int]) -> str:
        if isinstance(value, (str, int)):
            return str(value)
        else:
            raise ValueError("Invalid input type: value should be str or int")

    async def is_inserted(self, var: Union[str, int], id: Union[str, int]) -> bool:
        try:
            var_str = self.ensure_str(var)
            id_str = self.ensure_str(id)
            users = await self.fetch_all(var_str)
            return id_str in users
        except Exception as e:
            print(f"Error in is_inserted: {e}")
            return False

    async def insert(self, var: Union[str, int], id: Union[str, int]) -> bool:
        try:
            var_str = self.ensure_str(var)
            id_str = self.ensure_str(id)
            users = await self.fetch_all(var_str)
            if id_str not in users:
                users.append(id_str)
                await self.db.set(var_str, self.l_s(users))
            return True
        except Exception as e:
            print(f"Error in insert: {e}")
            return False

    async def fetch_all(self, var: str) -> List[str]:
        if not isinstance(var, str):
            raise ValueError("Invalid input type: 'var' should be str")
        
        try:
            users = await self.db.get(var)
            return [] if users is None or users == "" else self.s_l(users)
        except Exception as e:
            print(f"Error in fetch_all: {e}")
            return []

    async def delete(self, var: Union[str, int], id: Union[str, int]) -> bool:
        try:
            var_str = self.ensure_str(var)
            id_str = self.ensure_str(id)
            users = await self.fetch_all(var_str)
            if id_str in users:
                users.remove(id_str)
                await self.db.set(var_str, self.l_s(users))
            return True
        except Exception as e:
            print(f"Error in delete: {e}")
            return False

# Configuration
REDIS_URI = Database.REDIS_URI.split(":")
host = REDIS_URI[0]
port = int(REDIS_URI[1])
password = Database.REDIS_PASSWORD

# db Instance 
db = RedisClient(host, port, password)
