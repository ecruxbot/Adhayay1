import board
from adhyay1_oled import Adhyay1_OLED

# Initialize and play animation directly
oled = Adhyay1_OLED(board.GP4, board.GP5)

# Play the animation (this will run forever in loop)
oled.show_sprite_animation(
    image_path="/sd/animation/cat_jump_10.bmp",
    sprite_size=(128, 64),
    position=(0, 0),
    frame_count=10,
    speed=0.15,
    loop=True
)
