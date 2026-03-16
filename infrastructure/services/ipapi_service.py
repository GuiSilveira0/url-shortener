import requests

class IPAPIService:
    def __init__(self):
        self.__base_url = "https://ipapi.co"
    
    def get_location(self, ip_address: str) -> dict:
        try:
            if self._is_private_ip(ip_address):
                return {"country": "Local", "city": "Local", "latitude": None, "longitude": None}
            
            response = requests.get(f"{self.__base_url}/{ip_address}/json/", timeout=2)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "country": data.get("country_name"),
                    "city": data.get("city"),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude")
                }
            
            return {"country": None, "city": None, "latitude": None, "longitude": None}
        except Exception as e:
            print(f"Erro ao buscar geolocalização via API: {e}")
            return {"country": None, "city": None, "latitude": None, "longitude": None}
    
    def _is_private_ip(self, ip: str) -> bool:
        private_ranges = ["127.", "10.", "172.16.", "172.17.", "172.18.", "172.19.",
                         "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
                         "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.",
                         "192.168.", "localhost", "::1"]
        return any(ip.startswith(prefix) for prefix in private_ranges)
