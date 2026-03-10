import random
import string

from app.gateway.shortener_repository_gateway import ShortenerRepositoryGateway
from app.gateway.redis_repository_gateway import RedisRepositoryGateway
from infrastructure.config import get_environment_variable

env = get_environment_variable()

class ShortenerUsecase:
    def __init__(
            self, 
            shortenerRepository: ShortenerRepositoryGateway,
            redisRepository: RedisRepositoryGateway
        ):
        None
        self.__shortenerRepository = shortenerRepository
        self.__redisRepository = redisRepository

    def generate_short_code(self, original_url: str, short_url: str = "", length: int = 6, max_retries: int = 5) -> str:
        for attempt in range(max_retries):
            chars = string.ascii_letters + string.digits
            code = ''.join(random.choice(chars) for _ in range(length))
            
            if not short_url:
                short_url = f"{env.API_BASE_URL}/{code}"

            try:
                self.__shortenerRepository.insert_url(original_url, code)
                self.__redisRepository.insert_key(code, original_url, short_url)
                return code
            except ValueError:
                if attempt == max_retries - 1:
                    raise ValueError("Não foi possível gerar um código único")
                continue
    
    def get_original_url(self, short_code: str) -> str:
        redis_data = self.__redisRepository.get_by_key(short_code)
        
        if redis_data:
            return redis_data["original_url"]
        
        url_data = self.__shortenerRepository.get_url_by_code(short_code)
        
        if not url_data:
            return None
        
        short_url = f"{env.API_BASE_URL}/{short_code}"
        self.__redisRepository.insert_key(short_code, url_data["original_url"], short_url)
        
        return url_data["original_url"]