# color_mixer.py - MicroPython version
import machine
import time
from adhyay1_led import Adhyay1_LED

# Initialize LED
led = Adhyay1_LED(machine.Pin(27), num_leds=1, brightness=0.6)

print("Color Mixer Demo")

# Smooth color transitions
colors = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (148, 0, 211),  # Violet
    (255, 0, 255),  # Magenta
    (255, 255, 255) # White
]

print("Smooth color transitions")
for color in colors:
    led.on(color)
    print("Color:", color)
    time.sleep(1)

# Color fading between two colors
print("Color fading between Red and Blue")
for i in range(0, 255, 5):
    led.on((i, 0, 255-i))
    time.sleep(0.05)

for i in range(255, 0, -5):
    led.on((i, 0, 255-i))
    time.sleep(0.05)

led.off()
print("Color mixer demo completed")