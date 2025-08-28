import digitalio

class Adhyay1_IRSensor:
    def __init__(self, pins):
        self.sensors = []
        for pin in pins:
            s = digitalio.DigitalInOut(pin)
            s.direction = digitalio.Direction.INPUT
            s.pull = digitalio.Pull.UP
            self.sensors.append(s)

    def read_all(self):
        return [0 if s.value else 1 for s in self.sensors]
