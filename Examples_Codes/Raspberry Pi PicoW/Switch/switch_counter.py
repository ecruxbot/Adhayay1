import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_button import Adhyay1_PushButton

# Initialize switch on GP21
switch = Adhyay1_PushButton(board.GP21)

press_count = 0
last_state = False

print("Switch Press Counter")
print("Press the button to count...")

while True:
    current_state = switch.is_pressed()
    
    # Detect button press (rising edge)
    if current_state and not last_state:
        press_count += 1
        print(f"🎯 Press count: {press_count}")
    
    last_state = current_state
    time.sleep(0.05)  # Small delay for debouncing
