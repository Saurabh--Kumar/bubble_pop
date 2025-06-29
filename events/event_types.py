from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional, Tuple

class EventType(Enum):
    """Enumeration of all possible event types in the game."""
    BUBBLE_HIT = auto()
    BUBBLE_MISSED = auto()
    POWER_HIT = auto()
    GAME_START = auto()
    GAME_OVER = auto()
    RESTART_GAME = auto()
    FREEZE_START = auto()
    FREEZE_END = auto()
    SCORE_UPDATE = auto()
    HEALTH_UPDATE = auto()

@dataclass
class GameEvent(ABC):
    """Base class for all game events."""
    event_type: EventType
    timestamp: float = 0.0
    
    def __post_init__(self):
        import time
        self.timestamp = time.time()

@dataclass
class BubbleHitEvent(GameEvent):
    """Event triggered when a bubble is hit by the player."""
    x: float = 0.0
    y: float = 0.0
    points: int = 1
    
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.BUBBLE_HIT

@dataclass
class BubbleMissedEvent(GameEvent):
    """Event triggered when a bubble is missed (goes off screen)."""
    x: float = 0.0
    y: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.BUBBLE_MISSED

@dataclass
class PowerHitEvent(GameEvent):
    """Event triggered when a power-up is collected."""
    power_type: str  # 'F' for freeze, 'D' for destroy, 'H' for health
    x: float = 0.0
    y: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.POWER_HIT

@dataclass
class GameStartEvent(GameEvent):
    """Event triggered when the game starts."""
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.GAME_START

@dataclass
class GameOverEvent(GameEvent):
    """Event triggered when the game is over."""
    final_score: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.GAME_OVER

@dataclass
class RestartGameEvent(GameEvent):
    """Event triggered when the game is restarted."""
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.RESTART_GAME

@dataclass
class FreezeEvent(GameEvent):
    """Event triggered when freeze power is activated or deactivated."""
    active: bool
    duration: float = 5.0  # seconds
    
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.FREEZE_START if self.active else EventType.FREEZE_END

@dataclass
class ScoreUpdateEvent(GameEvent):
    """Event triggered when score is updated."""
    score: int = 0
    delta: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.SCORE_UPDATE

@dataclass
class HealthUpdateEvent(GameEvent):
    """Event triggered when health is updated."""
    health: float = 0.0
    delta: float = 0.0
    
    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.HEALTH_UPDATE
