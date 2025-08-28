import board
import time
class Adhyay1_MPU6050:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address

        # Wake up MPU6050 (it starts in sleep mode)
        self._write_register(0x6B, 0x00)

    def _write_register(self, reg, data):
        while not self.i2c.try_lock():
            pass
        self.i2c.writeto(self.address, bytes([reg, data]))
        self.i2c.unlock()

    def _read_registers(self, reg, length):
        buf = bytearray(length)
        while not self.i2c.try_lock():
            pass
        self.i2c.writeto_then_readfrom(self.address, bytes([reg]), buf)
        self.i2c.unlock()
        return buf

    def _convert(self, high, low):
        value = (high << 8) | low
        if value >= 0x8000:
            return -((65535 - value) + 1)
        else:
            return value

    def get_accel(self):
        raw = self._read_registers(0x3B, 6)
        ax = self._convert(raw[0], raw[1]) / 16384.0
        ay = self._convert(raw[2], raw[3]) / 16384.0
        az = self._convert(raw[4], raw[5]) / 16384.0
        return (ax, ay, az)

    def get_gyro(self):
        raw = self._read_registers(0x43, 6)
        gx = self._convert(raw[0], raw[1]) / 131.0
        gy = self._convert(raw[2], raw[3]) / 131.0
        gz = self._convert(raw[4], raw[5]) / 131.0
        return (gx, gy, gz)

    def get_temperature(self):
        raw = self._read_registers(0x41, 2)
        temp_raw = self._convert(raw[0], raw[1])
        return (temp_raw / 340.0) + 36.53

    def get_all(self):
        accel = self.get_accel()
        gyro = self.get_gyro()
        temp = self.get_temperature()
        return (accel, gyro, temp)