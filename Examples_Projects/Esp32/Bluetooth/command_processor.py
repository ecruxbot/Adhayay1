# command_processor.py - MicroPython version
from machine import Pin
import time
from adhyay1_bluetooth import Adhyay1_Bluetooth

# Initialize Bluetooth
bt = Adhyay1_Bluetooth(tx_pin=Pin(0), rx_pin=Pin(1))

print("Bluetooth Command Processor")
print("Available commands:")
print("LED ON, LED OFF, BEEP, STATUS, HELP")
print("Waiting for commands...")

def process_command(command):
    """Process Bluetooth commands"""
    command = command.upper().strip()
    
    if command == "LED ON":
        return "LED turned ON"
    elif command == "LED OFF":
        return "LED turned OFF"
    elif command == "BEEP":
        return "Beep sound played"
    elif command == "STATUS":
        return "System status: OK"
    elif command == "HELP":
        return "Commands: LED ON, LED OFF, BEEP, STATUS, HELP"
    else:
        return "Unknown command: " + command

try:
    while True:
        data = bt.read()
        if data:
            print("Command received:", data)
            response = process_command(data)
            print("Response:", response)
            bt.write(response)  # Send response back
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCommand processor stopped")