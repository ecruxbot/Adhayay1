import board
import time
from adhyay1_bluetooth import Adhyay1_Bluetooth

# Initialize Bluetooth on GP0 (TX) and GP1 (RX)
bt = Adhyay1_Bluetooth(board.GP0, board.GP1)

print("Simple Bluetooth Receiver")
print("Waiting for data from Bluetooth...")
print("Connect to your Pico via Bluetooth serial")
print("Press Ctrl+C to stop")

try:
    while True:
        data = bt.read()
        if data:
            print(f"Received: {data}")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nBluetooth receiver stopped")
