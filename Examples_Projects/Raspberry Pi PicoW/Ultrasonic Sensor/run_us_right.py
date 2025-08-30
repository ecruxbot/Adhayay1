import board
import time
from adhyay1_ultrasonic import Adhyay1_Ultrasonic

# Initialize RIGHT ultrasonic sensor (Trig: GP7, Echo: GP6)
right_sensor = Adhyay1_Ultrasonic(board.GP7, board.GP6)

print("Right Ultrasonic Sensor")
print("Measuring distance with right sensor...")
print("Press Ctrl+C to stop")

try:
    while True:
        distance = right_sensor.get_distance_cm()
        
        if distance == -1:
            print("Right: ❌ No object detected or timeout")
        else:
            print(f"Right: 📏 {distance:5.1f} cm")
            
            # Continuous distance graph
            bars = int(distance / 5)  # 1 bar = 5 cm
            graph = "[" + "#" * bars + " " * (20 - bars) + "]"
            print(f"Right: {graph} {distance:3.0f}cm")
        
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nRight sensor monitoring stopped")
