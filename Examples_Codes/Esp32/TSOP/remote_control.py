# remote_control.py - MicroPython version
import time
from adhyay1_tsop import IRRemote

# Initialize TSOP IR receiver on GP20
tsop = IRRemote(20)

# Define your remote button codes (you need to get these from your remote)
# Example codes for common NEC remotes - replace with your actual remote codes
BUTTON_CODES = {
    (0x00, 0xFF, 0x00, 0xFF): "POWER",
    (0x00, 0xFF, 0x80, 0x7F): "VOLUME_UP",
    (0x00, 0xFF, 0x40, 0xBF): "VOLUME_DOWN",
    (0x00, 0xFF, 0x20, 0xDF): "CHANNEL_UP",
    (0x00, 0xFF, 0xA0, 0x5F): "CHANNEL_DOWN",
    (0x00, 0xFF, 0x60, 0x9F): "MENU",
    (0x00, 0xFF, 0x10, 0xEF): "OK",
    (0x00, 0xFF, 0x90, 0x6F): "UP",
    (0x00, 0xFF, 0x50, 0xAF): "DOWN",
    (0x00, 0xFF, 0x30, 0xCF): "LEFT",
    (0x00, 0xFF, 0xB0, 0x4F): "RIGHT"
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
            print("Button pressed:", button)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nRemote control demo stopped")