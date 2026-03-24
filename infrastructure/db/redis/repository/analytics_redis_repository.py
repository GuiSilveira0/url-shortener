import json
from typing import Optional

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
                total_clicks = redis_conn.get(f"stats:{short_code}:total_clicks")
                unique_ips = redis_conn.scard(f"stats:{short_code}:unique_ips")
                countries = redis_conn.hgetall(f"stats:{short_code}:countries")
                devices = redis_conn.hgetall(f"stats:{short_code}:devices")
                browsers = redis_conn.hgetall(f"stats:{short_code}:browsers")

                return {
                    "total_clicks": int(total_clicks) if total_clicks else 0,
                    "unique_clicks": unique_ips or 0,
                    "countries": {k: int(v) for k, v in countries.items()} if countries else {},
                    "devices": {k: int(v) for k, v in devices.items()} if devices else {},
                    "browsers": {k: int(v) for k, v in browsers.items()} if browsers else {}
                }
        except RedisError as e:
            raise Exception(f"Erro ao buscar stats em tempo real: {str(e)}")

    def get_cached_stats(self, cache_key: str) -> Optional[dict]:
        try:
            with self.__redis_handler as redis_conn:
                data = redis_conn.get(cache_key)
                if data:
                    return json.loads(data)
                return None
        except RedisError as e:
            raise Exception(f"Erro ao buscar cache: {str(e)}")

    def set_cached_stats(self, cache_key: str, data: dict, ttl: int = 60) -> None:
        try:
            with self.__redis_handler as redis_conn:
                redis_conn.setex(cache_key, ttl, json.dumps(data))
        except RedisError as e:
            raise Exception(f"Erro ao salvar cache: {str(e)}")

    def invalidate_cache(self, short_code: str) -> None:
        try:
            with self.__redis_handler as redis_conn:
                keys = redis_conn.keys(f"cache:stats:{short_code}:*")
                if keys:
                    redis_conn.delete(*keys)
        except RedisError as e:
            raise Exception(f"Erro ao invalidar cache: {str(e)}")