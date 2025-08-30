import board
import time
from adhyay1_button import Adhyay1_PushButton

# Initialize switch on GP21
switch = Adhyay1_PushButton(board.GP21)

print("Simple Switch Demo")
print("Press the button to see the state...")

while True:
    if switch.is_pressed():
        print("Button PRESSED")
    else:
        print("Button RELEASED")
    
    time.sleep(0.1)  # Small delay to avoid flooding output
