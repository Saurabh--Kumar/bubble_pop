from typing import Dict, Any, Optional

from core.game_engine import GameEngine
from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config


class ScoreObserver(IObserver):
    """Handles score-related events."""
    
    def __init__(self, game_engine: Optional[GameEngine] = None):
        """
        Initialize the score observer.
        
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
            
        if event.event_type == EventType.BUBBLE_HIT:
            # Increase score when a bubble is hit
            self.game_engine.score += config.SCORE_PER_POP
            
            # Notify score update
            self.game_engine.event_manager.post(GameEvent(
                EventType.SCORE_UPDATE,
                {"score": self.game_engine.score}
            ))
