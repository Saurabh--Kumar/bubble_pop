import time
from typing import Dict, Any, Optional

from core.game_engine import GameEngine
from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config, PowerType


class FreezeObserver(IObserver):
    """Handles the freeze power-up functionality."""
    
    def __init__(self, game_engine: GameEngine):
        """
        Initialize the freeze observer.
        
        Args:
            game_engine: Reference to the game engine
        """
        self.game_engine = game_engine
        self._freeze_timer: Optional[threading.Timer] = None
    
    def handle(self, event: GameEvent):
        """
        Handle a game event and activate freeze if needed.
        
        Args:
            event: The game event to handle
        """
        if (event.event_type == EventType.POWER_ACTIVATED and 
            event.data.get("power_type") == "F"):
            self.activate_freeze()
    
    def activate_freeze(self, duration: Optional[float] = None):
        """
        Activate the freeze effect.
        
        Args:
            duration: Duration of the freeze in seconds (uses config if None)
        """
        # Cancel any existing freeze timer
        if self._freeze_timer and self._freeze_timer.is_alive():
            self._freeze_timer.cancel()
        
        # Set the freeze end time
        freeze_duration = duration or config.POWER_DURATION
        self.game_engine.freeze_until = time.time() + freeze_duration
        
        # Freeze all objects
        self.game_engine.object_manager.freeze_all(True)
        
        # Post freeze start event
        self.game_engine.event_manager.post(GameEvent(
            EventType.FREEZE_START,
            {"duration": freeze_duration}
        ))
        
        # Set a timer to end the freeze
        self._freeze_timer = threading.Timer(
            freeze_duration,
            self._end_freeze
        )
        self._freeze_timer.daemon = True
        self._freeze_timer.start()
    
    def _end_freeze(self):
        """End the freeze effect."""
        # Unfreeze all objects
        self.game_engine.object_manager.freeze_all(False)
        
        # Post freeze end event
        self.game_engine.event_manager.post(GameEvent(
            EventType.FREEZE_END,
            {}
        ))
    
    def cleanup(self):
        """Clean up resources."""
        if self._freeze_timer and self._freeze_timer.is_alive():
            self._freeze_timer.cancel()
