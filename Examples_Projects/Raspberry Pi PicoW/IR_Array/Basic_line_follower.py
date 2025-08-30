import board
import time
from adhyay1_irarray import Adhyay1_IRSensor

# Initialize 5-channel IR array
ir_pins = [board.GP9, board.GP10, board.GP11, board.GP12, board.GP13]
ir = Adhyay1_IRSensor(ir_pins)

print("Line Follower Simulation")
print("Sensor pattern: [L2, L1, C, R1, R2]")
print("Following black line on white surface")

def get_line_position(values):
    """Determine line position from sensor values"""
    # 1 = white surface, 0 = black line
    if values == [1, 1, 0, 1, 1]:    # Only center on line
        return "CENTER"
    elif values == [1, 0, 0, 1, 1]:  # Left sensors on line
        return "LEFT1"
    elif values == [0, 0, 1, 1, 1]:  # Far left on line
        return "LEFT2"
    elif values == [1, 1, 0, 0, 1]:  # Right sensors on line
        return "RIGHT1"
    elif values == [1, 1, 1, 0, 0]:  # Far right on line
        return "RIGHT2"
    elif values == [0, 0, 0, 0, 0]:  # All on black
        return "ALL BLACK"
    elif values == [1, 1, 1, 1, 1]:  # All on white
        return "ALL WHITE"
    else:
        return "COMPLEX"

try:
    while True:
        values = ir.read_all()
        position = get_line_position(values)
        
        print(f"Sensors: {values} -> {position}")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nLine follower stopped")
