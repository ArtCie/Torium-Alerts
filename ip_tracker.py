import requests


class IpTracker:
    @staticmethod
    def get_location(ip_address):
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        return {
            "ip": ip_address,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }