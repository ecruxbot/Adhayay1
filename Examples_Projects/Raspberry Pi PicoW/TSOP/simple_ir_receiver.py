import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_tsop import IRRemote

# Initialize TSOP IR receiver on GP20
tsop = IRRemote(board.GP20)

print("Simple IR Receiver")
print("Point your IR remote at the TSOP sensor...")
print("Press Ctrl+C to stop")

try:
    while True:
        raw_data = tsop.read_raw()
        if raw_data:
            print(f"Raw pulses: {len(raw_data)} pulses")
            print(f"Data: {raw_data[:10]}...")  # Show first 10 pulses
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nIR receiver stopped")
