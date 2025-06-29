import unittest
from unittest.mock import Mock, patch, MagicMock, call
import numpy as np

from core.game_engine import GameEngine
from config.game_config import GameState
from events.event_manager import EventManager, GameEvent, EventType

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        # Patch the dependencies
        self.hand_tracker_patch = patch('core.game_engine.HandTracker')
        self.object_manager_patch = patch('core.game_engine.ObjectManager')
        self.renderer_patch = patch('core.game_engine.Renderer')
        self.event_manager_patch = patch('core.game_engine.EventManager')
        
        # Start patches
        self.mock_hand_tracker_cls = self.hand_tracker_patch.start()
        self.mock_object_manager_cls = self.object_manager_patch.start()
        self.mock_renderer_cls = self.renderer_patch.start()
        self.mock_event_manager_cls = self.event_manager_patch.start()
        
        # Create mock instances
        self.mock_hand_tracker = MagicMock()
        self.mock_object_manager = MagicMock()
        self.mock_renderer = MagicMock()
        self.mock_event_manager = MagicMock()
        
        # Configure the class mocks to return our mock instances
        self.mock_hand_tracker_cls.return_value = self.mock_hand_tracker
        self.mock_object_manager_cls.return_value = self.mock_object_manager
        self.mock_renderer_cls.return_value = self.mock_renderer
        self.mock_event_manager_cls.return_value = self.mock_event_manager
        
        # Import after patching
        from core.game_engine import GameEngine
        self.GameEngine = GameEngine
    
    def tearDown(self):
        # Stop all patches
        self.hand_tracker_patch.stop()
        self.object_manager_patch.stop()
        self.renderer_patch.stop()
        self.event_manager_patch.stop()
    
    def test_engine_initialization(self):
        """Test that the game engine initializes correctly."""
        # Create the engine
        engine = self.GameEngine()
        
        # Verify initialization
        self.assertEqual(engine.state, GameState.INIT)
        self.assertEqual(engine.score, 0)
        self.assertEqual(engine.health, 100)  # Default health from config
        
        # Verify components were created
        self.mock_hand_tracker_cls.assert_called_once()
        self.mock_object_manager_cls.assert_called_once()
        self.mock_renderer_cls.assert_called_once()
        self.mock_event_manager_cls.assert_called_once()
        
        # Verify event manager started
        self.mock_event_manager.start_dispatch_loop.assert_called_once()
    
    def test_register_observers(self):
        """Test that observers are registered during initialization."""
        # Import the observers to patch them
        with patch('events.observers.score_observer.ScoreObserver', create=True) as mock_score_observer_cls, \
             patch('events.observers.health_observer.HealthObserver', create=True) as mock_health_observer_cls, \
             patch('events.observers.sound_observer.SoundObserver', create=True) as mock_sound_observer_cls, \
             patch('events.observers.spawner_observer.SpawnerObserver', create=True) as mock_spawner_observer_cls, \
             patch('events.observers.freeze_observer.FreezeObserver', create=True) as mock_freeze_observer_cls:
            
            # Create the engine which will register observers
            engine = self.GameEngine()
            
            # Verify observers were created and registered
            mock_score_observer_cls.assert_called_once_with(engine)
            mock_health_observer_cls.assert_called_once_with(engine)
            mock_sound_observer_cls.assert_called_once()
            mock_spawner_observer_cls.assert_called_once_with(engine.object_manager)
            mock_freeze_observer_cls.assert_called_once_with(engine)
            
            # Verify event manager registration
            expected_calls = [
                call(EventType.BUBBLE_HIT, mock_score_observer_cls.return_value),
                call(EventType.BUBBLE_HIT, mock_sound_observer_cls.return_value),
                call(EventType.BUBBLE_MISSED, mock_health_observer_cls.return_value),
                call(EventType.BUBBLE_HIT, mock_spawner_observer_cls.return_value),
                call(EventType.POWER_ACTIVATED, mock_freeze_observer_cls.return_value)
            ]
            self.mock_event_manager.register_observer.assert_has_calls(expected_calls, any_order=True)
    
    def test_update_not_running(self):
        """Test that update doesn't process game logic when not in RUNNING state."""
        engine = self.GameEngine()
        engine.state = GameState.INIT
        
        # Mock time to control the frozen state
        with patch('time.time', return_value=1000):
            engine.update(1.0/60.0)  # 60 FPS
        
        # Verify no game logic was processed
        self.mock_object_manager.update_all.assert_not_called()
    
    def test_update_running(self):
        """Test that update processes game logic when in RUNNING state."""
        engine = self.GameEngine()
        engine.state = GameState.RUNNING
        
        # Mock time to control the frozen state
        with patch('time.time', return_value=1000):
            engine.update(1.0/60.0)  # 60 FPS
        
        # Verify game logic was processed
        self.mock_object_manager.update_all.assert_called_once_with(1.0/60.0)
    
    def test_game_over_condition(self):
        """Test that game transitions to GAME_OVER when health reaches zero."""
        engine = self.GameEngine()
        engine.state = GameState.RUNNING
        engine.health = 0
        
        # Run an update
        engine.update(1.0/60.0)
        
        # Should transition to GAME_OVER
        self.assertEqual(engine.state, GameState.GAME_OVER)

if __name__ == '__main__':
    unittest.main()
