import os

import requests


class APIException(Exception):
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code


class ApiClient:
    def __init__(self, api_url: str = None, api_key: str = None) -> None:
        self.api_url = api_url if api_url else os.getenv("API_URL")
        self.api_key = api_key if api_key else os.getenv("API_KEY")

    def get(self, path: str) -> dict:
        response = requests.get(
            url=f"{self.api_url}{path}", headers={"GROCY-API-KEY": self.api_key}
        )
        if response.status_code != 200:
            raise APIException(
                message=response.json()["error_message"],
                status_code=response.status_code,
            )

        return response.json()

    def post(self, path: str, data: dict) -> dict:
        response = requests.post(
            url=f"{self.api_url}{path}",
            json=data,
            headers={"GROCY-API-KEY": self.api_key},
        )
        if response.status_code != 200:
            raise APIException(
                message=response.json()["error_message"],
                status_code=response.status_code,
            )

        return response.json()
