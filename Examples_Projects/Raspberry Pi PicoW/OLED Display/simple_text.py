import board
import time
from adhyay1_oled import Adhyay1_OLED

# Initialize OLED display
oled = Adhyay1_OLED(sda_pin=board.GP4, scl_pin=board.GP5)

print("Simple Text Display")
print("Showing text on OLED...")

# Display simple text
oled.show_data("Hello Adhyay1!", x=10, y=10)
time.sleep(2)

oled.show_data("OLED Display", x=15, y=25)
time.sleep(2)

oled.show_data("Working Great!", x=20, y=40)
time.sleep(2)

# Clear display
oled.clear()
oled.show_data("Text Demo Done!", x=10, y=30)
time.sleep(2)

print("Text display completed")
