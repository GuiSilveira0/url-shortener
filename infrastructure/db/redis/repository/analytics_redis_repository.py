from datetime import datetime
from redis.exceptions import RedisError
from app.gateway.analytics_redis_repository_gateway import AnalyticsRedisRepositoryGateway
from infrastructure.db.redis.settings.connection import RedisConnectionHandler

class AnalyticsRedisRepository(AnalyticsRedisRepositoryGateway):
    def __init__(self):
        self.__redis_handler = RedisConnectionHandler()
        self.__ttl = 604800  # 7 dias em segundos
    
    def increment_total_clicks(self, short_code: str) -> int:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:total_clicks"
                count = redis_conn.incr(key)
                redis_conn.expire(key, self.__ttl)
                return count
        except RedisError as e:
            raise Exception(f"Erro ao incrementar total de cliques: {str(e)}")
    
    def add_unique_ip(self, short_code: str, ip: str) -> bool:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:unique_ips"
                is_new = redis_conn.sadd(key, ip)
                redis_conn.expire(key, self.__ttl)
                return bool(is_new)
        except RedisError as e:
            raise Exception(f"Erro ao adicionar IP único: {str(e)}")
    
    def increment_daily_clicks(self, short_code: str, date: str) -> int:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:clicks:daily:{date}"
                count = redis_conn.incr(key)
                redis_conn.expire(key, self.__ttl)
                return count
        except RedisError as e:
            raise Exception(f"Erro ao incrementar cliques diários: {str(e)}")
    
    def increment_hourly_clicks(self, short_code: str, hour: str) -> int:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:clicks:hourly:{hour}"
                count = redis_conn.incr(key)
                redis_conn.expire(key, self.__ttl)
                return count
        except RedisError as e:
            raise Exception(f"Erro ao incrementar cliques por hora: {str(e)}")
    
    def increment_country_clicks(self, short_code: str, country: str) -> int:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:countries"
                count = redis_conn.hincrby(key, country, 1)
                redis_conn.expire(key, self.__ttl)
                return count
        except RedisError as e:
            raise Exception(f"Erro ao incrementar cliques por país: {str(e)}")
    
    def increment_device_clicks(self, short_code: str, device: str) -> int:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:devices"
                count = redis_conn.hincrby(key, device, 1)
                redis_conn.expire(key, self.__ttl)
                return count
        except RedisError as e:
            raise Exception(f"Erro ao incrementar cliques por dispositivo: {str(e)}")
    
    def increment_browser_clicks(self, short_code: str, browser: str) -> int:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:browsers"
                count = redis_conn.hincrby(key, browser, 1)
                redis_conn.expire(key, self.__ttl)
                return count
        except RedisError as e:
            raise Exception(f"Erro ao incrementar cliques por navegador: {str(e)}")
    
    def get_realtime_stats(self, short_code: str) -> dict:
        try:
            with self.__redis_handler as redis_conn:
                total_clicks = redis_conn.get(f"stats:{short_code}:total_clicks") or 0
                unique_ips = redis_conn.scard(f"stats:{short_code}:unique_ips") or 0
                
                countries = redis_conn.hgetall(f"stats:{short_code}:countries") or {}
                devices = redis_conn.hgetall(f"stats:{short_code}:devices") or {}
                browsers = redis_conn.hgetall(f"stats:{short_code}:browsers") or {}
                
                today = datetime.now().date()
                daily_clicks = {}
                for i in range(7):
                    date_key = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                    clicks = redis_conn.get(f"stats:{short_code}:clicks:daily:{date_key}") or 0
                    daily_clicks[date_key] = int(clicks)
                
                return {
                    "short_code": short_code,
                    "total_clicks": int(total_clicks),
                    "unique_visitors": int(unique_ips),
                    "countries": {k: int(v) for k, v in countries.items()},
                    "devices": {k: int(v) for k, v in devices.items()},
                    "browsers": {k: int(v) for k, v in browsers.items()},
                    "daily_clicks": daily_clicks
                }
        except RedisError as e:
            raise Exception(f"Erro ao buscar estatísticas em tempo real: {str(e)}")
    
    def get_unique_visitors_count(self, short_code: str) -> int:
        try:
            with self.__redis_handler as redis_conn:
                key = f"stats:{short_code}:unique_ips"
                return redis_conn.scard(key) or 0
        except RedisError as e:
            raise Exception(f"Erro ao buscar visitantes únicos: {str(e)}")
    
    def clear_stats(self, short_code: str) -> bool:
        try:
            with self.__redis_handler as redis_conn:
                keys_pattern = f"stats:{short_code}:*"
                keys = redis_conn.keys(keys_pattern)
                if keys:
                    redis_conn.delete(*keys)
                return True
        except RedisError as e:
            raise Exception(f"Erro ao limpar estatísticas: {str(e)}")
