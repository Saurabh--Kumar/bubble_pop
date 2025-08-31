import cv2
import numpy as np
from typing import Optional
import random

from objects.base_object import AbstractFallingObject
from config.game_config import config


class Bubble(AbstractFallingObject):
    """A bubble that falls from the top of the screen."""

    def __init__(self, x: float, y: float, radius: Optional[float] = None, speed: Optional[float] = None):
        if radius is None:
            radius = random.uniform(*config.BUBBLE_RADIUS_RANGE)
        if speed is None:
            speed = random.uniform(*config.BUBBLE_SPEED_RANGE)

        super().__init__(x=x, y=y, radius=radius, speed=speed, obj_type="bubble")
        self.color = config.COLOR_BUBBLE

    def draw(self, frame: np.ndarray) -> None:
        if not self.active:
            return

        center = (int(self.x), int(self.y))
        radius = int(self.radius)

        # Draw the bubble
        cv2.circle(frame, center, radius, self.color, -1)

        # Draw highlight
        highlight_color = (200, 200, 200)
        highlight_radius = int(self.radius * 0.3)
        highlight_x = int(self.x - self.radius * 0.4)
        highlight_y = int(self.y - self.radius * 0.4)
        cv2.circle(frame, (highlight_x, highlight_y), highlight_radius, highlight_color, -1)

        # Draw bubble outline
        cv2.circle(frame, center, radius, (255, 255, 255), 1)

    def reset(self, **kwargs) -> None:
        super().reset(**kwargs)
        if 'radius' not in kwargs:
            self.radius = random.uniform(*config.BUBBLE_RADIUS_RANGE)
        if 'speed' not in kwargs:
            self.speed = random.uniform(*config.BUBBLE_SPEED_RANGE)
