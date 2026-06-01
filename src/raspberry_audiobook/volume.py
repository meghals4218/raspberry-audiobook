from collections.abc import Callable

from gpiozero import Device, RotaryEncoder
from gpiozero.pins.lgpio import LGPIOFactory


Device.pin_factory = LGPIOFactory()


class VolumeController:
    def __init__(
        self,
        on_change: Callable[[int], None],
        *,
        a_pin: int = 16,
        b_pin: int = 20,
        initial_volume: int = 50,
        step: int = 5,
    ) -> None:
        self.encoder = RotaryEncoder(a=a_pin, b=b_pin, max_steps=0)
        self.last_steps = self.encoder.steps
        self.on_change = on_change
        self.volume = self._clamp(initial_volume)
        self.step = step

        self.on_change(self.volume)
        self.encoder.when_rotated = self.rotated

    def rotated(self) -> None:
        steps = self.encoder.steps

        if steps > self.last_steps:
            self.set_volume(self.volume + self.step)
        else:
            self.set_volume(self.volume - self.step)

        self.last_steps = steps

    def set_volume(self, volume: int) -> None:
        previous_volume = self.volume
        self.volume = self._clamp(volume)
        self.on_change(self.volume)

        if self.volume != previous_volume:
            print(f"Volume: {self.volume}%")

    def _clamp(self, volume: int) -> int:
        return max(0, min(100, volume))
