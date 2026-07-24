# simple_read.py - MicroPython version
import time
from adhyay1_irarray import Adhyay1_IRSensor

# Initialize 5-channel IR array
ir_pins = [9, 10, 11, 12, 13]  # GP9, GP10, GP11, GP12, GP13
ir = Adhyay1_IRSensor(ir_pins)

print("Simple IR Array Reading")
print("Sensor values: [L2, L1, C, R1, R2]")
print("1 = White surface, 0 = Black line/cliff")
print("Press Ctrl+C to stop")

try:
    while True:
        values = ir.read_all()
        print("IR Sensors:", values)
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nIR reading stopped")