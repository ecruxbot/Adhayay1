import board, time
import adhyay1_libs; adhyay1_libs.mount_sd()

import adhyay1_led

led = adhyay1_led.Adhyay1_LED(board.GP27)

while True:
    led.on((255, 0, 0))  # Red
    time.sleep(1)
    led.on((0, 255, 0))  # Green
    time.sleep(1)
    led.on((0, 0, 255))  # Blue
    time.sleep(1)

