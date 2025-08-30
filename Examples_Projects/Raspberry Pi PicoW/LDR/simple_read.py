import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_ldr import Adhyay1_LDR

# Initialize LDR sensor on GP26
ldr = Adhyay1_LDR(board.GP26)

print("Simple LDR Reading")
print("Raw value (0-65535), Higher value = Darker")
print("Press Ctrl+C to stop")

try:
    while True:
        raw_value = ldr.read_raw()
        voltage = ldr.read_voltage()
        
        print(f"📊 Raw: {raw_value:>5d} | ⚡ Voltage: {voltage:.2f}V")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nLDR reading stopped")
