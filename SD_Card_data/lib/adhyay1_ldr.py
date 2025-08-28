import analogio

class Adhyay1_LDR:
    def __init__(self, pin):
        self.ldr = analogio.AnalogIn(pin)

    def read_raw(self):
        return self.ldr.value

    def read_voltage(self):
        return (self.ldr.value * 3.3) / 65535

    def is_dark(self, threshold=30000):
        return self.ldr.value > threshold
