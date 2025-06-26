import cv2
import numpy as np
from typing import Optional

from objects.base_object import AbstractFallingObject
from config.game_config import config


class Bubble(AbstractFallingObject):
    """A bubble that falls from the top of the screen."""
    
    def __init__(self, x: float, y: float, radius: Optional[float] = None, 
                 speed: Optional[float] = None):
        """
        Initialize a bubble.
        
        Args:
            x: Initial x position (center)
            y: Initial y position (center)
            radius: Radius of the bubble (random if None)
            speed: Falling speed in pixels per second (random if None)
        """
        if radius is None:
            radius = np.random.uniform(*config.BUBBLE_RADIUS_RANGE)
            
        if speed is None:
            speed = np.random.uniform(*config.BUBBLE_SPEED_RANGE)
        
        super().__init__(x, y, radius, speed, "bubble")
        
        # Bubble properties
        self.highlight = False
        self.highlight_timer = 0
        self.highlight_duration = 0.2  # seconds
    
    def update(self, dt: float):
        """
        Update the bubble's position and state.
        
        Args:
            dt: Time delta in seconds since last update
        """
        if not self.active:
            return
            
        super().update(dt)
        
        # Update highlight timer
        if self.highlight:
            self.highlight_timer -= dt
            if self.highlight_timer <= 0:
                self.highlight = False
    
    def draw(self, frame):
        """
        Draw the bubble on the frame.
        
        Args:
            frame: OpenCV frame to draw on
        """
        if not self.active:
            return
            
        # Draw outer circle (glow effect when highlighted)
        if self.highlight:
            # Draw a larger, semi-transparent circle for glow
            overlay = frame.copy()
            cv2.circle(overlay, (int(self.x), int(self.y)), 
                      int(self.radius * 1.5), (255, 255, 200, 0.5), -1)
            alpha = 0.5
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Draw the bubble
        color = config.COLOR_BUBBLE
        cv2.circle(frame, (int(self.x), int(self.y)), 
                  int(self.radius), color, -1)
        
        # Draw highlight
        if self.highlight:
            highlight_color = (255, 255, 255)
        else:
            highlight_color = (200, 200, 200)
            
        # Draw a small highlight circle
        highlight_radius = int(self.radius * 0.3)
        highlight_x = int(self.x - self.radius * 0.4)
        highlight_y = int(self.y - self.radius * 0.4)
        cv2.circle(frame, (highlight_x, highlight_y), 
                  highlight_radius, highlight_color, -1)
        
        # Draw bubble outline
        cv2.circle(frame, (int(self.x), int(self.y)), 
                  int(self.radius), (255, 255, 255), 1)
    
    def set_highlight(self, duration: Optional[float] = None):
        """
        Set the bubble to be highlighted for a duration.
        
        Args:
            duration: Duration in seconds (uses default if None)
        """
        self.highlight = True
        self.highlight_timer = duration or self.highlight_duration
    
    def reset(self, x: Optional[float] = None, y: Optional[float] = None, 
              radius: Optional[float] = None, speed: Optional[float] = None):
        """
        Reset the bubble's properties for reuse.
        
        Args:
            x: New x position (random if None)
            y: New y position (random if None)
            radius: New radius (random if None)
            speed: New speed (random if None)
        """
        if x is None:
            # Keep bubbles within 10-90% of screen width for better pop detection
            margin = config.WINDOW_WIDTH * 0.1
            x = np.random.uniform(margin, config.WINDOW_WIDTH - margin)
            
        if y is None:
            y = -50  # Start above the screen
            
        if radius is None:
            radius = np.random.uniform(*config.BUBBLE_RADIUS_RANGE)
            
        if speed is None:
            speed = np.random.uniform(*config.BUBBLE_SPEED_RANGE)
            
        super().reset(x, y, radius, speed)
        self.highlight = False
        self.highlight_timer = 0
