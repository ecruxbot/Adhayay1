import time
import board
import pwmio
from adafruit_motor import servo

class Adhyay1_Servo:

    def __init__(self, pin=board.GP0):
        self.pwm = pwmio.PWMOut(pin, duty_cycle=2 ** 15, frequency=50)
        self.servo = servo.Servo(self.pwm)
        self.last_angle = 0

    def set_angle(self, angle):
        angle = max(0, min(180, angle))
        self.servo.angle = angle
        self.last_angle = angle

    def get_angle(self):
        return self.servo.angle

    def sweep(self, start=0, end=180, delay=0.01):
        step = 1 if end > start else -1
        for angle in range(start, end + step, step):
            self.set_angle(angle)
            time.sleep(delay)

    def toggle(self, angle1=0, angle2=90):
        if self.last_angle == angle1:
            self.set_angle(angle2)
        else:
            self.set_angle(angle1)

    def control_by_button(self, button_pin):
        import digitalio
        button = digitalio.DigitalInOut(button_pin)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        state = False
        while True:
            if not button.value:
                self.toggle(0, 90)
                while not button.value:
                    pass
                time.sleep(0.3)

    def control_by_sensor(self, sensor_func, angle_on=90, angle_off=0):
        while True:
            if sensor_func():
                self.set_angle(angle_on)
            else:
                self.set_angle(angle_off)
            time.sleep(0.2)

    def ramp_move(self, delay=0.05):
        self.sweep(0, 180, delay)
        self.sweep(180, 0, delay)

    def multi_position(self, angles=[0, 45, 90, 135, 180], delay=0.5):
        for angle in angles:
            self.set_angle(angle)
            time.sleep(delay)

    def heartbeat(self):
        while True:
            self.toggle(0, 180)
            time.sleep(1)

    def attach_sensor_display(self, oled_obj, sensor_func):
        while True:
            val = sensor_func()
            if val:
                self.set_angle(90)
                oled_obj.show_status("Servo: ON")
            else:
                self.set_angle(0)
                oled_obj.show_status("Servo: OFF")
            time.sleep(0.5)
