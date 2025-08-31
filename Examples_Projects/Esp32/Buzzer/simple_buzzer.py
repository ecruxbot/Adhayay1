# simple_buzzer.py - MicroPython version
import time
from adhyay1_buzzer import Adhyay1_Buzzer

# Initialize passive buzzer on GP22
buzzer = Adhyay1_Buzzer(22, passive=True)

print("Simple Buzzer Test")

# Single beep
print("Single beep")
buzzer.beep()
time.sleep(1)

# Turn on for 2 seconds
print("Continuous sound for 2 seconds")
buzzer.on()
time.sleep(2)
buzzer.off()

print("Test completed")