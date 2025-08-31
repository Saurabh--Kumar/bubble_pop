from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
import cv2


class IGameObject(ABC):
    """Interface for any object that can be updated and drawn."""

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, frame: np.ndarray) -> None:
        pass


class AbstractFallingObject(IGameObject, ABC):
    """Abstract base class for objects that fall from the top of the screen."""

    def __init__(self, x: float, y: float, speed: float, radius: float, obj_type: str):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.type = obj_type
        self.active = True
        self.frozen = False
        self.original_speed = speed

    def update(self, dt: float) -> None:
        if not self.frozen:
            self.y += self.speed * dt
        if self.y - self.radius > 720:  # Assuming screen height of 720
            self.deactivate()

    def draw(self, frame: np.ndarray) -> None:
        if self.active:
            center = (int(self.x), int(self.y))
            cv2.circle(frame, center, int(self.radius), (255, 0, 0), -1)

    def is_hit(self, fist_pos: Tuple[int, int]) -> bool:
        if not self.active:
            return False
        distance = np.sqrt((self.x - fist_pos[0]) ** 2 + (self.y - fist_pos[1]) ** 2)
        return distance <= self.radius

    def is_off_screen(self, height: int) -> bool:
        """Check if the object is off the screen."""
        return self.y > height + self.radius

    def reset(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.active = True
        self.frozen = False

    def deactivate(self) -> None:
        self.active = False
