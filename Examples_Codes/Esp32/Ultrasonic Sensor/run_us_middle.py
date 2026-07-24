# run_us_middle.py - MicroPython version
import time
from adhyay1_ultrasonic import Adhyay1_Ultrasonic

# Initialize MIDDLE ultrasonic sensor (Trig: GP8, Echo: GP9)
middle_sensor = Adhyay1_Ultrasonic(8, 9)

print("Middle Ultrasonic Sensor")
print("Measuring distance with middle sensor...")
print("Press Ctrl+C to stop")

try:
    while True:
        distance = middle_sensor.get_distance_cm()
        
        if distance == -1:
            print("Middle: No object detected or timeout")
        else:
            print("Middle: {:5.1f} cm".format(distance))
            
            # Add proximity zones
            if distance < 10:
                print("Middle: Very close object!")
            elif distance < 30:
                print("Middle: Object in medium range")
            elif distance < 50:
                print("Middle: Object in far range")
        
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nMiddle sensor monitoring stopped")