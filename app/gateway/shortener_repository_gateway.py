from abc import ABC, abstractmethod

class ShortenerRepositoryGateway(ABC):
    @abstractmethod
    def insert_url(self, original_url: str, short_code: str) -> dict:
        pass
    
    @abstractmethod
    def get_url_by_code(self, short_code: str) -> dict:
        pass