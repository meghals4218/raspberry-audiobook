#!/usr/bin/env python3
"""TFT display test script for Raspberry Pi + Adafruit RGB TFT modules."""

import argparse
import sys
import time

try:
    import board
    import busio
    import digitalio
    import displayio
    from adafruit_display_text import label
    from adafruit_rgb_display import ili9341, st7735, st7789
    import terminalio
except ImportError as exc:
    print("Missing required Raspberry Pi display libraries.")
    print("Install dependencies with:")
    print("  python3 -m pip install adafruit-circuitpython-rgb-display adafruit-circuitpython-display-text")
    print(f"Import error: {exc}")
    sys.exit(1)

DRIVER_INFO = {
    "st7735": (st7735.ST7735, 128, 160),
    "ili9341": (ili9341.ILI9341, 320, 240),
    "st7789": (st7789.ST7789, 240, 240),
}

COLOR_STEPS = [
    (0xFF0000, "RED"),
    (0x00FF00, "GREEN"),
    (0x0000FF, "BLUE"),
    (0xFFFFFF, "WHITE"),
    (0x000000, "BLACK"),
]


def pin_from_name(name: str):
    try:
        return getattr(board, name)
    except AttributeError as exc:
        raise ValueError(f"Invalid board pin name: {name}") from exc


def init_spi(baudrate: int):
    spi = busio.SPI(board.SCK, MOSI=board.MOSI)
    while not spi.try_lock():
        pass
    spi.configure(baudrate=baudrate, phase=0, polarity=0)
    spi.unlock()
    return spi


def init_display(args, spi):
    driver_cls, width, height = DRIVER_INFO[args.display]

    cs = digitalio.DigitalInOut(pin_from_name(args.cs))
    dc = digitalio.DigitalInOut(pin_from_name(args.dc))
    rst = None
    if args.rst:
        rst = digitalio.DigitalInOut(pin_from_name(args.rst))

    release = getattr(displayio, "release_displays", None)
    if callable(release):
        release()

    return driver_cls(
        spi,
        cs=cs,
        dc=dc,
        rst=rst,
        rotation=args.rotation,
        width=width,
        height=height,
    )


def show_test_pattern(display, width, height, delay):
    bitmap = displayio.Bitmap(width, height, 1)
    palette = displayio.Palette(1)
    palette[0] = 0x000000

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
    group = displayio.Group()
    group.append(tile_grid)

    text_area = label.Label(
        terminalio.FONT,
        text="Starting display test...",
        color=0xFFFFFF,
        x=10,
        y=height - 20,
    )
    group.append(text_area)
    display.show(group)

    for color, name in COLOR_STEPS:
        text_area.text = f"{name} test"
        palette[0] = color
        time.sleep(delay)

    text_area.text = "Display test complete."
    palette[0] = 0x000000
    time.sleep(delay)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test an Adafruit RGB TFT display connected to Raspberry Pi."
    )
    parser.add_argument(
        "--display",
        choices=DRIVER_INFO,
        default="st7735",
        help="Display driver type.",
    )
    parser.add_argument(
        "--cs",
        default="D5",
        help="SPI chip select pin name on the Raspberry Pi board.",
    )
    parser.add_argument(
        "--dc",
        default="D6",
        help="Data/command pin name on the Raspberry Pi board.",
    )
    parser.add_argument(
        "--rst",
        default="D9",
        help="Reset pin name on the Raspberry Pi board (optional).",
    )
    parser.add_argument(
        "--rotation",
        type=int,
        default=90,
        help="Rotation of the display in degrees.",
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        default=24000000,
        help="SPI baud rate for the display.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=1.5,
        help="Seconds to show each color test.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        spi = init_spi(args.baudrate)
        display = init_display(args, spi)
    except ValueError as exc:
        print(exc)
        sys.exit(1)
    except Exception as exc:
        print(f"Failed to initialize display: {exc}")
        sys.exit(1)

    driver_cls, width, height = DRIVER_INFO[args.display]
    show_test_pattern(display, width, height, args.duration)


if __name__ == "__main__":
    main()
