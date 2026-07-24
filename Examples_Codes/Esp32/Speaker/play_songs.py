# play_songs.py - MicroPython version
import time
from adhyay1_speaker import Adhyay1_Speaker

# Initialize speaker on GP28
speaker = Adhyay1_Speaker()
speaker.begin(28)

print("Music Player")
print("Playing melodies using tones...")

# Define some simple melodies
melodies = {
    "scale": [
        (262, 0.3), (294, 0.3), (330, 0.3), (349, 0.3),
        (392, 0.3), (440, 0.3), (494, 0.3), (523, 0.5)
    ],
    "happy_birthday": [
        (262, 0.4), (262, 0.4), (294, 0.8), (262, 0.8),
        (349, 0.8), (330, 0.8), (262, 0.4), (262, 0.4),
        (294, 0.8), (262, 0.8), (392, 0.8), (349, 0.8)
    ],
    "jingle_bells": [
        (330, 0.4), (330, 0.4), (330, 0.8), (330, 0.4),
        (330, 0.4), (330, 0.8), (330, 0.4), (392, 0.4),
        (262, 0.8), (294, 0.4), (330, 1.0)
    ]
}

try:
    for song_name, notes in melodies.items():
        print("Now playing:", song_name)
        speaker.play_notes(notes)
        print("Song completed")
        time.sleep(1)  # Pause between songs
    
    print("All songs played!")

except KeyboardInterrupt:
    speaker.stop()
    print("\nMusic playback stopped")

except Exception as e:
    print("Error:", e)
    speaker.stop()