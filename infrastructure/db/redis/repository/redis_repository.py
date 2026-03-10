import json
from redis.exceptions import RedisError
from app.gateway.redis_repository_gateway import RedisRepositoryGateway
from infrastructure.db.redis.settings.connection import RedisConnectionHandler

class RedisRepository(RedisRepositoryGateway):
    def __init__(self):
        self.__redis_handler = RedisConnectionHandler()
    
    def insert_key(self, short_code: str, original_url: str, short_url: str) -> bool:
        try:
            with self.__redis_handler as redis_conn:
                data = {
                    "original_url": original_url,
                    "short_code": short_code,
                    "short_url": short_url
                }
                redis_conn.setex(
                    name=short_code,
                    time=86400,
                    value=json.dumps(data)
                )
                return True
        except RedisError as e:
            raise Exception(f"Erro ao salvar no Redis: {str(e)}")
    
    def get_by_key(self, short_code: str) -> dict:
        try:
            with self.__redis_handler as redis_conn:
                data = redis_conn.get(short_code)
                
                if not data:
                    return None
                
                return json.loads(data)
        except RedisError as e:
            raise Exception(f"Erro ao buscar no Redis: {str(e)}")
        except json.JSONDecodeError:
            return None
