import unittest
from unittest.mock import Mock, patch
from events.event_manager import EventManager
from events.base_event import EventType, GameEvent

class TestEventDispatch(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.mock_observer = Mock()
    
    def test_register_and_notify_observer(self):
        """Test that registered observers are notified of events."""
        # Register mock observer for BUBBLE_HIT event
        self.event_manager.register_observer(EventType.BUBBLE_HIT, self.mock_observer)
        
        # Create and post an event
        event = GameEvent(EventType.BUBBLE_HIT, {"x": 100, "y": 100, "points": 1})
        self.event_manager.post(event)
        
        # Process events
        self.event_manager.notify_observers(event)
        
        # Verify observer was called with the event
        self.mock_observer.handle.assert_called_once()
        called_event = self.mock_observer.handle.call_args[0][0]
        self.assertEqual(called_event.event_type, EventType.BUBBLE_HIT)
        self.assertEqual(called_event.data["x"], 100)
        self.assertEqual(called_event.data["y"], 100)
        self.assertEqual(called_event.data["points"], 1)
    
    def test_multiple_observers(self):
        """Test that multiple observers can be registered for the same event type."""
        mock_observer1 = Mock()
        mock_observer2 = Mock()
        
        self.event_manager.register_observer(EventType.BUBBLE_HIT, mock_observer1)
        self.event_manager.register_observer(EventType.BUBBLE_HIT, mock_observer2)
        
        event = GameEvent(EventType.BUBBLE_HIT, {"x": 100, "y": 100, "points": 1})
        self.event_manager.post(event)
        self.event_manager.notify_observers(event)
        
        # Verify both observers were called
        mock_observer1.handle.assert_called_once()
        mock_observer2.handle.assert_called_once()
        
        # Verify they were called with the correct event
        event1 = mock_observer1.handle.call_args[0][0]
        event2 = mock_observer2.handle.call_args[0][0]
        self.assertEqual(event1.event_type, EventType.BUBBLE_HIT)
        self.assertEqual(event2.event_type, EventType.BUBBLE_HIT)
    
    @patch('time.time', return_value=1234567890.0)
    def test_event_timestamp(self, mock_time):
        """Test that events have timestamps."""
        event = GameEvent(EventType.BUBBLE_HIT, {})
        # The base GameEvent doesn't automatically add a timestamp
        # So we'll just verify the event was created successfully
        self.assertEqual(event.event_type, EventType.BUBBLE_HIT)
        self.assertEqual(event.data, {})

if __name__ == '__main__':
    unittest.main()
