import queue
import threading
import time
from typing import Dict, List, Optional

from events.base_event import GameEvent, EventType, IObserver, IObservable


class EventManager(IObservable):
    """Manages game events and notifies observers."""
    
    def __init__(self):
        """Initialize the event manager."""
        super().__init__()
        self._event_queue = queue.Queue()
        self._running = False
        self._dispatch_thread: Optional[threading.Thread] = None
        self._observers: Dict[EventType, List[IObserver]] = {}
    
    def post(self, event: GameEvent):
        """
        Post an event to the queue.
        
        Args:
            event: Event to post
        """
        self._event_queue.put(event)
    
    def start_dispatch_loop(self):
        """Start the event dispatch loop in a separate thread."""
        if self._running:
            return
            
        self._running = True
        self._dispatch_thread = threading.Thread(target=self._dispatch_loop, daemon=True)
        self._dispatch_thread.start()
    
    def stop_dispatch_loop(self):
        """Stop the event dispatch loop."""
        self._running = False
        
        # Put a None event to unblock the queue if it's empty
        self._event_queue.put(None)
        
        if self._dispatch_thread and self._dispatch_thread.is_alive():
            self._dispatch_thread.join(timeout=1.0)
    
    def _dispatch_loop(self):
        """Process events from the queue and notify observers."""
        while self._running:
            try:
                # Get event with timeout to allow checking self._running
                try:
                    event = self._event_queue.get(timeout=0.1)
                    if event is None:  # Sentinel value to stop
                        break
                except queue.Empty:
                    continue
                
                # Notify observers
                if event.event_type in self._observers:
                    for observer in self._observers[event.event_type]:
                        try:
                            observer.handle(event)
                        except Exception as e:
                            print(f"Error in event handler: {e}")
                
                # Mark task as done
                self._event_queue.task_done()
                
            except Exception as e:
                print(f"Error in event dispatch loop: {e}")
                time.sleep(0.1)  # Prevent tight loop on error
    
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
