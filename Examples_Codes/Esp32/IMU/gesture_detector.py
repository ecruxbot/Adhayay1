# gesture_detector.py - MicroPython version
import machine
import time
from adhyay1_mpu6050 import Adhyay1_MPU6050

# Initialize I2C and MPU6050
i2c = machine.I2C(0, scl=machine.Pin(3), sda=machine.Pin(2))
mpu = Adhyay1_MPU6050(i2c)

print("Simple Gesture Detector")
print("Move the sensor to detect gestures...")

# Variables for gesture detection
last_accel = mpu.get_accel()
last_time = time.ticks_ms()

def detect_gesture(current_accel, last_accel, time_diff):
    """Detect simple gestures from acceleration changes"""
    # Calculate acceleration differences
    diff_x = abs(current_accel[0] - last_accel[0])
    diff_y = abs(current_accel[1] - last_accel[1])
    diff_z = abs(current_accel[2] - last_accel[2])
    
    # Check for significant movements
    threshold = 3.0  # g-force threshold for gesture detection
    
    if diff_x > threshold and diff_x > diff_y and diff_x > diff_z:
        return "SHAKE X"
    elif diff_y > threshold and diff_y > diff_x and diff_y > diff_z:
        return "SHAKE Y"
    elif diff_z > threshold and diff_z > diff_x and diff_z > diff_y:
        return "SHAKE Z"
    elif current_accel[2] < 5.0:  # Quick flip detection
        return "FLIP"
    else:
        return None

try:
    while True:
        current_accel = mpu.get_accel()
        current_time = time.ticks_ms()
        time_diff = (current_time - last_time) / 1000  # Convert to seconds
        
        gesture = detect_gesture(current_accel, last_accel, time_diff)
        
        if gesture:
            print("Gesture detected:", gesture)
        
        # Update for next iteration
        last_accel = current_accel
        last_time = current_time
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nGesture detection stopped")