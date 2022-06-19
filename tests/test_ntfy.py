import unittest
from unittest.mock import MagicMock, patch

from src.ntfy import NtfyClient

SERVER = "localhost:8080"
TOPIC = "test"


def mock_getenv(key: str) -> str:
    if key == "NTFY_SERVER":
        return SERVER
    elif key == "NTFY_TOPIC":
        return TOPIC


class TestNtfy(unittest.TestCase):
    @patch("src.ntfy.requests.post")
    @patch("src.ntfy.os.getenv", side_effect=mock_getenv)
    def test_correct_config_through_env(self, mock_getenv, mock_post):

        mock_post.return_value = MagicMock(status_code=200, json=lambda: {})

        ntfy = NtfyClient()
        ntfy.send_message("")

        mock_post.assert_called
        self.assertEqual(mock_post.call_args.kwargs["url"], f"http://{SERVER}/{TOPIC}")

    @patch("src.ntfy.requests.post")
    @patch("src.ntfy.os.getenv", side_effect=mock_getenv)
    def test_send_message(self, mock_getenv, mock_post):
        message = "Hello World"

        ntfy = NtfyClient()
        ntfy.send_message(message)

        mock_post.assert_called
        self.assertEqual(mock_post.call_args.kwargs["data"], message)

    @patch("src.ntfy.os.getenv")
    def test_raises_on_missing_config(self, mock_getenv):
        mock_getenv.return_value = None

        with self.assertRaises(ValueError):
            NtfyClient()
        with self.assertRaises(ValueError):
            NtfyClient(server=SERVER)
        with self.assertRaises(ValueError):
            NtfyClient(topic=TOPIC)

    def test_not_raises_with_params(self):
        NtfyClient(server=SERVER, topic=TOPIC)
