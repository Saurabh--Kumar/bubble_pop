from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np
from config.game_config import config


class AbstractFallingObject(ABC):
    """Base class for all falling objects (bubbles, power-ups, etc.)"""
    
    def __init__(self, x: float, y: float, radius: float, speed: float, obj_type: str):
        """
        Initialize a falling object.
        
        Args:
            x: Initial x position (center)
            y: Initial y position (center)
            radius: Radius of the object
            speed: Falling speed in pixels per second
            obj_type: Type of object (e.g., 'bubble', 'power')
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.type = obj_type
        self.active = True
    
    def update(self, dt: float):
        """
        Update the object's position.
        
        Args:
            dt: Time delta in seconds since last update
        """
        if not self.active:
            return
            
        self.y += self.speed * dt
    
    @abstractmethod
    def draw(self, frame):
        """
        Draw the object on the frame.
        
        Args:
            frame: OpenCV frame to draw on
        """
        pass
    
    def is_hit(self, position: Tuple[float, float]) -> bool:
        """
        Check if the object is hit by a position (e.g., fist position).
        
        Args:
            position: (x, y) coordinates to check
            
        Returns:
            bool: True if the position is inside the object's radius
        """
        if not self.active:
            return False
            
        x, y = position
        distance = np.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance <= self.radius
    
    def is_off_screen(self) -> bool:
        """
        Check if the object is off the bottom of the screen.
        
        Returns:
            bool: True if the object is off screen
        """
        return self.y - self.radius > config.WINDOW_HEIGHT
    
    def reset(self, x: Optional[float] = None, y: Optional[float] = None, 
              radius: Optional[float] = None, speed: Optional[float] = None):
        """
        Reset the object's properties for reuse.
        
        Args:
            x: New x position (optional)
            y: New y position (optional)
            radius: New radius (optional)
            speed: New speed (optional)
        """
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if radius is not None:
            self.radius = radius
        if speed is not None:
            self.speed = speed
            
        self.active = True
    
    def deactivate(self):
        """Mark the object as inactive so it can be reused."""
        self.active = False
