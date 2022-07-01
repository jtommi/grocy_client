import logging
import os

import requests


class NtfyClient:
    def __init__(self, server: str | None = None, topic: str | None = None) -> None:
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


class NtfyHandler(logging.StreamHandler):
    def __init__(self, server=None, topic=None):
        logging.StreamHandler.__init__(self)
        self.server = server
        self.topic = topic

        self.ntfy_client = NtfyClient(server=server, topic=topic)

    def emit(self, record):
        msg = self.format(record)
        self.ntfy_client.send_message(msg)
