import unittest
from logging import StreamHandler
from unittest.mock import MagicMock, patch

from src.ntfy import NtfyClient, NtfyHandler

SERVER: str = "localhost:8080"
TOPIC: str = "test"


def mock_getenv(key: str) -> str:  # type: ignore
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
        mock_post.return_value = MagicMock(status_code=200)
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

    @patch("src.ntfy.requests.post")
    @patch("src.ntfy.logging.error")
    def test_logs_on_error(self, mock_error, mock_post):
        mock_post.return_value = MagicMock(status_code=400)

        ntfy = NtfyClient(server=SERVER, topic=TOPIC)
        ntfy.send_message("")
        mock_error.assert_called()


class TestNtfyHandler(unittest.TestCase):
    @patch("src.ntfy.NtfyClient")
    def test_client_init(self, mock_client):
        handler = NtfyHandler(server=SERVER, topic=TOPIC)
        self.assertIsInstance(handler, StreamHandler)
        mock_client.assert_called_with(server=SERVER, topic=TOPIC)

    @patch("src.ntfy.logging.StreamHandler.format")
    @patch("src.ntfy.NtfyClient.send_message")
    def test_emit_sends_message(self, mock_send_message, mock_format):
        handler = NtfyHandler(server=SERVER, topic=TOPIC)
        message = "Hello World"
        mock_format.return_value = message
        handler.emit(message)  # type: ignore
        mock_send_message.assert_called_with(message)
