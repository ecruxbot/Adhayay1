import board
import time
from adhyay1_irarray import Adhyay1_IRSensor

# Initialize 5-channel IR array
ir_pins = [board.GP9, board.GP10, board.GP11, board.GP12, board.GP13]
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
                cliff_sensors.append(f"Sensor{i+1}")
        return True, cliff_sensors
    return False, []

try:
    while True:
        values = ir.read_all()
        has_cliff, cliff_sensors = check_cliff(values)
        
        print(f"Sensors: {values}", end=" ")
        
        if has_cliff:
            print(f"🚨 CLIFF DETECTED! Sensors: {', '.join(cliff_sensors)}")
        else:
            print("✅ Surface normal")
        
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nCliff detection stopped")
