import adhyay1_libs; adhyay1_libs.mount_sd()
import board
import time
from adhyay1_oled import Adhyay1_OLED

oled = Adhyay1_OLED(board.GP4, board.GP5)

print("Playing animation for 10 seconds...")

# Play animation for limited time
try:
    # Note: show_sprite_animation is blocking, so we can't use time.sleep()
    # For timed animation, we need to modify the library or use a different approach
    # This version will play until you press Ctrl+C
    
    oled.show_sprite_animation(
        image_path="/sd/animation/cat_jump_10.bmp",
        sprite_size=(128, 64),
        position=(0, 0),
        frame_count=10,
        speed=0.15,
        loop=True
    )
    
except KeyboardInterrupt:
    oled.clear()
    oled.show_data("Animation Stopped", x=10, y=30)
    print("Animation stopped by user")
