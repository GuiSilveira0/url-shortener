from abc import ABC, abstractmethod
from typing import Optional


class AnalyticsRedisRepositoryGateway(ABC):
    
    @abstractmethod
    def increment_total_clicks(self, short_code: str) -> int:
        pass
    
    @abstractmethod
    def add_unique_ip(self, short_code: str, ip: str) -> bool:
        pass
    
    @abstractmethod
    def increment_daily_clicks(self, short_code: str, date: str) -> int:
        pass
    
    @abstractmethod
    def increment_hourly_clicks(self, short_code: str, hour: str) -> int:
        pass
    
    @abstractmethod
    def increment_country_clicks(self, short_code: str, country: str) -> int:
        pass
    
    @abstractmethod
    def increment_device_clicks(self, short_code: str, device: str) -> int:
        pass
    
    @abstractmethod
    def increment_browser_clicks(self, short_code: str, browser: str) -> int:
        pass

    @abstractmethod
    def get_realtime_stats(self, short_code: str) -> dict:
        pass

    @abstractmethod
    def get_cached_stats(self, cache_key: str) -> Optional[dict]:
        pass

    @abstractmethod
    def set_cached_stats(self, cache_key: str, data: dict, ttl: int = 60) -> None:
        pass

    @abstractmethod
    def invalidate_cache(self, short_code: str) -> None:
        pass