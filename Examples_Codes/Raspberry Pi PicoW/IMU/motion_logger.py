import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import busio
import time
from adhyay1_mpu6050 import Adhyay1_MPU6050

# Initialize I2C and MPU6050
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
mpu = Adhyay1_MPU6050(i2c)

print("Motion Data Logger")
print("Logging sensor data every 0.5 seconds...")
print("Time\tAccel-X\tAccel-Y\tAccel-Z\tGyro-X\tGyro-Y\tGyro-Z")
print("-" * 60)

try:
    while True:
        # Get current time
        current_time = time.monotonic()
        
        # Read sensor data
        accel = mpu.get_accel()
        gyro = mpu.get_gyro()
        
        # Log data
        print("{:.1f}s\t{:.2f}\t{:.2f}\t{:.2f}\t{:.1f}\t{:.1f}\t{:.1f}".format(
            current_time, accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2]
        ))
        
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nMotion logging stopped")

