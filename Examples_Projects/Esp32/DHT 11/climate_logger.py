# climate_logger.py - MicroPython version
import time
from adhyay1_dht import Adhyay1_DHT

# Initialize DHT11 sensor on GP20
dht = Adhyay1_DHT(20, sensor_type='DHT11')

print("Climate Data Logger")
print("Logging data every 5 seconds...")
print("Time\t\tTemperature\tHumidity")
print("-" * 40)

try:
    while True:
        # Get current time
        current_time = time.localtime()
        time_str = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
        
        # Read sensor data
        data = dht.read_all()
        
        if data['temperature'] is not None and data['humidity'] is not None:
            print(time_str + "\t" + str(data['temperature']) + "°C\t\t" + str(data['humidity']) + "%")
        else:
            print(time_str + "\tRead Error\tRead Error")
        
        time.sleep(5)  # Log every 5 seconds

except KeyboardInterrupt:
    print("\nData logging stopped")