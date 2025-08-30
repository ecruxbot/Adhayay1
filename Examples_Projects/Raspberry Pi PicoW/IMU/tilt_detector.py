import board
import busio
import time
from adhyay1_mpu6050 import Adhyay1_MPU6050

# Initialize I2C and MPU6050
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
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
        position = "📱 FLAT"
    elif z < -8.0:
        position = "🔄 UPSIDE DOWN"
    elif x > 5.0:
        position = "⬅️  TILT LEFT"
    elif x < -5.0:
        position = "➡️  TILT RIGHT"
    elif y > 5.0:
        position = "⬇️  TILT FORWARD"
    elif y < -5.0:
        position = "⬆️  TILT BACKWARD"
    else:
        position = "🎯 UNKNOWN"
    
    return tilt_x, tilt_y, position

try:
    while True:
        accel = mpu.get_accel()
        tilt_x, tilt_y, position = detect_tilt(accel)
        
        print(f"X-tilt: {tilt_x:3d}° | Y-tilt: {tilt_y:3d}° | {position}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nTilt detection stopped")
