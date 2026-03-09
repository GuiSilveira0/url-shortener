import random
import string

from app.gateway.shortener_repository_gateway import ShortenerRepositoryGateway

class ShortenerUsecase:
    def __init__(
            self, 
            shortenerRepository: ShortenerRepositoryGateway
        ):
        None
        self.__shortenerRepository = shortenerRepository

    def generate_short_code(self, original_url: str, length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        code = ''.join(random.choice(chars) for _ in range(length))

        self.__shortenerRepository.insert_url(original_url, code)
        return code
    
    def get_original_url(self, short_code: str) -> str:
        url_data = self.__shortenerRepository.get_url_by_code(short_code)
        
        if not url_data:
            return None
        
        return url_data["original_url"]