import board
import time
from adhyay1_tsop import IRRemote

# Initialize TSOP IR receiver on GP20
tsop = IRRemote(board.GP20)

print("IR Decoder")
print("Decoding IR remote signals...")
print("Press any button on your IR remote")
print("Press Ctrl+C to stop")

try:
    while True:
        decoded_data = tsop.decode()
        if decoded_data:
            print(f"Decoded: {decoded_data}")
            print(f"Hex: {[hex(x) for x in decoded_data]}")
            print("-" * 30)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nIR decoding stopped")
