from typing import Optional

from app.gateway.analytics_repository_gateway import AnalyticsRepositoryGateway
from app.gateway.analytics_redis_repository_gateway import AnalyticsRedisRepositoryGateway


CACHE_TTL = 60  # segundos


class AnalyticsUsecase:
    def __init__(
        self,
        analytics_repository: AnalyticsRepositoryGateway,
        analytics_redis_repository: AnalyticsRedisRepositoryGateway
    ):
        self.__analytics_repository = analytics_repository
        self.__analytics_redis_repository = analytics_redis_repository
    
    def track_access(self, analytics_data: dict) -> None:
        try:
            short_code = analytics_data["short_code"]
            
            self.__analytics_redis_repository.increment_total_clicks(short_code)
            self.__analytics_redis_repository.add_unique_ip(short_code, analytics_data["ip_address"])
            
            date_str = analytics_data["accessed_at"].strftime("%Y-%m-%d")
            self.__analytics_redis_repository.increment_daily_clicks(short_code, date_str)
            
            hour_str = analytics_data["accessed_at"].strftime("%Y-%m-%d-%H")
            self.__analytics_redis_repository.increment_hourly_clicks(short_code, hour_str)
            
            if analytics_data.get("country"):
                self.__analytics_redis_repository.increment_country_clicks(short_code, analytics_data["country"])
            
            if analytics_data.get("device_type"):
                self.__analytics_redis_repository.increment_device_clicks(short_code, analytics_data["device_type"])
            
            if analytics_data.get("browser"):
                self.__analytics_redis_repository.increment_browser_clicks(short_code, analytics_data["browser"])
            
            self.__analytics_repository.insert_analytics(analytics_data)

            self.__analytics_redis_repository.invalidate_cache(short_code)
            
        except Exception as e:
            raise Exception(f"Erro ao processar tracking: {str(e)}")

    def get_url_statistics(self, short_code: str) -> Optional[dict]:
        cache_key = f"cache:stats:{short_code}:summary"
        cached = self.__analytics_redis_repository.get_cached_stats(cache_key)
        if cached:
            return cached

        stats = self.__analytics_repository.get_stats_summary(short_code)
        if not stats:
            return None

        stats["top_countries"] = self.__analytics_repository.get_top_countries(short_code)
        stats["top_devices"] = self.__analytics_repository.get_device_distribution(short_code)
        stats["top_browsers"] = self.__analytics_repository.get_browser_distribution(short_code)

        self.__analytics_redis_repository.set_cached_stats(cache_key, stats, CACHE_TTL)
        return stats

    def get_detailed_analytics(self, short_code: str, start_date: str, end_date: str) -> Optional[dict]:
        cache_key = f"cache:stats:{short_code}:detailed:{start_date}:{end_date}"
        cached = self.__analytics_redis_repository.get_cached_stats(cache_key)
        if cached:
            return cached

        stats = self.__analytics_repository.get_stats_summary(short_code)
        if not stats:
            return None

        result = {
            "total_clicks": stats["total_clicks"],
            "unique_clicks": stats["unique_clicks"],
            "clicks_by_day": self.__analytics_repository.get_clicks_by_period(short_code, start_date, end_date),
            "top_countries": self.__analytics_repository.get_top_countries(short_code),
            "top_devices": self.__analytics_repository.get_device_distribution(short_code),
            "top_browsers": self.__analytics_repository.get_browser_distribution(short_code)
        }

        self.__analytics_redis_repository.set_cached_stats(cache_key, result, CACHE_TTL)
        return result

    def get_realtime_stats(self, short_code: str) -> dict:
        return self.__analytics_redis_repository.get_realtime_stats(short_code)