from typing import Dict, Any, Optional

from core.game_engine import GameEngine, GameState
from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config


class HealthObserver(IObserver):
    """Handles health-related events."""
    
    def __init__(self, game_engine: Optional[GameEngine] = None):
        """
        Initialize the health observer.
        
        Args:
            game_engine: Reference to the game engine (optional)
        """
        self.game_engine = game_engine
    
    def set_game_engine(self, game_engine: GameEngine):
        """
        Set the game engine reference.
        
        Args:
            game_engine: Reference to the game engine
        """
        self.game_engine = game_engine
    
    def handle(self, event: GameEvent):
        """
        Handle a game event.
        
        Args:
            event: The game event to handle
        """
        if not self.game_engine:
            return
            
        if event.event_type == EventType.BUBBLE_MISSED:
            # Decrease health when a bubble is missed
            self.game_engine.health -= config.HEALTH_DECREASE_ON_MISS
            
            # Clamp health between 0 and 100
            self.game_engine.health = max(0, min(100, self.game_engine.health))
            
            # Notify health update
            self.game_engine.event_manager.post(GameEvent(
                EventType.HEALTH_UPDATE,
                {"health": self.game_engine.health}
            ))
            
            # Check for game over
            if self.game_engine.health <= 0:
                self.game_engine.event_manager.post(GameEvent(
                    EventType.GAME_OVER,
                    {"reason": "Health depleted"}
                ))
        
        elif event.event_type == EventType.POWER_ACTIVATED and event.data.get("power_type") == "H":
            # Heal when health power-up is collected
            self.game_engine.health = 100.0
            
            # Notify health update
            self.game_engine.event_manager.post(GameEvent(
                EventType.HEALTH_UPDATE,
                {"health": self.game_engine.health}
            ))
