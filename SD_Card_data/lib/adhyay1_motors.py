# adhyay1_motors.py
import pwmio

class Adhyay1_Motor:
    def __init__(self, pin1, pin2, freq=1000):
        self.a1 = pwmio.PWMOut(pin1, frequency=freq)
        self.a2 = pwmio.PWMOut(pin2, frequency=freq)

    def _duty(self, percent):
        return int((percent / 100) * 65535)

    def forward(self, speed=100):
        self.a1.duty_cycle = self._duty(speed)
        self.a2.duty_cycle = 0

    def reverse(self, speed=100):
        self.a1.duty_cycle = 0
        self.a2.duty_cycle = self._duty(speed)

    def stop(self):
        self.a1.duty_cycle = 0
        self.a2.duty_cycle = 0
