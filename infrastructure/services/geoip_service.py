from typing import Optional
import geoip2.database
import geoip2.errors
from infrastructure.config import get_environment_variable

env = get_environment_variable()

class GeoIPService:
    def __init__(self):
        self.__reader = None
        try:
            # Tenta carregar o banco de dados GeoIP
            if hasattr(env, 'GEOIP_DATABASE_PATH') and env.GEOIP_DATABASE_PATH:
                self.__reader = geoip2.database.Reader(env.GEOIP_DATABASE_PATH)
        except Exception as e:
            print(f"GeoIP database não disponível: {e}")
    
    def get_location(self, ip_address: str) -> dict:
        """
        Retorna informações de localização baseado no IP.
        Retorna dict com country, city, latitude, longitude.
        """
        if not self.__reader:
            return {
                "country": None,
                "city": None,
                "latitude": None,
                "longitude": None
            }
        
        try:
            # IPs locais/privados não têm geolocalização
            if self._is_private_ip(ip_address):
                return {
                    "country": "Local",
                    "city": "Local",
                    "latitude": None,
                    "longitude": None
                }
            
            response = self.__reader.city(ip_address)
            
            return {
                "country": response.country.name if response.country.name else None,
                "city": response.city.name if response.city.name else None,
                "latitude": response.location.latitude if response.location.latitude else None,
                "longitude": response.location.longitude if response.location.longitude else None
            }
        except geoip2.errors.AddressNotFoundError:
            return {
                "country": "Unknown",
                "city": None,
                "latitude": None,
                "longitude": None
            }
        except Exception as e:
            print(f"Erro ao buscar geolocalização: {e}")
            return {
                "country": None,
                "city": None,
                "latitude": None,
                "longitude": None
            }
    
    def _is_private_ip(self, ip: str) -> bool:
        """Verifica se o IP é privado/local"""
        private_ranges = [
            "127.",
            "10.",
            "172.16.", "172.17.", "172.18.", "172.19.",
            "172.20.", "172.21.", "172.22.", "172.23.",
            "172.24.", "172.25.", "172.26.", "172.27.",
            "172.28.", "172.29.", "172.30.", "172.31.",
            "192.168.",
            "localhost",
            "::1"
        ]
        return any(ip.startswith(prefix) for prefix in private_ranges)
    
    def __del__(self):
        """Fecha o reader ao destruir o objeto"""
        if self.__reader:
            self.__reader.close()
