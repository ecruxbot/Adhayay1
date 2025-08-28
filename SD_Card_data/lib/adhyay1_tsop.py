import pulseio
import adafruit_irremote

class IRRemote:
    def __init__(self, pin):
        self.pulse_in = pulseio.PulseIn(pin, maxlen=120, idle_state=True)
        self.decoder = adafruit_irremote.GenericDecode()
        self.button_codes = {}

    def set_button_codes(self, mapping):
        self.button_codes = mapping

    def read_raw(self):
        try: return self.decoder.read_pulses(self.pulse_in)
        except: return None

    def decode(self):
        try: return self.decoder.decode_bits(self.read_raw())
        except: return None

    def get_button(self):
        code = self.decode()
        return self.button_codes.get(tuple(code), code)
