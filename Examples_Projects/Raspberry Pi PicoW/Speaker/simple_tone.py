import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_speaker import Adhyay1_Speaker

# Initialize speaker on GP28
speaker = Adhyay1_Speaker()
speaker.begin(board.GP28)

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
    print(f"Playing: {note_name} ({freq}Hz)")
    # For tone generation, we'll use a different approach since your library is WAV-based
    # This is a placeholder - you might need a different library for pure tones
    print(f"Would play {freq}Hz for {duration}s")
    time.sleep(duration)

print("Tone demo completed!")
