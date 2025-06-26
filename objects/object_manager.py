import random
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from config.game_config import config, PowerType
from objects.base_object import AbstractFallingObject
from objects.bubble import Bubble
from objects.power import Power

class ObjectManager:
    """Manages all game objects (bubbles, power-ups, etc.)"""
    
    def __init__(self, max_objects: int = 100):
        """
        Initialize the object manager.
        
        Args:
            max_objects: Maximum number of objects to manage
        """
        self.max_objects = max_objects
        self.objects: List[AbstractFallingObject] = []
        self._object_pool = {
            'bubble': [],
            'power': []
        }
    
    def update_all(self, dt: float):
        """
        Update all active objects.
        
        Args:
            dt: Time delta in seconds since last update
        """
        for obj in self.objects[:]:  # Iterate over a copy to allow removal
            if not obj.active:
                self.objects.remove(obj)
                self._return_to_pool(obj)
            else:
                obj.update(dt)
    
    def draw_all(self, frame):
        """
        Draw all active objects.
        
        Args:
            frame: OpenCV frame to draw on
        """
        for obj in self.objects:
            if obj.active:
                obj.draw(frame)
    
    def spawn_bubble(self, x: Optional[float] = None, y: Optional[float] = None) -> Bubble:
        """
        Spawn a new bubble.
        
        Args:
            x: X position (random if None)
            y: Y position (top of screen if None)
            
        Returns:
            The spawned bubble
        """
        if x is None:
            # Keep bubbles within 10-90% of screen width for better pop detection
            margin = config.WINDOW_WIDTH * 0.1
            x = random.uniform(margin, config.WINDOW_WIDTH - margin)
            
        if y is None:
            y = -50  # Start above the screen
            
        # Try to get from pool first
        bubble = self._get_from_pool('bubble')
        if bubble is None:
            bubble = Bubble(x, y)
        else:
            bubble.reset(x, y)
            
        self.objects.append(bubble)
        return bubble
    
    def spawn_power(self, power_type=None, x: Optional[float] = None, 
                   y: Optional[float] = None) -> Optional[Power]:
        """
        Spawn a new power-up.
        
        Args:
            power_type: Type of power-up (random if None)
            x: X position (random if None)
            y: Y position (top of screen if None)
            
        Returns:
            The spawned power-up, or None if max objects reached
        """
        if x is None:
            # Keep power-ups within 10-90% of screen width for better interaction
            margin = config.WINDOW_WIDTH * 0.1
            x = random.uniform(margin, config.WINDOW_WIDTH - margin)
            
        if y is None:
            y = -50  # Start above the screen
            
        # Try to get from pool first
        power = self._get_from_pool('power')
        if power is None:
            power = Power(x, y, power_type)
        else:
            power.reset(x, y, power_type)
            
        self.objects.append(power)
        return power
    
    def get_objects(self, obj_type: Optional[str] = None) -> List[AbstractFallingObject]:
        """
        Get all objects of a specific type.
        
        Args:
            obj_type: Type of objects to get (None for all)
            
        Returns:
            List of objects
        """
        if obj_type is None:
            return self.objects
        return [obj for obj in self.objects if obj.type == obj_type]
    
    def remove_object(self, obj: AbstractFallingObject):
        """
        Remove an object from the active list and return it to the pool.
        
        Args:
            obj: Object to remove
        """
        if obj in self.objects:
            self.objects.remove(obj)
            self._return_to_pool(obj)
    
    def remove_all(self, obj_type: Optional[str] = None):
        """
        Remove all objects of a specific type.
        
        Args:
            obj_type: Type of objects to remove (None for all)
        """
        if obj_type is None:
            for obj in self.objects[:]:
                self._return_to_pool(obj)
            self.objects = []
        else:
            for obj in self.objects[:]:
                if obj.type == obj_type:
                    self.objects.remove(obj)
                    self._return_to_pool(obj)
    
    def freeze_all(self, freeze: bool = True):
        """
        Freeze or unfreeze all objects.
        
        Args:
            freeze: Whether to freeze (True) or unfreeze (False)
        """
        for obj in self.objects:
            if hasattr(obj, 'frozen'):
                obj.frozen = freeze
            elif hasattr(obj, 'speed'):
                if freeze:
                    obj.original_speed = obj.speed
                    obj.speed = 0
                else:
                    if hasattr(obj, 'original_speed'):
                        obj.speed = obj.original_speed
    
    def reset(self):
        """Reset the object manager, clearing all objects."""
        self.remove_all()
        self._object_pool = {
            'bubble': [],
            'power': []
        }
    
    def _get_from_pool(self, obj_type: str) -> Optional[AbstractFallingObject]:
        """
        Get an object from the pool if available.
        
        Args:
            obj_type: Type of object to get
            
        Returns:
            The object, or None if pool is empty
        """
        if not self._object_pool[obj_type]:
            return None
            
        # Get the first available object
        for i, obj in enumerate(self._object_pool[obj_type]):
            if not obj.active:
                return self._object_pool[obj_type].pop(i)
                
        return None
    
    def _return_to_pool(self, obj: AbstractFallingObject):
        """
        Return an object to the pool for reuse.
        
        Args:
            obj: Object to return to the pool
        """
        if obj.type in self._object_pool:
            obj.deactivate()
            self._object_pool[obj.type].append(obj)
