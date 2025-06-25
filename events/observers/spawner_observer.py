from typing import Dict, Any, List, Optional
import random

from core.game_engine import GameEngine
from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config, PowerType
from objects.object_manager import ObjectManager


class SpawnerObserver(IObserver):
    """Handles spawning of new game objects."""
    
    def __init__(self, object_manager: ObjectManager):
        """
        Initialize the spawner observer.
        
        Args:
            object_manager: Reference to the object manager
        """
        self.object_manager = object_manager
        self.spawn_counter = 0
    
    def handle(self, event: GameEvent):
        """
        Handle a game event and spawn new objects if needed.
        
        Args:
            event: The game event to handle
        """
        if event.event_type == EventType.BUBBLE_HIT:
            # Spawn a new bubble when one is popped
            self.spawn_counter += 1
            
            # Every 5 pops, spawn a power-up instead of a bubble
            if self.spawn_counter >= 5:
                self.spawn_counter = 0
                self.object_manager.spawn_power()
            else:
                # Spawn a new bubble
                self.object_manager.spawn_bubble()
        
        elif event.event_type == EventType.POWER_ACTIVATED and event.data.get("power_type") == "D":
            # Destroy all bubbles when 'D' power-up is collected
            self.object_manager.remove_all("bubble")
