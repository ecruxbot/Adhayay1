import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_speaker import Adhyay1_Speaker

# Initialize speaker on GP28
speaker = Adhyay1_Speaker()
speaker.begin(board.GP28)

print("Sound Effects Player")
print("Playing various sound effects...")

# List of sound effects to play
sound_effects = [
    "/sd/sounds/beep.wav",
    "/sd/sounds/alert.wav", 
    "/sd/sounds/click.wav",
    "/sd/sounds/chime.wav",
    "/sd/sounds/notification.wav"
]

try:
    for sound_file in sound_effects:
        print(f"Playing: {sound_file}")
        try:
            speaker.play_music(sound_file)
            time.sleep(0.5)  # Short pause between sounds
        except Exception as e:
            print(f"Error playing {sound_file}: {e}")
    
    print("All sound effects played!")

except KeyboardInterrupt:
    speaker.stop()
    print("\nSound effects stopped")

except Exception as e:
    print(f"Error: {e}")
