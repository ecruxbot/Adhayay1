import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import busio
import time
from adhyay1_mpu6050 import Adhyay1_MPU6050

# Initialize I2C and MPU6050
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
mpu = Adhyay1_MPU6050(i2c)

print("MPU6050 Simple Reading")
print("Accel (g), Gyro (°/s), Temp (°C)")
print("Press Ctrl+C to stop")

try:
    while True:
        # Read all sensor data
        accel = mpu.get_accel()
        gyro = mpu.get_gyro()
        temp = mpu.get_temperature()
        
        print(f"Accel: X:{accel[0]:6.2f} Y:{accel[1]:6.2f} Z:{accel[2]:6.2f} g")
        print(f"Gyro:  X:{gyro[0]:6.2f} Y:{gyro[1]:6.2f} Z:{gyro[2]:6.2f} °/s")
        print(f"Temp:  {temp:6.2f} °C")
        print("-" * 40)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMPU6050 reading stopped")
