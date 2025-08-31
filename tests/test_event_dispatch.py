import unittest
from unittest.mock import Mock
import queue

from events.event_manager import EventManager
from events.base_event import EventType, GameEvent


class TestEventDispatch(unittest.TestCase):

    def setUp(self):
        self.event_manager = EventManager()
        self.mock_observer = Mock()

    def test_register_and_post_event(self):
        """Test that an event is correctly posted to the queue."""
        self.event_manager.register_observer(EventType.BUBBLE_HIT, self.mock_observer)
        event = GameEvent(EventType.BUBBLE_HIT, {"x": 100, "y": 100})

        self.event_manager.post(event)

        try:
            posted_event = self.event_manager._event_queue.get_nowait()
            self.assertEqual(posted_event, event)
        except queue.Empty:
            self.fail("Event was not posted to the queue")

    def test_dispatch_loop_notifies_observers(self):
        """Test that the dispatch loop notifies registered observers."""
        self.event_manager.register_observer(EventType.BUBBLE_HIT, self.mock_observer)
        event = GameEvent(EventType.BUBBLE_HIT, {"x": 100, "y": 100})
        self.event_manager.post(event)

        # Start and stop the loop to process the event
        self.event_manager.start_dispatch_loop()
        self.event_manager.stop_dispatch_loop()

        self.mock_observer.handle.assert_called_once_with(event)


if __name__ == '__main__':
    unittest.main()
