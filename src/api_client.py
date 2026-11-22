import requests
from datetime import datetime, timezone

BASE_URL = "https://ips.alexgallax-edu.ru/api/v1"

class PumpApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def send_glucose(self, pump_id: str, glucose_value: float):
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        payload = {
            "glucose_value": glucose_value,
            "glucose_unit": "mmol/L",
            "timestamp": timestamp
        }
        return self.session.post(f"{self.base_url}/pumps/{pump_id}/telemetry", json=payload)