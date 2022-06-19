import logging
import os

import requests


class NtfyClient:
    def __init__(self, server: str = None, topic: str = None) -> None:
        self.server = server if server else os.getenv("NTFY_SERVER")
        self.topic = topic if topic else os.getenv("NTFY_TOPIC")
        if not self.server:
            raise ValueError("NTFY_SERVER is not set")
        if not self.topic:
            raise ValueError("NTFY_TOPIC is not set")

        if not self.server.startswith("http"):
            self.server = f"http://{self.server}"

    def send_message(self, message: str) -> None:
        response = requests.post(url=f"{self.server}/{self.topic}", data=message)
        if response.status_code != 200:
            logging.error(response.json())
