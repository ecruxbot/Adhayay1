import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_motors import Adhyay1_Motor

# Initialize RIGHT motor only (GP14, GP15)
right_motor = Adhyay1_Motor(board.GP14, board.GP15)

print("Right Motor Test")
print("Testing right motor only...")

# Forward tests
print("Forward 50% speed for 2 seconds")
right_motor.forward(50)
time.sleep(2)

print("Forward 100% speed for 2 seconds")
right_motor.forward(100)
time.sleep(2)

# Reverse tests
print("Reverse 50% speed for 2 seconds")
right_motor.reverse(50)
time.sleep(2)

print("Reverse 100% speed for 2 seconds")
right_motor.reverse(100)
time.sleep(2)

# Stop
right_motor.stop()
print("Right motor test completed!")
