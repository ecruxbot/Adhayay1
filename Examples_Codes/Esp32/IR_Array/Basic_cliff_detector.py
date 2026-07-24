# Basic_cliff_detector.py - MicroPython version
import time
from adhyay1_irarray import Adhyay1_IRSensor

# Initialize 5-channel IR array
ir_pins = [9, 10, 11, 12, 13]  # GP9, GP10, GP11, GP12, GP13
ir = Adhyay1_IRSensor(ir_pins)

print("Cliff Detection System")
print("1 = Surface detected, 0 = Cliff (no surface)")
print("Monitoring for drop-offs...")

def check_cliff(values):
    """Check if any sensor detects a cliff"""
    # For cliff detection: 1 = surface, 0 = cliff
    if 0 in values:
        cliff_sensors = []
        for i, val in enumerate(values):
            if val == 0:
                cliff_sensors.append("Sensor" + str(i+1))
        return True, cliff_sensors
    return False, []

try:
    while True:
        values = ir.read_all()
        has_cliff, cliff_sensors = check_cliff(values)
        
        print("Sensors:", values, end=" ")
        
        if has_cliff:
            print("CLIFF DETECTED! Sensors:", ", ".join(cliff_sensors))
        else:
            print("Surface normal")
        
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nCliff detection stopped")