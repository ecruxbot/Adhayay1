import board
import time
from adhyay1_oled import Adhyay1_OLED

# Initialize OLED display
oled = Adhyay1_OLED(sda_pin=board.GP4, scl_pin=board.GP5)

print("Multi-Page Display")
print("Cycling through different pages...")

# Different display pages
pages = [
    {
        "title": "SYSTEM INFO",
        "lines": [
            "Board: Pico W",
            "CPU: RP2040",
            "RAM: 264KB",
            "Flash: 2MB"
        ]
    },
    {
        "title": "NETWORK STATS",
        "lines": [
            "WiFi: Connected",
            "IP: 192.168.1.100",
            "Signal: Excellent",
            "Uptime: 12:34:56"
        ]
    },
    {
        "title": "SENSOR DATA",
        "lines": [
            "Temp: 25.6°C",
            "Humidity: 45%",
            "Light: 78%",
            "Motion: None"
        ]
    }
]

try:
    page_index = 0
    while True:
        # Get current page
        page = pages[page_index]
        
        # Display page
        oled.clear()
        oled.show_data(page["title"], x=15, y=5, clear=False)
        
        # Display each line
        for i, line in enumerate(page["lines"]):
            oled.show_data(line, x=5, y=20 + i*12, clear=False)
        
        print(f"Displaying page: {page['title']}")
        
        # Move to next page
        page_index = (page_index + 1) % len(pages)
        time.sleep(3)  # Show each page for 3 seconds

except KeyboardInterrupt:
    oled.clear()
    oled.show_data("Demo Stopped", x=20, y=30)
    print("\nMulti-page display stopped")
