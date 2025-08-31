from __future__ import annotations
from typing import TYPE_CHECKING
from events.base_event import IObserver, GameEvent
from config.game_config import PowerType, config

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class PowerHealthObserver(IObserver):
    """Handles the health power-up by restoring the player's health."""

    def __init__(self, game_engine: GameEngine):
        self.game_engine = game_engine

    def handle(self, event: GameEvent) -> None:
        if event.data.get('power_type') == PowerType.HEALTH:
            self.game_engine.health = config.INITIAL_HEALTH
