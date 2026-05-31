from gpiozero import Device, RotaryEncoder
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()


class SeekController:
    def __init__(self, on_seek, step_seconds: int = 10) -> None:
        self.encoder = RotaryEncoder(a=19, b=26, max_steps=0)
        self.last_steps = self.encoder.steps
        self.on_seek = on_seek
        self.step_seconds = step_seconds

        self.encoder.when_rotated = self.rotated

    def rotated(self) -> None:
        steps = self.encoder.steps

        if steps > self.last_steps:
            self.on_seek(+self.step_seconds)
        else:
            self.on_seek(-self.step_seconds)

        self.last_steps = steps