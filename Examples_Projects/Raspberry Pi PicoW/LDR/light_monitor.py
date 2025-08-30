import board
import time
from adhyay1_ldr import Adhyay1_LDR

# Initialize LDR sensor on GP26
ldr = Adhyay1_LDR(board.GP26)

print("Light Level Monitor")
print("Monitoring ambient light conditions...")

def get_light_level(raw_value):
    """Categorize light level based on raw value"""
    if raw_value < 10000:
        return "☀️  Very Bright", 1
    elif raw_value < 20000:
        return "🔆 Bright", 2
    elif raw_value < 30000:
        return "🌤️  Moderate", 3
    elif raw_value < 40000:
        return "🌙 Dim", 4
    else:
        return "🌑 Dark", 5

try:
    while True:
        raw_value = ldr.read_raw()
        light_level, category = get_light_level(raw_value)
        
        print(f"Raw: {raw_value:>5d} | Level: {category} | {light_level}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nLight monitoring stopped")
