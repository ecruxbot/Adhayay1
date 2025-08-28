# adhyay1_led.py
import neopixel
import time

class Adhyay1_LED:
    def __init__(self, pin, num_leds=1, brightness=1.0):
        self.pixels = neopixel.NeoPixel(pin, num_leds, brightness=brightness, auto_write=False)
        self.num_leds = num_leds

    def on(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def pulse(self, color, delay=0.01):
        for b in range(0, 255, 5):
            scaled = tuple(int(c * b / 255) for c in color)
            self.pixels.fill(scaled)
            self.pixels.show()
            time.sleep(delay)
        for b in range(255, 0, -5):
            scaled = tuple(int(c * b / 255) for c in color)
            self.pixels.fill(scaled)
            self.pixels.show()
            time.sleep(delay)

    def blink(self, color, times=5, delay=0.2):
        for _ in range(times):
            self.pixels.fill(color)
            self.pixels.show()
            time.sleep(delay)
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
            time.sleep(delay)

    def chase(self, color, delay=0.05):
        for i in range(self.num_leds):
            self.pixels[i] = color
            self.pixels.show()
            time.sleep(delay)
            self.pixels[i] = (0, 0, 0)
            self.pixels.show()

    def color_wipe(self, color, delay=0.05):
        for i in range(self.num_leds):
            self.pixels[i] = color
            self.pixels.show()
            time.sleep(delay)

    def wave(self, color1, color2, delay=0.05):
        for i in range(self.num_leds):
            self.pixels.fill(color1)
            self.pixels[i] = color2
            self.pixels.show()
            time.sleep(delay)

    def random_colors(self, delay=0.05):
        for i in range(self.num_leds):
            self.pixels[i] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.pixels.show()
        time.sleep(delay)

    def rainbow_cycle(self, wait=0.01):
        for j in range(255):
            for i in range(self.num_leds):
                pixel_index = (i * 256 // self.num_leds) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def off(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def wheel(self, pos):
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return (pos * 3, 0, 255 - pos * 3)
