import cv2
import numpy as np
from typing import Optional, Dict, Tuple
import random

from objects.base_object import AbstractFallingObject
from config.game_config import config, PowerType


class Power(AbstractFallingObject):
    """A power-up that falls from the top of the screen."""

    POWER_RADIUS = 25
    POWER_SPEED = 50.0
    POWER_COLORS: Dict[PowerType, Tuple[int, int, int]] = {
        PowerType.FREEZE: config.COLOR_POWER_FREEZE,
        PowerType.DESTROY: config.COLOR_POWER_DESTROY,
        PowerType.HEALTH: config.COLOR_POWER_HEALTH,
    }

    def __init__(self, x: float, y: float, power_type: Optional[PowerType] = None):
        if power_type is None:
            power_type = random.choice(list(PowerType))

        super().__init__(x=x, y=y, radius=self.POWER_RADIUS, speed=self.POWER_SPEED, obj_type="power")
        self.power_type = power_type
        self.pulse_timer = 0.0
        self.pulse_speed = 2.0  # Radians per second

    def draw(self, frame: np.ndarray) -> None:
        if not self.active:
            return

        color = self.POWER_COLORS.get(self.power_type, (255, 255, 255))
        pulse = np.sin(self.pulse_timer) * 0.1 + 1.0  # Pulse between 0.9 and 1.1
        radius = int(self.radius * pulse)
        center = (int(self.x), int(self.y))

        # Draw main circle
        cv2.circle(frame, center, radius, color, -1)
        # Draw outline
        cv2.circle(frame, center, radius, (255, 255, 255), 1)
        # Draw power symbol
        self._draw_power_symbol(frame)

    def update(self, dt: float) -> None:
        super().update(dt)
        self.pulse_timer += dt * self.pulse_speed

    def _draw_power_symbol(self, frame: np.ndarray) -> None:
        text = self.power_type.value
        font_scale = 0.8
        thickness = 2
        (text_width, text_height), _ = cv2.getTextSize(text, config.FONT_FACE, font_scale, thickness)
        text_x = int(self.x - text_width / 2)
        text_y = int(self.y + text_height / 2)

        # Draw text shadow
        cv2.putText(frame, text, (text_x + 1, text_y + 1), config.FONT_FACE, font_scale, (0, 0, 0), thickness)
        # Draw main text
        cv2.putText(frame, text, (text_x, text_y), config.FONT_FACE, font_scale, (255, 255, 255), thickness)

    def reset(self, **kwargs) -> None:
        super().reset(**kwargs)
        if 'power_type' not in kwargs:
            self.power_type = random.choice(list(PowerType))
        self.pulse_timer = 0.0
