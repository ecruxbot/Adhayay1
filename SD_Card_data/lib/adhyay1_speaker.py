import audiocore
import audiopwmio
import time

class Adhyay1_Speaker:
    def __init__(self):
        self.audio = None
    
    def begin(self, pin):
        self.audio = audiopwmio.PWMAudioOut(pin)
    
    def play_music(self, filename):
        if not self.audio:
            raise RuntimeError("Call begin() first with pin number!")
        with open(filename, "rb") as f:
            wav = audiocore.WaveFile(f)
            self.audio.play(wav)
            while self.audio.playing:
                time.sleep(0.1)
    
    def stop(self):
        if self.audio:
            self.audio.stop()