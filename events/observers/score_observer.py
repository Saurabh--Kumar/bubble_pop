from __future__ import annotations
from typing import TYPE_CHECKING

from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config

if TYPE_CHECKING:
    from core.game_engine import GameEngine


class ScoreObserver(IObserver):
    """Handles score-related events by updating the game score."""

    def __init__(self, game_engine: GameEngine):
        self.game_engine = game_engine

    def handle(self, event: GameEvent) -> None:
        if event.event_type == EventType.BUBBLE_HIT:
            self.game_engine.score += config.SCORE_PER_POP
