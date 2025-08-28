import adhyay1_libs
adhyay1_libs.mount_sd()
import board
import time
from adhyay1_led import Adhyay1_LED

# Pin GP27 pe ek NeoPixel LED
led = Adhyay1_LED(board.GP27, num_leds=8, brightness=0.5)

while True:
    # LED ON red color
    print("LED ON red color")
    led.on((255, 0, 0))
    time.sleep(1)

    # Blink blue
    print("Blink blue")
    led.blink((0, 0, 255), times=3, delay=0.3)

    # Pulse green
    print("Pulse green")
    led.pulse((0, 255, 0), delay=0.01)

    # Chase yellow
    print("Chase yellow")
    led.chase((255, 255, 0), delay=0.05)

    # Color wipe magenta
    print("Color wipe magenta")
    led.color_wipe((255, 0, 255), delay=0.05)

    # Wave effect red & blue
    print("Wave effect red & blue")
    led.wave((255, 0, 0), (0, 0, 255), delay=0.05)

    # Rainbow cycle
    print("Rainbow cycle")
    led.rainbow_cycle(wait=0.01)

    # LED OFF
    print("LED OFF")
    led.off()
    time.sleep(1)

