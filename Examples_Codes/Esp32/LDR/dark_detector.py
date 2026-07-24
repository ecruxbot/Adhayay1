# dark_detector.py - MicroPython version
import time
from adhyay1_ldr import Adhyay1_LDR
from adhyay1_buzzer import Adhyay1_Buzzer

# Initialize components
ldr = Adhyay1_LDR(26)
buzzer = Adhyay1_Buzzer(22, passive=True)

# Set darkness threshold (adjust based on your environment)
# Scaled for MicroPython's 12-bit ADC
DARK_THRESHOLD = 3500  # 0-4095 range

print("Darkness Detector with Alarm")
print("Threshold:", DARK_THRESHOLD, "(higher = darker)")
print("Alarm will sound when it gets dark")

try:
    while True:
        raw_value = ldr.read_raw()
        is_dark = ldr.is_dark(DARK_THRESHOLD * 65535 / 4095)  # Convert threshold
        
        print("Raw: {:5d} | Dark: {}".format(raw_value, is_dark), end=" ")
        
        if is_dark:
            print("ALARM: Too dark!")
            buzzer.on()  # Sound alarm
        else:
            print("Normal light")
            buzzer.off()  # Turn off alarm
        
        time.sleep(0.5)

except KeyboardInterrupt:
    buzzer.off()
    print("\nDarkness detector stopped")