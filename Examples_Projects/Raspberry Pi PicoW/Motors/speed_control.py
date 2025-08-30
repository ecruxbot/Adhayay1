import board
import time
from adhyay1_motors import Adhyay1_Motor

# Initialize both motors
left_motor = Adhyay1_Motor(board.GP11, board.GP10)
right_motor = Adhyay1_Motor(board.GP14, board.GP15)

print("Motor Speed Control Demo")
print("Testing different speed levels...")

# Speed ramp up forward
print("Ramping up speed forward...")
for speed in range(0, 101, 10):  # 0% to 100% in steps of 10
    left_motor.forward(speed)
    right_motor.forward(speed)
    print(f"Speed: {speed}%")
    time.sleep(1)

time.sleep(2)

# Speed ramp down forward
print("Ramping down speed forward...")
for speed in range(100, -1, -10):  # 100% to 0% in steps of 10
    left_motor.forward(speed)
    right_motor.forward(speed)
    print(f"Speed: {speed}%")
    time.sleep(1)

time.sleep(1)

# Speed ramp up reverse
print("Ramping up speed reverse...")
for speed in range(0, 101, 10):
    left_motor.reverse(speed)
    right_motor.reverse(speed)
    print(f"Speed: {speed}%")
    time.sleep(1)

time.sleep(2)

# Different speeds for turning
print("Different speeds for smooth turning...")
left_motor.forward(40)   # Slow left
right_motor.forward(80)  # Fast right → gentle right turn
print("Gentle right turn (L:40%, R:80%)")
time.sleep(3)

left_motor.forward(80)   # Fast left
right_motor.forward(40)  # Slow right → gentle left turn
print("Gentle left turn (L:80%, R:40%)")
time.sleep(3)

# Stop
left_motor.stop()
right_motor.stop()
print("Speed control demo completed!")
