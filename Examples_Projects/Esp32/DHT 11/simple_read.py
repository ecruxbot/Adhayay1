# simple_read.py - MicroPython version
import time
from adhyay1_dht import Adhyay1_DHT

# Initialize DHT11 sensor on GP20
dht = Adhyay1_DHT(20, sensor_type='DHT11')

print("Simple DHT11 Reading")
print("Press Ctrl+C to stop")

try:
    while True:
        # Read temperature and humidity
        temp = dht.temperature()
        hum = dht.humidity()
        
        if temp is not None and hum is not None:
            print("Temperature:", temp, "°C")
            print("Humidity:", hum, "%")
            print("-" * 20)
        else:
            print("Sensor read error")
        
        time.sleep(2)  # Wait 2 seconds between readings

except KeyboardInterrupt:
    print("\nDHT11 reading stopped")