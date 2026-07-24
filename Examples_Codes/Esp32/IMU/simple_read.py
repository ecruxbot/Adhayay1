# simple_read.py - MicroPython version
import machine
import time
from adhyay1_mpu6050 import Adhyay1_MPU6050

# Initialize I2C and MPU6050
i2c = machine.I2C(0, scl=machine.Pin(3), sda=machine.Pin(2))
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
        
        print("Accel: X:{:6.2f} Y:{:6.2f} Z:{:6.2f} g".format(accel[0], accel[1], accel[2]))
        print("Gyro:  X:{:6.2f} Y:{:6.2f} Z:{:6.2f} °/s".format(gyro[0], gyro[1], gyro[2]))
        print("Temp:  {:6.2f} °C".format(temp))
        print("-" * 40)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMPU6050 reading stopped")