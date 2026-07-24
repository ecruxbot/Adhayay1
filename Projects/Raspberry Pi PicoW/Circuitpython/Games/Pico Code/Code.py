import adhyay1_libs
adhyay1_libs.mount_sd()

import board
import busio
import time
from adhyay1_mpu6050 import Adhyay1_MPU6050
import digitalio
import rotaryio

print("=====================================")
print("   🎮 PICO UNIVERSAL CONTROLLER")
print("=====================================")

# --- IMU Setup ---
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
mpu = Adhyay1_MPU6050(i2c)
print("✅ IMU Connected")

# --- Button Setup ---
button = digitalio.DigitalInOut(board.GP21)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
print("✅ Button Connected on GP15")

# --- Encoder Setup ---
try:
    encoder = rotaryio.IncrementalEncoder(board.GP12, board.GP13)
    last_position = 0
    print("✅ Encoder Connected")
except:
    encoder = None
    print("⚠️ Encoder Disabled")

print("=====================================")

# --- Calibration ---
print("Calibrating IMU...")
time.sleep(2)

offset_x = 0
offset_y = 0
samples = 100

for i in range(samples):
    try:
        accel = mpu.get_accel()
        offset_x += accel[0]
        offset_y += accel[1]
    except:
        pass
    time.sleep(0.01)

offset_x /= samples
offset_y /= samples

print(f"✅ Calibration Done!")
print("=====================================")

# --- Smoothing ---
readings_x = []
readings_y = []
WINDOW = 5

# --- State Variables ---
last_button = True
button_hold_counter = 0
encoder_enabled = (encoder is not None)

print("📡 SENDING DATA...")
print("=====================================")
print("")

# --- Main Loop ---
try:
    while True:
        # --- BUTTON ---
        button_state = button.value
        
        if button_state != last_button:
            if not button_state:
                print("BTN:1")
            else:
                print("BTN:0")
            last_button = button_state
        
        # Button hold
        if not button_state:
            button_hold_counter += 1
            if button_hold_counter % 3 == 0:
                print("BTN_HOLD")
        else:
            button_hold_counter = 0
        
        # --- IMU ---
        try:
            accel = mpu.get_accel()
            x = accel[0] - offset_x
            y = accel[1] - offset_y
            
            readings_x.append(x)
            if len(readings_x) > WINDOW:
                readings_x.pop(0)
            avg_x = sum(readings_x) / len(readings_x)
            
            readings_y.append(y)
            if len(readings_y) > WINDOW:
                readings_y.pop(0)
            avg_y = sum(readings_y) / len(readings_y)
            
            print(f"IMU:{round(avg_x, 2)},{round(avg_y, 2)}")
            
        except:
            pass
        
        # --- ENCODER ---
        if encoder_enabled:
            try:
                current_position = encoder.position
                if current_position != last_position:
                    print(f"ENC:{current_position}")
                    last_position = current_position
            except:
                encoder_enabled = False
        
        time.sleep(0.02)
        
except KeyboardInterrupt:
    print("")
    print("🛑 Stopped!")
