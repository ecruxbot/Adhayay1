import board
import time
from adhyay1_motors import Adhyay1_Motor

# Initialize LEFT motor only (GP11, GP10)
left_motor = Adhyay1_Motor(board.GP11, board.GP10)

print("Left Motor Test")
print("Testing left motor only...")

# Forward tests
print("Forward 50% speed for 2 seconds")
left_motor.forward(50)
time.sleep(2)

print("Forward 100% speed for 2 seconds")
left_motor.forward(100)
time.sleep(2)

# Reverse tests
print("Reverse 50% speed for 2 seconds")
left_motor.reverse(50)
time.sleep(2)

print("Reverse 100% speed for 2 seconds")
left_motor.reverse(100)
time.sleep(2)

# Stop
left_motor.stop()
print("Left motor test completed!")
