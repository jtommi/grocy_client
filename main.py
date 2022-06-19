import logging
import os
import sys

import serial
from serial.tools import list_ports

from src.api_client import APIException
from src.grocycode import GrocyCode, InvalidGrocyCodeException
from src.ntfy import NtfyClient
from src.product import NoStockEntriesException, Product, ProductNotExistsException

VID_PID = os.getenv("VID_PID", "")


def find_barcode_scanner(vid_pid: str):
    """
    Find barcode scanner
    """
    ports = list_ports.grep(vid_pid)
    device = list(ports)[0]
    if not device:
        raise ValueError("Barcode scanner not found")

    return device.device


def main():
    """
    Main function
    """
    device = find_barcode_scanner(VID_PID)

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
