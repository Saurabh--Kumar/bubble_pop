import queue
import threading
from typing import Dict, List, Optional, Type

from events.base_event import GameEvent, EventType, IObserver


class EventManager:
    """Manages game events and notifies observers in a separate thread."""

    def __init__(self):
        self._event_queue: queue.Queue[Optional[GameEvent]] = queue.Queue()
        self._observers: Dict[EventType, List[IObserver]] = {}
        self._running = False
        self._dispatch_thread: Optional[threading.Thread] = None

    def register_observer(self, event_type: EventType, observer: IObserver) -> None:
        """Register an observer for a specific event type."""
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def post(self, event: GameEvent) -> None:
        """Post an event to the queue for asynchronous processing."""
        self._event_queue.put(event)

    def start_dispatch_loop(self) -> None:
        """Start the event dispatch loop in a separate thread."""
        if self._running:
            return
        self._running = True
        self._dispatch_thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self._dispatch_thread.start()

    def stop_dispatch_loop(self) -> None:
        """Stop the event dispatch loop."""
        self._running = False
        self._event_queue.put(None)  # Sentinel to unblock the queue
        if self._dispatch_thread:
            self._dispatch_thread.join()

    def _dispatch_loop(self) -> None:
        """Continuously process events from the queue and notify observers."""
        while self._running:
            try:
                event = self._event_queue.get(timeout=0.1)
                if event is None:  # Sentinel value check
                    break

                if event.event_type in self._observers:
                    for observer in self._observers[event.event_type]:
                        observer.handle(event)

                self._event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in event dispatch loop: {e}")

    def wait_for_events(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for all events to be processed.
        
        Args:
            timeout: Maximum time to wait in seconds (None for no timeout)
            
        Returns:
            bool: True if all events were processed, False if timed out
        """
        try:
            self._event_queue.join(timeout=timeout)
            return True
        except Exception as e:
            print(f"Error waiting for events: {e}")
            return False
    
    def clear_events(self):
        """Clear all pending events."""
        while not self._event_queue.empty():
            try:
                self._event_queue.get_nowait()
                self._event_queue.task_done()
            except queue.Empty:
                break
