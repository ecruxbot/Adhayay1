# light_trigger.py - MicroPython version
import time
from adhyay1_ldr import Adhyay1_LDR

# Initialize LDR sensor on GP26
ldr = Adhyay1_LDR(26)

print("Light Trigger System")
print("Detecting sudden light changes")
print("Cover and uncover the LDR to test")

# Calibration - get initial light level
print("Calibrating... please keep normal light condition")
time.sleep(2)
initial_value = ldr.read_raw()
print("Calibrated baseline:", initial_value)

# Set change threshold (20% change)
CHANGE_THRESHOLD = initial_value * 0.2

try:
    while True:
        current_value = ldr.read_raw()
        change = abs(current_value - initial_value)
        
        print("Current: {:5d} | Change: {:5.0f}".format(current_value, change), end=" ")
        
        if change > CHANGE_THRESHOLD:
            if current_value > initial_value:
                print("-> Light DECREASED (darker)")
            else:
                print("-> Light INCREASED (brighter)")
        else:
            print("-> Light stable")
        
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nLight trigger system stopped")