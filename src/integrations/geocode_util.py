import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LOCATIONIQ_API_KEY")


class _GeocodeClient:
    BASE_URL = "https://us1.locationiq.com/v1/search"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def fetch(self, address: str) -> dict | None:

        params = {
            "key": self.api_key,
            "q": address,
            "format": "json",
            "limit": 1
        }

        response = self.session.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data:
            return None

        top = data[0]

        return {
            "full_address": top.get("display_name"),
            "latitude": float(top.get("lat")),
            "longitude": float(top.get("lon"))
        }


# REQUIRED FUNCTION
def get_structured_address(partial_address: str):
    """
    Given a partial address, returns the full structured address using LocationIQ API.
    """
    if not partial_address:
        return None

    client = _GeocodeClient(API_KEY)

    return client.fetch(partial_address)