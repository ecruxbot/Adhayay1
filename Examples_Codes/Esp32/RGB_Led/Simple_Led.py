# Simple_Led.py - MicroPython version
import machine
import time
from adhyay1_led import Adhyay1_LED

# Initialize LED on GP27 with 1 LED and 50% brightness
led = Adhyay1_LED(machine.Pin(27), num_leds=1, brightness=0.5)

print("Simple LED Control - Basic Colors")

# Test basic colors
led.on((255, 0, 0))    # Red
print("Red")
time.sleep(1)

led.on((0, 255, 0))    # Green
print("Green")
time.sleep(1)

led.on((0, 0, 255))    # Blue
print("Blue")
time.sleep(1)

led.on((255, 255, 0))  # Yellow
print("Yellow")
time.sleep(1)

led.on((255, 0, 255))  # Magenta
print("Magenta")
time.sleep(1)

led.on((0, 255, 255))  # Cyan
print("Cyan")
time.sleep(1)

led.on((255, 255, 255))  # White
print("White")
time.sleep(1)

led.off()
print("Test completed")