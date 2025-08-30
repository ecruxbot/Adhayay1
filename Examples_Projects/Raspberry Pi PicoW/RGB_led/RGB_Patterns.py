import board
import time
from adhyay1_led import Adhyay1_LED

# Initialize LED strip with 8 LEDs
led = Adhyay1_LED(board.GP27, num_leds=8, brightness=0.3)

print("LED Patterns Demo")

# Blink pattern
print("Blink pattern (Red)")
led.blink((255, 0, 0), times=5, delay=0.3)

# Chase pattern
print("Chase pattern (Blue)")
led.chase((0, 0, 255), delay=0.1)

# Color wipe pattern
print("Color wipe (Green)")
led.color_wipe((0, 255, 0), delay=0.05)

# Wave pattern
print("Wave pattern (Red & Blue)")
led.wave((255, 0, 0), (0, 0, 255), delay=0.08)

led.off()
print("All patterns completed")
