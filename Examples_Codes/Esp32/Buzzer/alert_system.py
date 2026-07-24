# alert_system.py - MicroPython version
import time
from adhyay1_buzzer import Adhyay1_Buzzer

# Initialize passive buzzer on GP22
buzzer = Adhyay1_Buzzer(22, passive=True)

print("Alert System Demo")
print("Press Ctrl+C to stop")

try:
    while True:
        # Different alert types based on time
        current_second = time.localtime()[5]  # Get seconds from time tuple
        
        if current_second < 15:
            # Slow beeps for first 15 seconds
            print("Mode: Slow alert")
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
            time.sleep(1.5)
            
        elif current_second < 30:
            # Fast beeps for next 15 seconds
            print("Mode: Fast alert")
            buzzer.on()
            time.sleep(0.2)
            buzzer.off()
            time.sleep(0.3)
            
        elif current_second < 45:
            # High pitch alert
            print("Mode: High pitch")
            buzzer.tone(880)  # A5
            time.sleep(0.1)
            buzzer.off()
            time.sleep(0.4)
            
        else:
            # Low pitch alert
            print("Mode: Low pitch")
            buzzer.tone(220)  # A3
            time.sleep(0.2)
            buzzer.off()
            time.sleep(0.8)
            
except KeyboardInterrupt:
    buzzer.off()
    print("\nAlert system stopped")