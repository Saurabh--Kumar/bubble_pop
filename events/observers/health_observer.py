from __future__ import annotations
from typing import TYPE_CHECKING

from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class HealthObserver(IObserver):
    """Handles health-related events, such as losing health when a bubble is missed."""

    def __init__(self, game_engine: GameEngine):
        self.game_engine = game_engine

    def handle(self, event: GameEvent) -> None:
        if event.event_type == EventType.BUBBLE_MISSED:
            self.game_engine.health -= config.HEALTH_DECREASE_ON_MISS
            self.game_engine.health = max(0, self.game_engine.health)

            if self.game_engine.health <= 0:
                self.game_engine.event_manager.post(GameEvent(EventType.GAME_OVER))
