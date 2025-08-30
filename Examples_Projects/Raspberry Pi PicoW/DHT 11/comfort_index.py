import board
import time
from adhyay1_dht import Adhyay1_DHT

# Initialize DHT11 sensor on GP20
dht = Adhyay1_DHT(board.GP20, sensor_type='DHT11')

def calculate_comfort_index(temp, humidity):
    """Calculate simple comfort index"""
    # Simple comfort calculation (can be improved)
    if 20 <= temp <= 26 and 40 <= humidity <= 60:
        return "Perfect 😊"
    elif temp > 30 and humidity > 70:
        return "Hot and Humid 😓"
    elif temp < 15:
        return "Too Cold 🥶"
    elif humidity < 30:
        return "Too Dry 🏜️"
    elif humidity > 80:
        return "Too Humid 💦"
    else:
        return "Moderate 🙂"

print("Comfort Index Calculator")
print("Checking environment comfort...")

try:
    while True:
        data = dht.read_all()
        
        if data['temperature'] is not None and data['humidity'] is not None:
            temp = data['temperature']
            hum = data['humidity']
            
            comfort = calculate_comfort_index(temp, hum)
            
            print(f"🌡️ Temp: {temp}°C | 💧 Hum: {hum}%")
            print(f"💭 Comfort: {comfort}")
            print("-" * 35)
        else:
            print("❌ Sensor read error")
        
        time.sleep(4)  # Check every 4 seconds

except KeyboardInterrupt:
    print("\nComfort monitoring stopped")
