from abc import ABC, abstractmethod
from typing import List, Optional

class AnalyticsRepositoryGateway(ABC):
    
    @abstractmethod
    def insert_analytics(self, analytics_data: dict) -> None:
        pass

    @abstractmethod
    def get_stats_summary(self, short_code: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_clicks_by_period(self, short_code: str, start_date: str, end_date: str) -> List[dict]:
        pass

    @abstractmethod
    def get_top_countries(self, short_code: str, limit: int = 10) -> List[dict]:
        pass

    @abstractmethod
    def get_device_distribution(self, short_code: str) -> List[dict]:
        pass

    @abstractmethod
    def get_browser_distribution(self, short_code: str) -> List[dict]:
        pass