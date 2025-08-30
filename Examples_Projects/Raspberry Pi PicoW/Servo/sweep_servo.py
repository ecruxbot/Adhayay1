import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_servo import Adhyay1_Servo

# Initialize servo on GP26
servo = Adhyay1_Servo(board.GP26)

print("Servo Sweep Demo")
print("Sweeping servo back and forth...")

# Sweep from 0 to 180 degrees
print("Sweeping 0° to 180°")
servo.sweep(0, 180, 0.01)  # Fast sweep
time.sleep(1)

# Sweep from 180 to 0 degrees
print("Sweeping 180° to 0°")
servo.sweep(180, 0, 0.01)  # Fast sweep
time.sleep(1)

# Slow sweep
print("Slow sweep 0° to 180°")
servo.sweep(0, 180, 0.05)  # Slow sweep
time.sleep(1)

print("Sweep demo completed!")
