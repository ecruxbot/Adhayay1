import digitalio, time

class Adhyay1_Ultrasonic:
    import time
    import digitalio
    import board
    def __init__(self, trig_pin, echo_pin):
        self.trig = digitalio.DigitalInOut(trig_pin)
        self.trig.direction = digitalio.Direction.OUTPUT
        self.trig.value = False

        self.echo = digitalio.DigitalInOut(echo_pin)
        self.echo.direction = digitalio.Direction.INPUT

    def get_distance_cm(self):
        self.trig.value = False
        time.sleep(0.000002)
        self.trig.value = True
        time.sleep(0.00001)
        self.trig.value = False

        timeout = 30000  # max wait loop
        count = 0

        while not self.echo.value:
            count += 1
            if count > timeout:
                return -1  # timeout

        start = time.monotonic_ns()

        count = 0
        while self.echo.value:
            count += 1
            if count > timeout:
                return -1

        end = time.monotonic_ns()

        duration = (end - start) / 1000  # us
        distance_cm = (duration / 2) / 29.1
        return round(distance_cm, 2)

    def is_object_near(self, threshold=20):
        d = self.get_distance_cm()
        return d != -1 and d <= threshold
