import board
import time
from adhyay1_dht import Adhyay1_DHT

# Initialize DHT11 sensor on GP20
dht = Adhyay1_DHT(board.GP20, sensor_type='DHT11')

print("Climate Data Logger")
print("Logging data every 5 seconds...")
print("Time\t\tTemperature\tHumidity")
print("-" * 40)

try:
    while True:
        # Get current time
        current_time = time.localtime()
        time_str = f"{current_time.tm_hour:02d}:{current_time.tm_min:02d}:{current_time.tm_sec:02d}"
        
        # Read sensor data
        data = dht.read_all()
        
        if data['temperature'] is not None and data['humidity'] is not None:
            print(f"{time_str}\t{data['temperature']}°C\t\t{data['humidity']}%")
        else:
            print(f"{time_str}\tRead Error\tRead Error")
        
        time.sleep(5)  # Log every 5 seconds

except KeyboardInterrupt:
    print("\nData logging stopped")
