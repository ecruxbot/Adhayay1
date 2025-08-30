import board
import time
from adhyay1_ultrasonic import Adhyay1_Ultrasonic

# Initialize LEFT ultrasonic sensor (Trig: GP13, Echo: GP12)
left_sensor = Adhyay1_Ultrasonic(board.GP13, board.GP12)

print("Left Ultrasonic Sensor")
print("Measuring distance with left sensor...")
print("Press Ctrl+C to stop")

try:
    while True:
        distance = left_sensor.get_distance_cm()
        
        if distance == -1:
            print("Left: ❌ No object detected or timeout")
        else:
            print(f"Left: 📏 {distance:5.1f} cm")
            
            # Add object detection alert
            if distance < 20:
                print("Left: ⚠️  Object nearby!")
        
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nLeft sensor monitoring stopped")
