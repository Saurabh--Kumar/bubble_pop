import unittest
import time
from unittest.mock import Mock, patch

from events.base_event import GameEvent, EventType
from events.observers.destroy_observer import DestroyObserver
from events.observers.freeze_observer import FreezeObserver
from events.observers.power_health_observer import PowerHealthObserver
from config.game_config import config, PowerType


class TestPowerupObservers(unittest.TestCase):

    def setUp(self):
        """Set up mock objects for each test."""
        self.mock_game_engine = Mock()
        self.mock_object_manager = Mock()

        # Mock event manager on the game engine
        self.mock_game_engine.event_manager = Mock()

        # Assign the object manager to the game engine mock
        self.mock_game_engine.object_manager = self.mock_object_manager

    def test_destroy_observer(self):
        """Verify that the DestroyObserver calls remove_all and updates score."""
        # Arrange
        from config.game_config import GameConfig
        # Mock get_objects to return a list with 3 bubbles
        mock_bubbles = [Mock(), Mock(), Mock()]
        self.mock_object_manager.get_objects.return_value = mock_bubbles
        self.mock_game_engine.score = 0
        
        destroy_observer = DestroyObserver(self.mock_game_engine)
        destroy_event = GameEvent(EventType.POWER_ACTIVATED, {"power_type": PowerType.DESTROY})

        # Act
        destroy_observer.handle(destroy_event)

        # Assert
        self.mock_object_manager.get_objects.assert_called_once_with(GameConfig.BUBBLE)
        self.mock_object_manager.remove_all.assert_called_once()
        # Verify score is updated correctly (3 bubbles * SCORE_PER_POP)
        self.assertEqual(self.mock_game_engine.score, 3 * GameConfig.SCORE_PER_POP)

    def test_power_health_observer(self):
        """Verify that the PowerHealthObserver restores health to the initial value."""
        # Arrange
        self.mock_game_engine.health = 50  # Assume current health is low
        health_observer = PowerHealthObserver(self.mock_game_engine)
        health_event = GameEvent(EventType.POWER_ACTIVATED, {"power_type": PowerType.HEALTH})

        # Act
        health_observer.handle(health_event)

        # Assert
        self.assertEqual(self.mock_game_engine.health, config.INITIAL_HEALTH)

    @patch('time.time')
    def test_freeze_observer_activates_freeze(self, mock_time):
        """Verify that the FreezeObserver correctly activates the freeze state."""
        # Arrange
        current_time = 1000.0
        mock_time.return_value = current_time
        freeze_observer = FreezeObserver(self.mock_game_engine)
        freeze_event = GameEvent(EventType.POWER_ACTIVATED, {"power_type": PowerType.FREEZE})

        # Act
        freeze_observer.handle(freeze_event)

        # Assert
        expected_freeze_until = current_time + config.POWER_DURATION
        self.assertEqual(self.mock_game_engine.freeze_until, expected_freeze_until)
        self.assertTrue(self.mock_game_engine.is_frozen)
        self.mock_object_manager.freeze_all.assert_called_once_with(True)

        # Verify that the FREEZE_START event was posted
        self.mock_game_engine.event_manager.post.assert_called_once()
        posted_event = self.mock_game_engine.event_manager.post.call_args[0][0]
        self.assertEqual(posted_event.event_type, EventType.FREEZE_START)
        self.assertEqual(posted_event.data['duration'], config.POWER_DURATION)


if __name__ == '__main__':
    unittest.main()
