from datetime import datetime, date, timedelta
from typing import Optional, List
from app.gateway.analytics_repository_gateway import AnalyticsRepositoryGateway
from app.gateway.analytics_redis_repository_gateway import AnalyticsRedisRepositoryGateway

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
            
        except Exception as e:
            raise Exception(f"Erro ao processar tracking: {str(e)}")
    
    def get_url_statistics(self, short_code: str) -> dict:
        try:
            summary = self.__analytics_repository.get_stats_summary(short_code)
            
            if not summary:
                return {
                    "short_code": short_code,
                    "total_clicks": 0,
                    "unique_clicks": 0,
                    "first_access": None,
                    "last_access": None
                }
            
            return summary
            
        except Exception as e:
            raise Exception(f"Erro ao buscar estatísticas: {str(e)}")
    
    def get_detailed_analytics(self, short_code: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> dict:
        try:
            if not end_date:
                end_date = date.today()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            summary = self.__analytics_repository.get_stats_summary(short_code)
            clicks_by_period = self.__analytics_repository.get_clicks_by_period(short_code, start_date, end_date)
            top_countries = self.__analytics_repository.get_top_countries(short_code, limit=10)
            device_distribution = self.__analytics_repository.get_device_distribution(short_code)
            browser_distribution = self.__analytics_repository.get_browser_distribution(short_code)
            top_referrers = self.__analytics_repository.get_top_referrers(short_code, limit=10)
            
            return {
                "short_code": short_code,
                "summary": summary or {},
                "clicks_by_period": clicks_by_period,
                "top_countries": top_countries,
                "device_distribution": device_distribution,
                "browser_distribution": browser_distribution,
                "top_referrers": top_referrers,
                "period": {
                    "start_date": str(start_date),
                    "end_date": str(end_date)
                }
            }
            
        except Exception as e:
            raise Exception(f"Erro ao buscar analytics detalhado: {str(e)}")
    
    def get_realtime_stats(self, short_code: str) -> dict:
        try:
            return self.__analytics_redis_repository.get_realtime_stats(short_code)
        except Exception as e:
            raise Exception(f"Erro ao buscar estatísticas em tempo real: {str(e)}")
    
    def export_analytics_report(self, short_code: str, format: str = "json") -> dict:
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=90)
            
            detailed_analytics = self.get_detailed_analytics(short_code, start_date, end_date)
            
            if format == "json":
                return detailed_analytics
            elif format == "csv":
                # TODO: Implementar conversão para CSV
                raise NotImplementedError("Formato CSV ainda não implementado")
            else:
                raise ValueError(f"Formato não suportado: {format}")
                
        except Exception as e:
            raise Exception(f"Erro ao exportar relatório: {str(e)}")
