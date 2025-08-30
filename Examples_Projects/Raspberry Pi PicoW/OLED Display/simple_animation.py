import board
import time
from adhyay1_oled import Adhyay1_OLED

# Initialize OLED display
oled = Adhyay1_OLED(sda_pin=board.GP4, scl_pin=board.GP5)

print("Simple GIF Animation")
print("Displaying cat_jump_10.bmp animation...")

# Animation configuration
ANIMATION_FILE = "/sd/animation/cat_jump_10.bmp"
FRAME_COUNT = 10  # Total frames in the sprite sheet
SPEED = 0.15      # Seconds per frame (adjust for speed)

try:
    # Display the animation
    oled.show_sprite_animation(
        image_path=ANIMATION_FILE,
        sprite_size=(128, 64),  # OLED display size
        position=(0, 0),        # Start from top-left corner
        frame_count=FRAME_COUNT,
        speed=SPEED,
        loop=True               # Keep looping the animation
    )
    
except Exception as e:
    print(f"Error: {e}")
    # Show error message on display
    oled.clear()
    oled.show_data("Animation Error", x=10, y=20)
    oled.show_data("Check SD Card", x=15, y=40)
    time.sleep(3)
