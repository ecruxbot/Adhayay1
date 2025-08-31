# simple_ir_receiver.py - MicroPython version
import time
from adhyay1_tsop import IRRemote

# Initialize TSOP IR receiver on GP20
tsop = IRRemote(20)

print("Simple IR Receiver")
print("Point your IR remote at the TSOP sensor...")
print("Press Ctrl+C to stop")

try:
    while True:
        raw_data = tsop.read_raw()
        if raw_data:
            print("Raw pulses:", len(raw_data), "pulses")
            if len(raw_data) > 0:
                print("First pulse:", raw_data[0], "us")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nIR receiver stopped")