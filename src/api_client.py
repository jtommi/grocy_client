import os

import requests


class APIException(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return self.message


class ApiClient:
    def __init__(self, api_url: str | None = None, api_key: str | None = None) -> None:
        self.api_url: str = api_url if api_url else os.getenv("API_URL")  # type: ignore
        self.api_key: str = api_key if api_key else os.getenv("API_KEY")  # type: ignore
        if not self.api_key or not self.api_url:
            raise ValueError("API_URL and/or API_KEY is not set")

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
