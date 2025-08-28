import board
import busio
import displayio
import time
import adafruit_displayio_ssd1306
import adafruit_imageload
from adafruit_display_text import label
import terminalio


class Adhyay1_OLED:
    def __init__(self, sda_pin=board.GP4, scl_pin=board.GP5, address=0x3C, width=128, height=64):
        """
        Initialize OLED with custom SDA/SCL pins (I2C).
        """
        displayio.release_displays()  # Free pins if previously used
        self.i2c = busio.I2C(scl_pin, sda_pin)
        display_bus = displayio.I2CDisplay(self.i2c, device_address=address)
        self.display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=width, height=height)
        self.group = displayio.Group()
        self.display.root_group = self.group

    def clear(self):
        """Clear display group."""
        while len(self.group) > 0:
            self.group.pop()

    def show_data(self, text, x=0, y=0, clear=True):
        """Show text on OLED."""
        if clear:
            self.clear()
        text_area = label.Label(terminalio.FONT, text=text)
        text_area.x = x
        text_area.y = y
        self.group.append(text_area)

    def show_image(self, file_path, x=0, y=0, clear=True):
        """Show BMP image from SD card."""
        try:
            if clear:
                self.clear()
            bitmap, palette = adafruit_imageload.load(file_path)
            tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y)
            self.group.append(tile_grid)
            return True
        except Exception as e:
            print(f"Image error: {e}")
            return False

    def show_sprite_animation(self, image_path, sprite_size, position, frame_count, speed=0.1, loop=False):
        """
        High-speed sprite sheet animation.
        - image_path: Path to BMP file (sprite sheet)
        - sprite_size: (frame_width, frame_height)
        - position: (x, y) on display
        - frame_count: Total frames in the sheet
        - speed: Seconds per frame
        - loop: Loop forever if True
        """
        try:
            bitmap, palette = adafruit_imageload.load(image_path)
            frame_width, frame_height = sprite_size

            # Create TileGrid once for max speed
            tile = displayio.TileGrid(
                bitmap,
                pixel_shader=palette,
                width=1,
                height=1,
                tile_width=frame_width,
                tile_height=frame_height,
                x=position[0],
                y=position[1]
            )

            self.clear()
            self.group.append(tile)

            current_frame = 0
            while True:
                tile[0] = current_frame
                time.sleep(speed)
                current_frame = (current_frame + 1) % frame_count

                if not loop and current_frame == 0:
                    break

        except Exception as e:
            print(f"Sprite animation error: {e}")
