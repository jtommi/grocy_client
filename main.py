import logging
import os
import sys
from datetime import datetime

from pendulum.tz import timezone
import serial
from serial.tools import list_ports

from src.api_client import APIException
from src.grocycode import GrocyCode, InvalidGrocyCodeException
from src.ntfy import NtfyHandler
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
    # Get timezone
    tz = timezone(os.getenv("TZ", default="UTC"))
     # Configure the logger
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)-8s %(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    # Add file logger if the application is running inside a Docker container
    if os.getenv("AM_I_IN_A_DOCKER_CONTAINER", default=False):
        file_handler = logging.FileHandler(
            f"/var/log/grocy_client/{__name__}_{datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}.log"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    # Add a Ntfy handler if the server was specified
    if os.getenv("NTFY_SERVER", default=False):
        ntfy_handler = NtfyHandler()
        ntfy_formatter = logging.Formatter("%(levelname)s - %(message)s")
        ntfy_handler.setFormatter(ntfy_formatter)
        ntfy_handler.setLevel(logging.WARNING)
        logger.addHandler(ntfy_handler)

    # Get the barcode scanner device
    try:
        device = find_serial_device(os.getenv("VID_PID", ""))
    except Exception as e:
        logger.exception(str(e))
        raise e

    with serial.Serial(device, 19200, timeout=0) as ser:
        logger.info("App started, watiting for barcode input")
        while True:
            barcode = ser.readline()
            barcode = barcode.strip()
            if len(barcode) > 0:
                try:
                    grocycode = GrocyCode(barcode.decode())
                    product: Product = grocycode.get_product()
                    product.open_or_consume()
                except (
                    InvalidGrocyCodeException,
                    NoStockEntriesException,
                    ProductNotExistsException,
                ) as e:
                    logger.warning(str(e))
                except APIException as e:
                    logger.debug("Stacktrace", exc_info=True)
                    logger.exception(str(e))


if __name__ == "__main__":
    main()
