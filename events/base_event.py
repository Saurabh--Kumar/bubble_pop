from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

class EventType(Enum):
    """Types of game events."""
    BUBBLE_HIT = auto()
    BUBBLE_MISSED = auto()
    POWER_ACTIVATED = auto()
    GAME_OVER = auto()
    GAME_START = auto()
    SCORE_UPDATE = auto()
    HEALTH_UPDATE = auto()
    FREEZE_START = auto()
    FREEZE_END = auto()


@dataclass
class GameEvent:
    """Base class for all game events."""
    event_type: EventType
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize with empty dict if no data provided."""
        if self.data is None:
            self.data = {}


class IObserver:
    """Observer interface for handling game events."""
    
    def handle(self, event: GameEvent):
        """
        Handle a game event.
        
        Args:
            event: The game event to handle
        """
        raise NotImplementedError("Subclasses must implement handle()")


class IObservable:
    """Interface for objects that can be observed."""
    
    def __init__(self):
        """Initialize with empty observers dict."""
        self._observers = {}
    
    def register_observer(self, event_type: EventType, observer: IObserver):
        """
        Register an observer for a specific event type.
        
        Args:
            event_type: Type of event to observe
            observer: Observer to register
        """
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)
    
    def unregister_observer(self, event_type: EventType, observer: IObserver):
        """
        Unregister an observer for a specific event type.
        
        Args:
            event_type: Type of event
            observer: Observer to unregister
        """
        if event_type in self._observers:
            if observer in self._observers[event_type]:
                self._observers[event_type].remove(observer)
    
    def notify_observers(self, event: GameEvent):
        """
        Notify all observers of an event.
        
        Args:
            event: Event to notify observers about
        """
        if event.event_type in self._observers:
            for observer in self._observers[event.event_type]:
                observer.handle(event)
