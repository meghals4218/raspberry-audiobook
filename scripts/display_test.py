import time
import board
import digitalio
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789

spi = board.SPI()

cs_pin = digitalio.DigitalInOut(board.CE0)     # GPIO8
dc_pin = digitalio.DigitalInOut(board.D25)     # GPIO25
reset_pin = digitalio.DigitalInOut(board.D24)  # GPIO24

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    width=320,
    height=240,
    rotation=0,
    baudrate=8000000,
)

image = Image.new("RGB", (320, 240), "black")
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, 319, 239), outline="white")
draw.text((20, 30), "TFT TEST", fill="white")
draw.text((20, 70), "Rotation 0", fill="green")
draw.text((20, 110), "320 x 240", fill="yellow")

disp.image(image)

time.sleep(30)