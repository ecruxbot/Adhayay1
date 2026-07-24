# play_sound_effects.py - MicroPython version
import time
from adhyay1_speaker import Adhyay1_Speaker

# Initialize speaker on GP28
speaker = Adhyay1_Speaker()
speaker.begin(28)

print("Sound Effects Player")
print("Playing various sound effects...")

# List of sound effects (frequency, duration pairs)
sound_effects = {
    "beep": [(1000, 0.1)],
    "alert": [(880, 0.2), (0, 0.1), (880, 0.2)],
    "siren": [(800, 0.1), (1200, 0.1), (800, 0.1), (1200, 0.1)],
    "click": [(2000, 0.05)],
    "chime": [(1047, 0.3), (1319, 0.3), (1568, 0.5)],
    "notification": [(1319, 0.1), (1568, 0.2)]
}

try:
    for effect_name, notes in sound_effects.items():
        print("Playing:", effect_name)
        speaker.play_notes(notes)
        time.sleep(0.5)  # Short pause between sounds
    
    print("All sound effects played!")

except KeyboardInterrupt:
    speaker.stop()
    print("\nSound effects stopped")

except Exception as e:
    print("Error:", e)