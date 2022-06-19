import os

import serial
from serial.tools import list_ports

from src.grocycode import GrocyCode
from src.product import Product

VID_PID = os.getenv("VID_PID")


def find_barcode_scanner(vid_pid: str):
    """
    Find barcode scanner
    """
    ports = list_ports.grep(vid_pid)
    device = list(ports)[0]
    return device.device


def main():
    """
    Main function
    """
    device = find_barcode_scanner(VID_PID)

    with serial.Serial(device, 19200, timeout=0) as ser:
        while True:
            barcode = ser.readline()
            barcode = barcode.strip()
            if len(barcode) > 0:
                grocycode = GrocyCode(barcode)
                product: Product = grocycode.get_item()
                product.open_or_consume()


if __name__ == "__main__":
    main()
