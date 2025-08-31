# simple_tone.py - MicroPython version
import time
from adhyay1_speaker import Adhyay1_Speaker

# Initialize speaker on GP28
speaker = Adhyay1_Speaker()
speaker.begin(28)

print("Simple Tone Generator")
print("Playing different tones...")

# Play various tones
tones = [
    (262, 0.5, "C4 (Do)"),
    (294, 0.5, "D4 (Re)"),
    (330, 0.5, "E4 (Mi)"),
    (349, 0.5, "F4 (Fa)"),
    (392, 0.5, "G4 (Sol)"),
    (440, 0.5, "A4 (La)"),
    (494, 0.5, "B4 (Si)"),
    (523, 1.0, "C5 (Do)")
]

for freq, duration, note_name in tones:
    print("Playing:", note_name, "({}Hz)".format(freq))
    speaker.play_tone(freq, duration)
    time.sleep(0.2)  # Short pause between tones

print("Tone demo completed!")