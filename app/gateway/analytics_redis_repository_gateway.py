from abc import ABC, abstractmethod

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
    def get_unique_visitors_count(self, short_code: str) -> int:
        pass
    
    @abstractmethod
    def clear_stats(self, short_code: str) -> bool:
        pass
