import logging
import os
import sys

import serial
from serial.tools import list_ports

from src.api_client import APIException
from src.grocycode import GrocyCode, InvalidGrocyCodeException
from src.ntfy import NtfyClient
from src.product import NoStockEntriesException, Product, ProductNotExistsException


class SerialDeviceNotFoundException(Exception):
    """
    Exception raised when serial device is not found
    """

    pass


def find_serial_device(vid_pid: str):
    """
    Find serial device
    """
    ports = list(list_ports.grep(vid_pid))
    try:
        vid, pid = vid_pid.split(":")
        # Convert vid and pid to integers to match the output of list_ports
        vid = int("0x" + vid, 16)
        pid = int("0x" + pid, 16)
    except ValueError as e:
        if str(e).startswith("too many values to unpack") or str(e).startswith(
            "not enough values to unpack"
        ):
            raise ValueError(
                f'vid_pid must be in the format VID:PID. Provided was "{vid_pid}"'
            ) from None
        elif str(e).startswith("invalid literal for int() with base 16"):
            raise ValueError(
                f'VID or PID is not in hexadecimal format. VID:PID provided was "{vid_pid}"'
            ) from None
        else:
            raise

    for port in ports:
        if port.vid == vid and port.pid == pid:
            return port.device

    raise SerialDeviceNotFoundException(f"Serial device {vid_pid} not found")


def main():
    """
    Main function
    """
    device = find_serial_device(os.getenv("VID_PID", ""))

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s [%(name)] %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)

    ntfy = NtfyClient()

    with serial.Serial(device, 19200, timeout=0) as ser:
        while True:
            barcode = ser.readline()
            barcode = barcode.strip()
            if len(barcode) > 0:
                try:
                    grocycode = GrocyCode(barcode)
                    product: Product = grocycode.get_item()
                    product.open_or_consume()
                except (
                    InvalidGrocyCodeException,
                    NoStockEntriesException,
                    ProductNotExistsException,
                ) as e:
                    logger.warning(str(e))
                    ntfy.send_message(str(e))
                except APIException as e:
                    logger.exception(str(e))
                    ntfy.send_message(f"Unhandled API exception: {str(e)}")


if __name__ == "__main__":
    main()
