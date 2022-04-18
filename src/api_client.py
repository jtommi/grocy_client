import os

import requests


class ApiClient:
    def __init__(
        self, api_url: str = os.getenv("API_URL"), api_key: str = os.getenv("API_KEY")
    ) -> None:
        self.api_url = api_url
        self.api_key = api_key

    def get(self, path: str) -> dict:
        response = requests.get(
            url=f"{self.api_url}{path}", headers={"GROCY-API-KEY": self.api_key}
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        return response.json()
