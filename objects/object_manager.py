from __future__ import annotations
import random
from typing import List, Type
import numpy as np
from objects.bubble import Bubble
from objects.power import Power
from objects.base_object import AbstractFallingObject
from config.game_config import config, PowerType, GameConfig


class ObjectManager:
    """Manages all active game objects, including spawning, updating, and pooling."""

    def __init__(self, max_objects: int = 100):
        self.max_objects = max_objects
        self.objects: List[AbstractFallingObject] = []
        self._object_pool: Dict[str, List[AbstractFallingObject]] = {
            'bubble': [],
            'power': []
        }

    def update_all(self, dt: float) -> None:
        """Update all active objects and remove inactive ones."""
        for obj in self.objects[:]:
            obj.update(dt)
            if not obj.active:
                self.remove_object(obj)

    def draw_all(self, frame: np.ndarray) -> None:
        """Draw all active objects on the frame."""
        for obj in self.objects:
            obj.draw(frame)

    def spawn_bubble(self) -> Bubble:
        """Get a bubble from the pool or create a new one and add it to the game."""
        margin = config.WINDOW_WIDTH * 0.1
        x = random.uniform(margin, config.WINDOW_WIDTH - margin)
        y = -50.0

        bubble = self._get_from_pool(GameConfig.BUBBLE, Bubble, x=x, y=y)
        self.objects.append(bubble)
        return bubble

    def spawn_power(self) -> Power:
        """Get a power-up from the pool or create a new one and add it to the game."""
        margin = config.WINDOW_WIDTH * 0.1
        x = random.uniform(margin, config.WINDOW_WIDTH - margin)
        y = -50.0

        power = self._get_from_pool(GameConfig.POWER, Power, x=x, y=y)
        self.objects.append(power)
        return power

    def get_objects(self, obj_type: Optional[str] = None) -> List[AbstractFallingObject]:
        """Return a list of all active objects, optionally filtered by type."""
        if obj_type:
            return [obj for obj in self.objects if obj.type == obj_type]
        return self.objects

    def remove_object(self, obj: AbstractFallingObject) -> None:
        """Remove an object from the active list and return it to the pool."""
        if obj in self.objects:
            self.objects.remove(obj)
            self._return_to_pool(obj)

    def remove_all(self, obj_type: Optional[str] = None) -> None:
        """Remove all objects, optionally filtered by type."""
        objects_to_remove = self.get_objects(obj_type)
        for obj in objects_to_remove[:]:
            self.remove_object(obj)

    def freeze_all(self, freeze: bool = True) -> None:
        """Freeze or unfreeze all bubbles."""
        for obj in self.get_objects(GameConfig.BUBBLE):
            obj.frozen = freeze

    def reset(self) -> None:
        """Reset the object manager by clearing all objects and pools."""
        self.objects.clear()
        for pool in self._object_pool.values():
            pool.clear()

    def _get_from_pool(self, obj_type: str, constructor: type, **kwargs) -> AbstractFallingObject:
        """Retrieve an object from the pool or create a new one if the pool is empty."""
        pool = self._object_pool[obj_type]
        if pool:
            obj = pool.pop()
            obj.reset(**kwargs)
            return obj
        return constructor(**kwargs)

    def _return_to_pool(self, obj: AbstractFallingObject) -> None:
        """Return an inactive object to the appropriate pool."""
        if obj.type in self._object_pool:
            obj.deactivate()
            self._object_pool[obj.type].append(obj)
