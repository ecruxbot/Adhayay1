import board
import time
from adhyay1_buzzer import Adhyay1_Buzzer

# Initialize passive buzzer on GP22
buzzer = Adhyay1_Buzzer(board.GP22, passive=True)

print("Buzzer Patterns")

# Built-in alert pattern
print("Alert pattern (3 beeps)")
buzzer.alert_pattern(550)
time.sleep(1)

# Custom beep pattern
print("Custom pattern: . . . - (SOS pattern)")
for _ in range(3):
    buzzer.on()
    time.sleep(0.1)
    buzzer.off()
    time.sleep(0.1)

time.sleep(0.3)

for _ in range(3):
    buzzer.on()
    time.sleep(0.3)
    buzzer.off()
    time.sleep(0.1)

print("Patterns completed")
