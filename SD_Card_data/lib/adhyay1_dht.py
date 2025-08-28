import adafruit_dht
import board
import time

class Adhyay1_DHT:
    import adafruit_dht
    import digitalio
    def __init__(self, pin, sensor_type='DHT11'):
        if sensor_type not in ['DHT11', 'DHT22']:
            raise ValueError("sensor_type must be 'DHT11' or 'DHT22'")

        self.pin = pin
        self.sensor_type = sensor_type
        self.dht_device = adafruit_dht.DHT11(pin) if sensor_type == 'DHT11' else adafruit_dht.DHT22(pin)

    def temperature(self):
        try:
            return self.dht_device.temperature
        except RuntimeError:
            return None

    def humidity(self):
        try:
            return self.dht_device.humidity
        except RuntimeError:
            return None

    def read_all(self):
        try:
            return {
                'temperature': self.dht_device.temperature,
                'humidity': self.dht_device.humidity
            }
        except RuntimeError:
            return {'temperature': None, 'humidity': None}

    def raw(self):
        return self.dht_device