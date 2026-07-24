# run_us_all_three.py - MicroPython version
import time
from adhyay1_ultrasonic import Adhyay1_Ultrasonic

# Initialize all three ultrasonic sensors
left_sensor = Adhyay1_Ultrasonic(13, 12)   # Left
middle_sensor = Adhyay1_Ultrasonic(8, 9)   # Middle
right_sensor = Adhyay1_Ultrasonic(7, 6)    # Right

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
        print("Left: {:5.1f} cm | ".format(left_dist), end="")
        print("Middle: {:5.1f} cm | ".format(middle_dist), end="")
        print("Right: {:5.1f} cm".format(right_dist))
        
        # Object detection logic
        if left_dist != -1 and left_dist < 15:
            print("Left sensor: Object detected!")
        if middle_dist != -1 and middle_dist < 15:
            print("Middle sensor: Object detected!")
        if right_dist != -1 and right_dist < 15:
            print("Right sensor: Object detected!")
        
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nAll sensor monitoring stopped")