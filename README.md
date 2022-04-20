# Grocy client

This project is intended to be a headless client for Grocy

In the day to day operations in your kitchen, you don't want to whip out your phone each time you open or consume and item.  
Instead you want easy, straight forward handling.

So this client is designed to take input from a barcode scanenr over a serial port and handle the product based on context:  

- If the item is currently "closed", the client will ask Grocy to "open" it
- If on the otherhand the item is already "open", the client will ask Grocy to "consume" it
