import cv2
import numpy as np
from enum import Enum
from typing import Optional, Tuple

from .base_object import AbstractFallingObject
from config.game_config import config, PowerType

class Power(AbstractFallingObject):
    """A power-up that falls from the top of the screen."""
    
    # Power-up properties
    POWER_RADIUS = 25
    POWER_SPEED = 50.0
    
    # Colors for different power types
    POWER_COLORS = {
        PowerType.FREEZE: config.COLOR_POWER_FREEZE,
        PowerType.DESTROY: config.COLOR_POWER_DESTROY,
        PowerType.HEAL: config.COLOR_POWER_HEAL
    }
    
    def __init__(self, x: float, y: float, power_type: Optional[PowerType] = None):
        """
        Initialize a power-up.
        
        Args:
            x: Initial x position (center)
            y: Initial y position (center)
            power_type: Type of power-up (random if None)
        """
        if power_type is None:
            power_type = np.random.choice(list(PowerType))
            
        super().__init__(x, y, self.POWER_RADIUS, self.POWER_SPEED, "power")
        
        self.power_type = power_type
        self.angle = 0
        self.pulse_timer = 0
        self.pulse_speed = 2.0  # radians per second
    
    def update(self, dt: float):
        """
        Update the power-up's position and animation.
        
        Args:
            dt: Time delta in seconds since last update
        """
        if not self.active:
            return
            
        super().update(dt)
        
        # Update animation
        self.pulse_timer += dt * self.pulse_speed
        self.angle = (self.angle + dt * 1.5) % (2 * np.pi)
    
    def draw(self, frame):
        """
        Draw the power-up on the frame.
        
        Args:
            frame: OpenCV frame to draw on
        """
        if not self.active:
            return
            
        # Get color based on power type
        color = self.POWER_COLORS.get(self.power_type, (255, 255, 255))
        
        # Calculate pulse effect
        pulse = np.sin(self.pulse_timer) * 0.2 + 0.9  # 0.7 to 1.1 scale
        radius = int(self.radius * pulse)
        
        # Draw glow/aura
        overlay = frame.copy()
        cv2.circle(overlay, (int(self.x), int(self.y)), 
                  radius + 5, (*color[:3], 0.3), -1)
        alpha = 0.5
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Draw main circle
        cv2.circle(frame, (int(self.x), int(self.y)), 
                  radius, color, -1)
        
        # Draw outline
        cv2.circle(frame, (int(self.x), int(self.y)), 
                  radius, (255, 255, 255), 1)
        
        # Draw power symbol
        self._draw_power_symbol(frame, color)
    
    def _draw_power_symbol(self, frame, color):
        """Draw the symbol for the power-up."""
        text = self.power_type.value  # 'F', 'D', or 'H'
        
        # Calculate text size and position
        font_scale = 0.8
        thickness = 2
        (text_width, text_height), _ = cv2.getTextSize(
            text, config.FONT_FACE, font_scale, thickness)
        
        text_x = int(self.x - text_width // 2)
        text_y = int(self.y + text_height // 2)
        
        # Draw text shadow
        cv2.putText(frame, text, (text_x + 1, text_y + 1), 
                   config.FONT_FACE, font_scale, 
                   (0, 0, 0), thickness)
        
        # Draw main text
        cv2.putText(frame, text, (text_x, text_y), 
                   config.FONT_FACE, font_scale, 
                   (255, 255, 255), thickness)
    
    def reset(self, x: Optional[float] = None, y: Optional[float] = None, 
              power_type: Optional[PowerType] = None):
        """
        Reset the power-up's properties for reuse.
        
        Args:
            x: New x position (random if None)
            y: New y position (random if None)
            power_type: Type of power-up (random if None)
        """
        if x is None:
            # Keep power-ups within 10-90% of screen width for better interaction
            margin = config.WINDOW_WIDTH * 0.1
            x = np.random.uniform(margin, config.WINDOW_WIDTH - margin)
            
        if y is None:
            y = -self.radius * 2  # Start above the screen
            
        if power_type is None:
            power_type = np.random.choice(list(PowerType))
        
        super().reset(x, y, self.POWER_RADIUS, self.POWER_SPEED)
        self.power_type = power_type
        self.angle = 0
        self.pulse_timer = 0
