import time
import board
import digitalio
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789

spi = board.SPI()

cs_pin = digitalio.DigitalInOut(board.CE0)    # GPIO8
dc_pin = digitalio.DigitalInOut(board.D25)    # GPIO25
reset_pin = digitalio.DigitalInOut(board.D24) # GPIO24

rotations = [0, 90, 180, 270]

for rotation in rotations:
    print(f"Trying rotation {rotation}")

    disp = st7789.ST7789(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        width=320,
        height=240,
        rotation=rotation,
        baudrate=24000000,
    )

    image = Image.new("RGB", (320, 240), "black")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, 319, 239), outline="white")
    draw.text((20, 30), f"ROTATION {rotation}", fill="white")
    draw.text((20, 70), "TFT TEST", fill="green")
    draw.text((20, 110), "If readable, it works", fill="yellow")

    disp.image(image)
    time.sleep(5)