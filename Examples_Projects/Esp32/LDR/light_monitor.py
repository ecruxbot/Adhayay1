# light_monitor.py - MicroPython version
import time
from adhyay1_ldr import Adhyay1_LDR

# Initialize LDR sensor on GP26
ldr = Adhyay1_LDR(26)

print("Light Level Monitor")
print("Monitoring ambient light conditions...")

def get_light_level(raw_value):
    """Categorize light level based on raw value"""
    # Adjusted for MicroPython's 12-bit ADC (0-4095)
    if raw_value < 1000:
        return "Very Bright", 1
    elif raw_value < 2000:
        return "Bright", 2
    elif raw_value < 3000:
        return "Moderate", 3
    elif raw_value < 3500:
        return "Dim", 4
    else:
        return "Dark", 5

try:
    while True:
        raw_value = ldr.read_raw()
        light_level, category = get_light_level(raw_value)
        
        print("Raw: {:5d} | Level: {} | {}".format(raw_value, category, light_level))
        time.sleep(1)

except KeyboardInterrupt:
    print("\nLight monitoring stopped")