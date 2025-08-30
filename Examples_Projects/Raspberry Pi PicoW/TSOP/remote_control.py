import board
import time
from adhyay1_tsop import IRRemote

# Initialize TSOP IR receiver on GP20
tsop = IRRemote(board.GP20)

# Define your remote button codes (you need to get these from your remote)
# Example codes - replace with your actual remote codes
BUTTON_CODES = {
    (255, 0, 255, 0): "POWER",
    (255, 0, 0, 255): "VOLUME_UP",
    (0, 255, 255, 0): "VOLUME_DOWN",
    (0, 255, 0, 255): "CHANNEL_UP",
    (255, 255, 0, 0): "CHANNEL_DOWN",
    (0, 0, 255, 255): "MENU",
    (255, 255, 255, 0): "OK",
    (0, 0, 0, 255): "UP",
    (255, 0, 0, 0): "DOWN",
    (0, 255, 0, 0): "LEFT",
    (0, 0, 255, 0): "RIGHT"
}

# Set the button codes mapping
tsop.set_button_codes(BUTTON_CODES)

print("Remote Control Demo")
print("Press buttons on your IR remote")
print("Press Ctrl+C to stop")

try:
    while True:
        button = tsop.get_button()
        if button and button != "Unknown":
            print(f"Button pressed: {button}")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nRemote control demo stopped")
