from __future__ import annotations
from typing import TYPE_CHECKING

from core.game_engine import GameEngine
from events.base_event import IObserver, GameEvent
from config.game_config import PowerType, GameConfig

if TYPE_CHECKING:
    from objects.object_manager import ObjectManager


class DestroyObserver(IObserver):
    """Handles the destroy power-up by removing all bubbles from the screen."""

    def __init__(self, game_engine: GameEngine):
        self.object_manager = game_engine.object_manager
        self.game_engine = game_engine

    def handle(self, event: GameEvent) -> None:
        if event.data.get('power_type') == PowerType.DESTROY:
            to_be_destroyed_bubbles = len(self.object_manager.get_objects(GameConfig.BUBBLE))
            self.game_engine.score += (to_be_destroyed_bubbles * GameConfig.SCORE_PER_POP)
            self.object_manager.remove_all()

