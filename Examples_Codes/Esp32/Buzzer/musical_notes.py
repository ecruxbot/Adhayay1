# musical_notes.py - MicroPython version
import time
from adhyay1_buzzer import Adhyay1_Buzzer

# Initialize passive buzzer on GP22
buzzer = Adhyay1_Buzzer(22, passive=True)

print("Musical Notes Demo")

# Play simple melody using different frequencies
notes = [
    (262, 0.3),  # C4
    (294, 0.3),  # D4
    (330, 0.3),  # E4
    (349, 0.3),  # F4
    (392, 0.3),  # G4
    (440, 0.3),  # A4
    (494, 0.3),  # B4
    (523, 0.5)   # C5
]

for freq, duration in notes:
    print("Playing note:", freq, "Hz")
    buzzer.tone(freq)
    time.sleep(duration)
    buzzer.off()
    time.sleep(0.1)

buzzer.off()
print("Melody completed")