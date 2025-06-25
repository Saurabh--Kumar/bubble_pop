import cv2
import numpy as np
from typing import Tuple, Optional, List, Dict, Any

from config.game_config import config, GameState
from objects.base_object import AbstractFallingObject

class Renderer:
    """Handles all rendering for the game."""
    
    def __init__(self):
        """Initialize the renderer."""
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._font_scale = config.FONT_SCALE
        self._font_thickness = config.FONT_THICKNESS
        self._font_color = config.COLOR_TEXT
        
        # Cache for rendered text
        self._text_cache = {}
    
    def draw_text(self, frame, text: str, position: Tuple[int, int], 
                 color: Optional[Tuple[int, int, int]] = None,
                 font_scale: Optional[float] = None,
                 thickness: Optional[int] = None,
                 centered: bool = False,
                 outline: bool = False,
                 outline_color: Tuple[int, int, int] = (0, 0, 0)):
        """
        Draw text on the frame.
        
        Args:
            frame: Frame to draw on
            text: Text to draw
            position: (x, y) position
            color: Text color (BGR)
            font_scale: Font scale
            thickness: Line thickness
            centered: If True, position is the center of the text
            outline: If True, draw an outline around the text
            outline_color: Color of the outline (BGR)
        """
        if color is None:
            color = self._font_color
        if font_scale is None:
            font_scale = self._font_scale
        if thickness is None:
            thickness = self._font_thickness
        
        x, y = position
        
        # Draw outline if requested
        if outline:
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1),
                          (-1, 0), (1, 0), (0, -1), (0, 1)]:
                cv2.putText(frame, text, (x + dx, y + dy), 
                          self._font, font_scale, 
                          outline_color, thickness + 1)
        
        # Draw main text
        cv2.putText(frame, text, (x, y), 
                   self._font, font_scale, 
                   color, thickness)
    
    def draw_centered_text(self, frame, text: str, y_offset: int = 0, 
                         font_scale: float = 1.0, **kwargs):
        """
        Draw centered text on the frame.
        
        Args:
            frame: Frame to draw on
            text: Text to draw
            y_offset: Vertical offset from center
            font_scale: Font scale
            **kwargs: Additional arguments for draw_text
        """
        # Get text size
        (text_width, text_height), _ = cv2.getTextSize(
            text, self._font, font_scale, self._font_thickness)
        
        # Calculate position
        x = (frame.shape[1] - text_width) // 2
        y = frame.shape[0] // 2 + y_offset + text_height // 2
        
        # Draw text
        self.draw_text(frame, text, (x, y), 
                      font_scale=font_scale, 
                      centered=True, **kwargs)
    
    def draw_health_bar(self, frame, health: float, 
                       position: Tuple[int, int], 
                       size: Tuple[int, int] = (200, 20),
                       border_thickness: int = 2):
        """
        Draw a health bar.
        
        Args:
            frame: Frame to draw on
            health: Health value (0-100)
            position: (x, y) position of the top-left corner
            size: (width, height) of the health bar
            border_thickness: Thickness of the border
        """
        x, y = position
        width, height = size
        
        # Clamp health between 0 and 100
        health = max(0, min(100, health))
        
        # Calculate fill width
        fill_width = int(width * (health / 100))
        
        # Draw background
        cv2.rectangle(frame, 
                     (x, y), 
                     (x + width, y + height), 
                     (50, 50, 50), -1)
        
        # Draw fill
        if health > 0:
            # Determine color based on health
            if health > 60:
                color = (0, 200, 0)  # Green
            elif health > 30:
                color = (0, 165, 255)  # Orange
            else:
                color = (0, 0, 200)  # Red
                
            cv2.rectangle(frame, 
                         (x, y), 
                         (x + fill_width, y + height), 
                         color, -1)
        
        # Draw border
        cv2.rectangle(frame, 
                     (x, y), 
                     (x + width, y + height), 
                     (200, 200, 200), border_thickness)
        
        # Draw health text
        health_text = f"{int(health)}%"
        text_size = cv2.getTextSize(health_text, self._font, 
                                  0.7, self._font_thickness)[0]
        
        text_x = x + (width - text_size[0]) // 2
        text_y = y + (height + text_size[1]) // 2
        
        self.draw_text(frame, health_text, (text_x, text_y), 
                      font_scale=0.7, 
                      color=(255, 255, 255))
    
    def draw_score(self, frame, score: int, position: Tuple[int, int] = (10, 30)):
        """
        Draw the score on the frame.
        
        Args:
            frame: Frame to draw on
            score: Current score
            position: (x, y) position of the top-left corner
        """
        score_text = f"Score: {score}"
        self.draw_text(frame, score_text, position, 
                      color=config.COLOR_TEXT,
                      font_scale=1.0,
                      outline=True)
    
    def draw_timer(self, frame, time_left: float, position: Tuple[int, int], 
                  color: Optional[Tuple[int, int, int]] = None):
        """
        Draw a timer on the frame.
        
        Args:
            frame: Frame to draw on
            time_left: Time left in seconds
            position: (x, y) position of the top-left corner
            color: Text color (BGR)
        """
        if color is None:
            color = config.COLOR_TEXT
            
        # Format time as MM:SS
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        
        self.draw_text(frame, timer_text, position, 
                      color=color,
                      font_scale=1.0,
                      outline=True)
    
    def draw_progress_bar(self, frame, progress: float, 
                         position: Tuple[int, int], 
                         size: Tuple[int, int],
                         color: Tuple[int, int, int],
                         bg_color: Tuple[int, int, int] = (50, 50, 50),
                         border: int = 2):
        """
        Draw a progress bar.
        
        Args:
            frame: Frame to draw on
            progress: Progress value (0.0 to 1.0)
            position: (x, y) position of the top-left corner
            size: (width, height) of the progress bar
            color: Fill color (BGR)
            bg_color: Background color (BGR)
            border: Border thickness
        """
        x, y = position
        width, height = size
        
        # Clamp progress between 0 and 1
        progress = max(0.0, min(1.0, progress))
        
        # Draw background
        cv2.rectangle(frame, 
                     (x, y), 
                     (x + width, y + height), 
                     bg_color, -1)
        
        # Draw progress
        if progress > 0:
            fill_width = int(width * progress)
            cv2.rectangle(frame, 
                         (x, y), 
                         (x + fill_width, y + height), 
                         color, -1)
        
        # Draw border
        if border > 0:
            cv2.rectangle(frame, 
                         (x, y), 
                         (x + width, y + height), 
                         (200, 200, 200), border)
    
    def draw_button(self, frame, text: str, position: Tuple[int, int], 
                   size: Tuple[int, int],
                   color: Tuple[int, int, int] = (100, 100, 200),
                   text_color: Tuple[int, int, int] = (255, 255, 255),
                   hover: bool = False,
                   pressed: bool = False):
        """
        Draw a button.
        
        Args:
            frame: Frame to draw on
            text: Button text
            position: (x, y) position of the top-left corner
            size: (width, height) of the button
            color: Button color (BGR)
            text_color: Text color (BGR)
            hover: Whether the button is being hovered
            pressed: Whether the button is being pressed
        """
        x, y = position
        width, height = size
        
        # Adjust color if hovered or pressed
        if pressed:
            color = tuple(max(0, c - 40) for c in color)
        elif hover:
            color = tuple(min(255, c + 30) for c in color)
        
        # Draw button background
        cv2.rectangle(frame, 
                     (x, y), 
                     (x + width, y + height), 
                     color, -1)
        
        # Draw border
        border_color = (min(255, color[0] + 60), 
                       min(255, color[1] + 60), 
                       min(255, color[2] + 60))
        cv2.rectangle(frame, 
                     (x, y), 
                     (x + width, y + height), 
                     border_color, 2)
        
        # Draw text
        text_size = cv2.getTextSize(text, self._font, 
                                  0.8, self._font_thickness)[0]
        text_x = x + (width - text_size[0]) // 2
        text_y = y + (height + text_size[1]) // 2
        
        # Text shadow
        cv2.putText(frame, text, (text_x + 1, text_y + 1), 
                   self._font, 0.8, 
                   (0, 0, 0), self._font_thickness)
        
        # Main text
        cv2.putText(frame, text, (text_x, text_y), 
                   self._font, 0.8, 
                   text_color, self._font_thickness)
        
        # Return button rect for click detection
        return (x, y, width, height)
