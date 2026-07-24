import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_motors import Adhyay1_Motor

# Initialize both motors
left_motor = Adhyay1_Motor(board.GP11, board.GP10)
right_motor = Adhyay1_Motor(board.GP14, board.GP15)

print("Dual Motor Test")
print("Testing both motors together...")

# Forward together
print("Both motors forward 75%")
left_motor.forward(75)
right_motor.forward(75)
time.sleep(3)

# Reverse together
print("Both motors reverse 75%")
left_motor.reverse(75)
right_motor.reverse(75)
time.sleep(3)

# Turn right (left forward, right stop)
print("Turn right - left motor forward")
left_motor.forward(80)
right_motor.stop()
time.sleep(2)

# Turn left (right forward, left stop)
print("Turn left - right motor forward")
right_motor.forward(80)
left_motor.stop()
time.sleep(2)

# Spin clockwise (left forward, right reverse)
print("Spin clockwise")
left_motor.forward(70)
right_motor.reverse(70)
time.sleep(2)

# Spin counter-clockwise (left reverse, right forward)
print("Spin counter-clockwise")
left_motor.reverse(70)
right_motor.forward(70)
time.sleep(2)

# Stop both
left_motor.stop()
right_motor.stop()
print("Dual motor test completed!")
