import digitalio

class Adhyay1_PushButton:
    def __init__(self, pin, pull=True):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP if pull else None

    def is_pressed(self):
        return not self.button.value
