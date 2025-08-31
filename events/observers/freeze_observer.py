from __future__ import annotations
import time
from typing import TYPE_CHECKING

from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config, PowerType

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class FreezeObserver(IObserver):
    """Handles the freeze power-up by updating the game engine's freeze state."""

    def __init__(self, game_engine: GameEngine):
        self.game_engine = game_engine

    def handle(self, event: GameEvent) -> None:
        if event.event_type == EventType.POWER_ACTIVATED and event.data.get("power_type") == PowerType.FREEZE:
            self.activate_freeze()

    def activate_freeze(self) -> None:
        """Activates the freeze effect in the game engine."""
        freeze_duration = config.POWER_DURATION
        self.game_engine.freeze_until = time.time() + freeze_duration
        self.game_engine.is_frozen = True
        self.game_engine.object_manager.freeze_all(True)
        self.game_engine.event_manager.post(GameEvent(EventType.FREEZE_START, {"duration": freeze_duration}))
