# temp_monitor.py - MicroPython version
import time
from adhyay1_dht import Adhyay1_DHT

# Initialize DHT11 sensor on GP20
dht = Adhyay1_DHT(20, sensor_type='DHT11')

print("Temperature Monitor")
print("Monitoring for high temperature...")

try:
    while True:
        data = dht.read_all()
        
        if data['temperature'] is not None and data['humidity'] is not None:
            temp = data['temperature']
            hum = data['humidity']
            
            print("Temp:", temp, "°C, Humidity:", hum, "%")
            
            # Check temperature conditions
            if temp > 30:
                print("HIGH TEMPERATURE ALERT! (>30°C)")
            elif temp < 15:
                print("LOW TEMPERATURE ALERT! (<15°C)")
            else:
                print("Temperature normal")
                
        else:
            print("Failed to read sensor")
        
        print("-" * 30)
        time.sleep(3)  # Read every 3 seconds

except KeyboardInterrupt:
    print("\nTemperature monitoring stopped")