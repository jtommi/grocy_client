# Grocy client

This project is intended to be a headless client for Grocy

In the day to day operations in your kitchen, you don't want to whip out your phone each time you open or consume and item.  
Instead you want easy, straight forward handling.

So this client is designed to take input from a barcode scanenr over a serial port and handle the product based on context:  

- If the item is currently "closed", the client will ask Grocy to "open" it
- If on the otherhand the item is already "open", the client will ask Grocy to "consume" it

## Setup with docker

(tested on RPi 3)µ

1. Install docker
1. Find the /dev file for your barcode scanner (e.g. /dev/ttyACM0)
1. Update /etc/udev/rules.d/99-com.rules to mount the device with permissions 666 (KERNEL=="ttyACM0", MODE="0666")
1. Define the different variables in the .env file
    - VID_PID (VID:PID of the barcode scanner)
    - API_URL (Base URL of the Grocy instance)
    - API_KEY (Grocy API key)
    - TZ (optional, default: UTC)
    - NTFY_SERVER (optional)
    - NTFY_TOPIC (optional)
