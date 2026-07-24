# simple_read.py - MicroPython version
import time
from adhyay1_ldr import Adhyay1_LDR

# Initialize LDR sensor on GP26
ldr = Adhyay1_LDR(26)

print("Simple LDR Reading")
print("Raw value (0-4095), Higher value = Darker")
print("Press Ctrl+C to stop")

try:
    while True:
        raw_value = ldr.read_raw()
        voltage = ldr.read_voltage()
        
        print("Raw: {:5d} | Voltage: {:.2f}V".format(raw_value, voltage))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nLDR reading stopped")