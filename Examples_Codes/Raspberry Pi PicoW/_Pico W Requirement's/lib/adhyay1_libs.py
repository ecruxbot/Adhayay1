# adhyay1_libs.py
import board
import busio
import sdcardio
import storage
import sys


def mount_sd(spi_clk=board.GP18, spi_mosi=board.GP19, spi_miso=board.GP16, cs_pin=board.GP17):
    try:
        spi = busio.SPI(clock=spi_clk, MOSI=spi_mosi, MISO=spi_miso)
        cs = cs_pin
        sd = sdcardio.SDCard(spi, cs)
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, "/sd")
        sys.path.append("/sd/lib")
        print("Adhyay1 Libs Bundle Initiated")
    except Exception as e:
        print("❌ Failed to mount SD:", e)
