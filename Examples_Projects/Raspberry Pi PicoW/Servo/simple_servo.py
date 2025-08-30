import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_servo import Adhyay1_Servo

# Initialize servo on GP26
servo = Adhyay1_Servo(board.GP26)

print("Simple Servo Control")
print("Moving servo to basic positions...")

# Move to basic angles
servo.set_angle(0)      # 0 degrees
print("Position: 0°")
time.sleep(1)

servo.set_angle(90)     # 90 degrees (middle)
print("Position: 90°")
time.sleep(1)

servo.set_angle(180)    # 180 degrees
print("Position: 180°")
time.sleep(1)

servo.set_angle(90)     # Back to middle
print("Position: 90°")
time.sleep(1)

print("Simple servo test completed!")
