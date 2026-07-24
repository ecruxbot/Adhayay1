# long_press.py - MicroPython version
import time
from adhyay1_button import Adhyay1_PushButton

# Initialize switch on GP21
switch = Adhyay1_PushButton(21)

print("Long Press Detector")
print("Press and hold for more than 1 second")

while True:
    if switch.is_pressed():
        start_time = time.ticks_ms()
        
        # Wait while button is pressed
        while switch.is_pressed():
            time.sleep(0.1)
        
        press_duration = time.ticks_diff(time.ticks_ms(), start_time) / 1000.0
        
        if press_duration > 1.0:
            print("LONG PRESS ({:.1f} seconds)".format(press_duration))
        else:
            print("SHORT PRESS ({:.1f} seconds)".format(press_duration))
    
    time.sleep(0.1)