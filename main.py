import serial
from serial.tools import list_ports
from serial.serialutil import SerialException
from time import sleep

VID_PID = "080C:0400"


def main():
    """
    Main function
    """
    ports = list_ports.grep(VID_PID)
    device = list(ports)[0].device

    with serial.Serial(device, 19200, timeout=0) as ser:
        while True:
            try:
                line = ser.readline()
            except SerialException as e:
                print("It happened")
                raise e
            else:
                line = line.strip()
                if len(line) > 0:
                    print(line)
                sleep(0.1)


if __name__ == "__main__":
    main()
