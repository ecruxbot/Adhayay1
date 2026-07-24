import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_ultrasonic import Adhyay1_Ultrasonic

# Initialize all three ultrasonic sensors
left_sensor = Adhyay1_Ultrasonic(board.GP13, board.GP12)   # Left
middle_sensor = Adhyay1_Ultrasonic(board.GP8, board.GP9)   # Middle
right_sensor = Adhyay1_Ultrasonic(board.GP7, board.GP6)    # Right

print("All Three Ultrasonic Sensors")
print("Monitoring left, middle, and right sensors...")
print("Press Ctrl+C to stop")

try:
    while True:
        # Read all three sensors
        left_dist = left_sensor.get_distance_cm()
        middle_dist = middle_sensor.get_distance_cm()
        right_dist = right_sensor.get_distance_cm()
        
        # Display results
        print(f"Left: {left_dist:5.1f} cm | ", end="")
        print(f"Middle: {middle_dist:5.1f} cm | ", end="")
        print(f"Right: {right_dist:5.1f} cm")
        
        # Object detection logic
        if left_dist != -1 and left_dist < 15:
            print("Left sensor: 🚨 Object detected!")
        if middle_dist != -1 and middle_dist < 15:
            print("Middle sensor: 🚨 Object detected!")
        if right_dist != -1 and right_dist < 15:
            print("Right sensor: 🚨 Object detected!")
        
        # Clear line for next output
        print("\033[F\033[F")  # Move cursor up two lines
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\n\nAll sensor monitoring stopped")
