from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple


class GameState(Enum):
    INIT = auto()
    RUNNING = auto()
    GAME_OVER = auto()


class PowerType(Enum):
    FREEZE = 'F'  # Freeze all bubbles
    DESTROY = 'D'  # Destroy all bubbles
    HEAL = 'H'     # Restore health


@dataclass
class GameConfig:
    # Window settings
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    FPS: int = 60
    
    # Game settings
    INITIAL_COUNTDOWN: int = 10  # seconds
    SCORE_PER_POP: int = 1
    HEALTH_DECREASE_ON_MISS: float = 10.0  # percentage
    INITIAL_HEALTH: float = 100.0
    
    # Bubble settings
    BUBBLE_RADIUS_RANGE: Tuple[int, int] = (30, 50)
    BUBBLE_SPEED_RANGE: Tuple[float, float] = (2.0, 5.0)
    BUBBLE_SPAWN_RATE: float = 0.03  # probability per frame
    
    # Power-up settings
    POWER_SPAWN_RATE: float = 0.005  # probability per frame
    POWER_DURATION: float = 5.0  # seconds
    
    # Hand tracking
    HAND_DETECTION_CONFIDENCE: float = 0.7
    FIST_RADIUS: int = 20
    
    # Collision
    COLLISION_FRAME_INTERVAL: int = 5  # check collision every N frames
    
    # Colors (BGR format)
    COLOR_BG: Tuple[int, int, int] = (0, 0, 0)  # Black
    COLOR_BUBBLE: Tuple[int, int, int] = (255, 255, 0)  # Yellow
    COLOR_POWER_FREEZE: Tuple[int, int, int] = (255, 0, 0)  # Blue
    COLOR_POWER_DESTROY: Tuple[int, int, int] = (0, 0, 255)  # Red
    COLOR_POWER_HEAL: Tuple[int, int, int] = (0, 255, 0)  # Green
    COLOR_FIST: Tuple[int, int, int] = (0, 255, 255)  # Cyan
    COLOR_TEXT: Tuple[int, int, int] = (255, 255, 255)  # White
    
    # Font
    FONT_FACE: int = 0  # cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE: float = 1.0
    FONT_THICKNESS: int = 2


# Singleton instance
config = GameConfig()
