import busio, time

class Adhyay1_Bluetooth:
    def __init__(self, tx, rx, baudrate=9600):
        self.uart = busio.UART(tx=tx, rx=rx, baudrate=baudrate)
        time.sleep(1)

    def read(self):
        data = self.uart.read(32)
        if data:
            try: return data.decode('utf-8').strip()
            except: return None

    def write(self, msg):
        self.uart.write((msg + '\n').encode())
