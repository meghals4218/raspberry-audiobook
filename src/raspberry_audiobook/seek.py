from collections.abc import Callable

from gpiozero import Device, RotaryEncoder
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()


class SeekController:
    def __init__(
        self,
        on_seek: Callable[[int], None],
        *,
        a_pin: int = 19,
        b_pin: int = 26,
        step_seconds: int = 10,
    ) -> None:
        self.encoder = RotaryEncoder(a=a_pin, b=b_pin, max_steps=0)
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
