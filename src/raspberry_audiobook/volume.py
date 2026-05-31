# volume.py

from gpiozero import Device, RotaryEncoder
from gpiozero.pins.lgpio import LGPIOFactory
import subprocess

Device.pin_factory = LGPIOFactory()

class VolumeController:
    def __init__(self):
        self.encoder = RotaryEncoder(a=16, b=20, max_steps=0)
        self.volume = 50
        self.last_steps = self.encoder.steps

        self.encoder.when_rotated = self.rotated

    def set_volume(self, v):
        self.volume = v
        subprocess.run(
            ["amixer", "set", "PCM", f"{v}%"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def rotated(self):
        if self.encoder.steps > self.last_steps:
            self.set_volume(min(100, self.volume + 1))
        else:
            self.set_volume(max(0, self.volume - 1))

        self.last_steps = self.encoder.steps