# tilt_detector.py - MicroPython version
import machine
import time
from adhyay1_mpu6050 import Adhyay1_MPU6050

# Initialize I2C and MPU6050
i2c = machine.I2C(0, scl=machine.Pin(3), sda=machine.Pin(2))
mpu = Adhyay1_MPU6050(i2c)

print("Tilt Detection")
print("Detecting device orientation...")

def detect_tilt(accel):
    """Detect tilt orientation from accelerometer data"""
    x, y, z = accel
    
    # Calculate tilt angles (simplified)
    tilt_x = int((x / 9.8) * 90)  # Approximate angle in degrees
    tilt_y = int((y / 9.8) * 90)
    
    # Determine orientation
    if z > 8.0:
        position = "FLAT"
    elif z < -8.0:
        position = "UPSIDE DOWN"
    elif x > 5.0:
        position = "TILT LEFT"
    elif x < -5.0:
        position = "TILT RIGHT"
    elif y > 5.0:
        position = "TILT FORWARD"
    elif y < -5.0:
        position = "TILT BACKWARD"
    else:
        position = "UNKNOWN"
    
    return tilt_x, tilt_y, position

try:
    while True:
        accel = mpu.get_accel()
        tilt_x, tilt_y, position = detect_tilt(accel)
        
        print("X-tilt: {:3d}° | Y-tilt: {:3d}° | {}".format(tilt_x, tilt_y, position))
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nTilt detection stopped")