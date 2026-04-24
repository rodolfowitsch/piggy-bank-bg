"""Coin drop animation state machine."""

import time
from dataclasses import dataclass, field

from .easing import coin_drop


@dataclass
class CoinAnimation:
    active: bool = False
    start_time: float = 0.0
    duration: float = 1.0  # seconds
    # Normalized coords: coin falls from above to the piggy bank slot (top right)
    start_pos: tuple[float, float] = (0.78, -0.1)
    end_pos: tuple[float, float] = (0.78, 0.13)
    saying: str = ""
    show_text_until: float = 0.0

    def trigger(self, saying: str = ""):
        self.active = True
        self.start_time = time.monotonic()
        self.saying = saying
        self.show_text_until = self.start_time + self.duration + 3.0

    def get_state(self) -> dict:
        now = time.monotonic()
        text_visible = now < self.show_text_until and self.saying

        if not self.active:
            return {
                "coin_visible": False,
                "text_visible": bool(text_visible),
                "saying": self.saying,
            }

        elapsed = now - self.start_time
        t = min(elapsed / self.duration, 1.0)
        progress = coin_drop(t)

        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress

        # Coin rotates during fall: 2 full rotations
        angle = t * 720.0

        if t >= 1.0:
            self.active = False

        return {
            "coin_visible": True,
            "coin_x": x,
            "coin_y": y,
            "coin_angle": angle,
            "text_visible": True,
            "saying": self.saying,
        }
