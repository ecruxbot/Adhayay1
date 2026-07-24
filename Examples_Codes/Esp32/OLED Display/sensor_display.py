# sensor_display.py - MicroPython version
import time
from adhyay1_oled import Adhyay1_OLED

# Initialize OLED display
oled = Adhyay1_OLED(sda_pin=4, scl_pin=5)

print("Sensor Data Display")
print("Showing simulated sensor data...")

# Simulated sensor data display
try:
    counter = 0
    while True:
        # Simulate sensor readings
        temp = 25 + (counter % 10) / 2
        hum = 50 + (counter % 15)
        pressure = 1013 + (counter % 5)
        
        # Update OLED display
        oled.clear()
        oled.show_data("SENSOR MONITOR", x=5, y=5, clear=False)
        oled.show_data("Temp: {:.1f} C".format(temp), x=5, y=20, clear=False)
        oled.show_data("Hum:  {}%".format(hum), x=5, y=35, clear=False)
        oled.show_data("Press: {} hPa".format(pressure), x=5, y=50, clear=False)
        
        print("Displaying: Temp={:.1f}C, Hum={}%".format(temp, hum))
        counter += 1
        time.sleep(1)

except KeyboardInterrupt:
    oled.clear()
    oled.show_data("Monitor Stopped", x=10, y=30)
    print("\nSensor display stopped")