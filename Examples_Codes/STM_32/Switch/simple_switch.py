import board, time
import adhyay1_libs; adhyay1_libs.mount_sd()

from adhyay1_button import Adhyay1_PushButton

button = Adhyay1_PushButton(board.GP21)

while True:
    if button.is_pressed():
        print("Button Pressed!")
    time.sleep(0.1)

