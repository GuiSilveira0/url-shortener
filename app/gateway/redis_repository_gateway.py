from abc import ABC, abstractmethod

class RedisRepositoryGateway(ABC):
    @abstractmethod
    def insert_key(self, short_code: str, original_url: str, short_url: str) -> bool:
        pass
    
    @abstractmethod
    def get_by_key(self, short_code: str) -> dict:
        pass