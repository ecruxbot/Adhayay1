# simple_receiver.py - MicroPython version
from machine import Pin
import time
from adhyay1_bluetooth import Adhyay1_Bluetooth

# Initialize Bluetooth on GP0 (TX) and GP1 (RX)
bt = Adhyay1_Bluetooth(tx_pin=Pin(0), rx_pin=Pin(1))

print("Simple Bluetooth Receiver")
print("Waiting for data from Bluetooth...")
print("Connect to your Pico via Bluetooth serial")
print("Press Ctrl+C to stop")

try:
    while True:
        data = bt.read()
        if data:
            print("Received:", data)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nBluetooth receiver stopped")