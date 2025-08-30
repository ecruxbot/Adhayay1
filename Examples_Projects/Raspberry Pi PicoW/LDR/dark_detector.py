import board
import time
from adhyay1_ldr import Adhyay1_LDR
from adhyay1_buzzer import Adhyay1_Buzzer

# Initialize components
ldr = Adhyay1_LDR(board.GP26)
buzzer = Adhyay1_Buzzer(board.GP22, passive=True)

# Set darkness threshold (adjust based on your environment)
DARK_THRESHOLD = 35000

print("Darkness Detector with Alarm")
print(f"Threshold: {DARK_THRESHOLD} (higher = darker)")
print("Alarm will sound when it gets dark")

try:
    while True:
        raw_value = ldr.read_raw()
        is_dark = ldr.is_dark(DARK_THRESHOLD)
        
        print(f"Raw: {raw_value:>5d} | Dark: {is_dark}", end=" ")
        
        if is_dark:
            print("🚨 ALARM: Too dark!")
            buzzer.on()  # Sound alarm
        else:
            print("✅ Normal light")
            buzzer.off()  # Turn off alarm
        
        time.sleep(0.5)

except KeyboardInterrupt:
    buzzer.off()
    print("\nDarkness detector stopped")
