import requests
from config import config

class APIClient:
    def __init__(self, use_auth=True):
        self.base_url = config.BASE_URL
        self.api_key = config.API_KEY
        self.use_auth = use_auth

    def _headers(self):
        if self.use_auth and self.api_key:
            return {"x-lifi-api-key": self.api_key}
        return {}

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, headers=self._headers(), params=params)

    def post(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, headers=self._headers(), json=json)

# Usage:
# api_client = APIClient(use_auth=True)
# response = api_client.get("/tools")
