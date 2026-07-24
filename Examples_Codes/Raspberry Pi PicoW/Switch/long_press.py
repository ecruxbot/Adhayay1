import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_button import Adhyay1_PushButton

# Initialize switch on GP21
switch = Adhyay1_PushButton(board.GP21)

print("Long Press Detector")
print("Press and hold for more than 1 second")

while True:
    if switch.is_pressed():
        start_time = time.monotonic()
        
        # Wait while button is pressed
        while switch.is_pressed():
            time.sleep(0.1)
        
        press_duration = time.monotonic() - start_time
        
        if press_duration > 1.0:
            print(f"⏰ LONG PRESS ({press_duration:.1f} seconds)")
        else:
            print(f"🔘 SHORT PRESS ({press_duration:.1f} seconds)")
    
    time.sleep(0.1)
