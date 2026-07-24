import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_bluetooth import Adhyay1_Bluetooth

# Initialize Bluetooth
bt = Adhyay1_Bluetooth(board.GP0, board.GP1)

print("Bluetooth Command Processor")
print("Available commands:")
print("LED ON, LED OFF, BEEP, STATUS, HELP")
print("Waiting for commands...")

def process_command(command):
    """Process Bluetooth commands"""
    command = command.upper().strip()
    
    if command == "LED ON":
        return "✅ LED turned ON"
    elif command == "LED OFF":
        return "✅ LED turned OFF"
    elif command == "BEEP":
        return "🔊 Beep sound played"
    elif command == "STATUS":
        return "📊 System status: OK"
    elif command == "HELP":
        return "📖 Commands: LED ON, LED OFF, BEEP, STATUS, HELP"
    else:
        return f"❌ Unknown command: {command}"

try:
    while True:
        data = bt.read()
        if data:
            print(f"Command received: {data}")
            response = process_command(data)
            print(f"Response: {response}")
            bt.write(response)  # Send response back
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCommand processor stopped")
