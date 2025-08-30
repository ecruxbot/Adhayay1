import board
import time
import random
from adhyay1_led import Adhyay1_LED

# Initialize LED strip with 12 LEDs
led = Adhyay1_LED(board.GP27, num_leds=12, brightness=0.4)

print("Advanced LED Effects")

# Pulse effect
print("Pulse effect (Green)")
led.pulse((0, 255, 0), delay=0.02)

# Rainbow cycle
print("Rainbow cycle")
led.rainbow_cycle(wait=0.05)

# Random colors
print("Random colors")
for _ in range(20):
    led.random_colors(delay=0.1)

# Breathing effect (custom implementation)
print("Breathing effect (Blue)")
for intensity in range(0, 255, 5):
    led.on((0, 0, intensity))
    time.sleep(0.02)
for intensity in range(255, 0, -5):
    led.on((0, 0, intensity))
    time.sleep(0.02)

led.off()
print("Advanced effects completed")
