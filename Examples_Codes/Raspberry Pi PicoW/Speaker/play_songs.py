import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_speaker import Adhyay1_Speaker

# Initialize speaker on GP28
speaker = Adhyay1_Speaker()
speaker.begin(board.GP28)

print("Music Player")
print("Playing songs from SD card...")

# List of songs to play
songs = [
    "/sd/sounds/morya_re1.wav",
    "/sd/sounds/kolaveri.wav",
    "/sd/sounds/melody.wav",
    "/sd/sounds/tune.wav"
]

try:
    for song in songs:
        print(f"Now playing: {song}")
        try:
            speaker.play_music(song)
            print("Song completed")
            time.sleep(1)  # Pause between songs
        except Exception as e:
            print(f"Error playing {song}: {e}")
            continue
    
    print("All songs played!")

except KeyboardInterrupt:
    speaker.stop()
    print("\nMusic playback stopped")

except Exception as e:
    print(f"Error: {e}")
    speaker.stop()
