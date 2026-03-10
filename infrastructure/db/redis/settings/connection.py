from infrastructure.config import get_environment_variable
import redis

env = get_environment_variable()

class RedisConnectionHandler:
    def __init__(self, db: int = env.REDIS_BASE) -> None:
        self.connection = redis.Redis(
            host=env.REDIS_HOST,
            port=env.REDIS_PORT,
            db=db,
            decode_responses=True
        )

    def __enter__(self) -> redis.Redis:
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()