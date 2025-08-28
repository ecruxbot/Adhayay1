import pwmio, digitalio
import board
import time

class Adhyay1_Buzzer:
    def __init__(self, pin, passive=True):
        self.passive = passive
        if passive:
            self.buzzer = pwmio.PWMOut(pin, duty_cycle=0, frequency=440, variable_frequency=True)
        else:
            self.buzzer = digitalio.DigitalInOut(pin)
            self.buzzer.direction = digitalio.Direction.OUTPUT

    def on(self, freq=440):
        if self.passive:
            self.buzzer.duty_cycle = 32768
        else:
            self.buzzer.value = True

    def off(self):
        if self.passive:
            self.buzzer.duty_cycle = 0
        else:
            self.buzzer.value = False

    def beep(self, freq=440):
        self.on()
        

    def tone(self, freq=440 ):
        if self.passive:
            self.buzzer.frequency = freq
            self.buzzer.duty_cycle = 32768
            

    def alert_pattern(self, freq=440 ):
        for _ in range(3):
            self.on()
            time.sleep(0.2)
            self.off()
            time.sleep(0.2)

    def play_melody(self):
        if self.passive:
            notes = [262, 294, 330, 349, 392]
            for freq in notes:
                self.buzzer.frequency = freq
                self.buzzer.duty_cycle = 32768