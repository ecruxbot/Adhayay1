# scrolling_text.py - MicroPython version
import time
from adhyay1_oled import Adhyay1_OLED

# Initialize OLED display
oled = Adhyay1_OLED(sda_pin=4, scl_pin=5)

print("Scrolling Text Display")
print("Showing scrolling text effect...")

messages = [
    "Welcome to Adhyay1 Kit",
    "OLED Display Demo",
    "Scrolling Text Effect",
    "Raspberry Pi Pico",
    "CircuitPython Rocks!",
    "Hello World! "
]

def scroll_text(text, delay=0.2):
    """Scroll text across the display"""
    text_width = len(text) * 8  # Approximate width in pixels
    for x_pos in range(128, -text_width, -1):  # Move from right to left
        oled.clear()
        oled.show_data(text, x=x_pos, y=25, clear=False)
        time.sleep(delay)

try:
    for message in messages:
        print("Scrolling:", message)
        scroll_text(message)
        time.sleep(1)

except KeyboardInterrupt:
    oled.clear()
    oled.show_data("Scroll Stopped", x=10, y=30)
    print("\nScrolling text stopped")