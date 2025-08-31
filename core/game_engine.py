import cv2
import time
import numpy as np

from config.game_config import config, GameState
from input.hand_tracker import HandTracker
from objects.object_manager import ObjectManager
from rendering.renderer import Renderer
from events.event_manager import EventManager, GameEvent, EventType


class GameEngine:
    def __init__(self):
        self.state = GameState.INIT
        self.score = 0
        self.health = config.INITIAL_HEALTH
        self.frame_count = 0
        self.last_collision_check = 0
        self.start_time = time.time()
        self.freeze_until = 0
        self.is_frozen = False
        
        # Initialize components
        self.hand_tracker = HandTracker()
        self.object_manager = ObjectManager()
        self.renderer = Renderer()
        self.event_manager = EventManager()
        
        # Register event observers
        self._register_observers()
        
        # Start event processing thread
        self.event_manager.start_dispatch_loop()
    
    def _register_observers(self):
        from events.observers.score_observer import ScoreObserver
        from events.observers.health_observer import HealthObserver
        from events.observers.sound_observer import SoundObserver
        from events.observers.freeze_observer import FreezeObserver
        from events.observers.destroy_observer import DestroyObserver
        from events.observers.power_health_observer import PowerHealthObserver
        
        self.event_manager.register_observer(EventType.BUBBLE_HIT, ScoreObserver(self))
        self.event_manager.register_observer(EventType.BUBBLE_HIT, SoundObserver())
        self.event_manager.register_observer(EventType.BUBBLE_MISSED, HealthObserver(self))
        self.event_manager.register_observer(EventType.POWER_ACTIVATED, FreezeObserver(self))
        self.event_manager.register_observer(EventType.POWER_ACTIVATED, DestroyObserver(self))
        self.event_manager.register_observer(EventType.POWER_ACTIVATED, PowerHealthObserver(self))
    
    def update(self, dt: float):
        """Update game state"""
        if self.state != GameState.RUNNING:
            return
            
        # Check and update freeze state
        self._update_freeze_state()

        # Update objects
        if not self.is_frozen:
            self.object_manager.update_all(dt)
        
        # Spawn new objects
        self._maybe_spawn_objects()
        
        # Check for missed objects (reached bottom of screen)
        self._check_missed_objects()
        
        # Check for collisions
        self._check_collisions()
        
        # Check game over condition
        if self.health <= 0:
            self.state = GameState.GAME_OVER
    
    def _update_freeze_state(self):
        """Checks if the freeze duration has expired and unfreezes objects."""
        if self.is_frozen and time.time() >= self.freeze_until:
            self.is_frozen = False
            self.object_manager.freeze_all(False)
            self.event_manager.post(GameEvent(EventType.FREEZE_END))
    
    def _maybe_spawn_objects(self):
        """Randomly spawn new bubbles and power-ups"""
        if np.random.uniform() < config.BUBBLE_SPAWN_RATE:
            self.object_manager.spawn_bubble()
            
        if np.random.uniform() < config.POWER_SPAWN_RATE:
            self.object_manager.spawn_power()
    
    def _check_missed_objects(self):
        """Check for objects that reached the bottom of the screen"""
        for obj in self.object_manager.get_objects():
            if obj.y - obj.radius > config.WINDOW_HEIGHT:
                if obj.type == "bubble":
                    self.event_manager.post(GameEvent(
                        EventType.BUBBLE_MISSED,
                        {"object": obj}
                    ))
                self.object_manager.remove_object(obj)
    
    def _check_collisions(self):
        self.frame_count += 1
        
        # Only check collisions every N frames for performance
        if (self.frame_count - self.last_collision_check) < config.COLLISION_FRAME_INTERVAL:
            return
            
        self.last_collision_check = self.frame_count
        
        # Get current fist positions
        fist_positions = self.hand_tracker.get_fist_positions()
        if not fist_positions or len(fist_positions) < 1:
            return
            
        # Check for hits
        for obj in self.object_manager.get_objects():
            for fist_pos in fist_positions:
                if obj.is_hit(fist_pos):
                    self._handle_hit(obj)
                    break  # Object can only be hit once
    
    def _handle_hit(self, obj):
        event_type = EventType.BUBBLE_HIT if obj.type == "bubble" else EventType.POWER_ACTIVATED
        payload = {"object": obj}
        if event_type == EventType.POWER_ACTIVATED:
            payload["power_type"] = obj.power_type

        self.event_manager.post(GameEvent(event_type, payload))
        self.object_manager.remove_object(obj)
    
    def draw(self, frame):
        """Draw the current game state on top of the camera frame"""
        # Make a copy of the frame to draw on
        frame_copy = frame.copy()
        
        # Draw all game objects
        self.object_manager.draw_all(frame_copy)
        
        # Draw fists (hand tracking)
        self.hand_tracker.draw_fists(frame_copy)
        
        # Create a semi-transparent overlay for UI elements
        overlay = frame_copy.copy()
        
        # Draw UI elements on the overlay
        self._draw_ui(overlay)
        
        # Draw game state specific elements
        if self.state == GameState.INIT:
            self._draw_countdown(overlay)
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over(overlay)
        
        # Blend the overlay with the frame
        alpha = 0.8  # Adjust this value to control transparency (0.0 to 1.0)
        cv2.addWeighted(overlay, alpha, frame_copy, 1 - alpha, 0, frame_copy)
        
        # Copy the result back to the original frame
        frame[:] = frame_copy
    
    def _draw_ui(self, frame):
        self._draw_score(frame)
        self._draw_health_bar(frame)
        self._draw_freeze_indicator(frame)
    
    def _draw_score(self, frame):
        score_text = f"Score: {self.score}"
        cv2.putText(frame, score_text, (10, 30), 
                   config.FONT_FACE, config.FONT_SCALE, 
                   config.COLOR_TEXT, config.FONT_THICKNESS)
        
    def _draw_health_bar(self, frame):
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = config.WINDOW_WIDTH - health_bar_width - 10
        health_bar_y = 10
        
        # Background
        cv2.rectangle(frame, 
                     (health_bar_x, health_bar_y), 
                     (health_bar_x + health_bar_width, health_bar_y + health_bar_height), 
                     (100, 100, 100), -1)
        
        # Current health
        health_width = int((self.health / 100.0) * health_bar_width)
        health_color = (0, 255, 0)  # Green when full
        if self.health < 30:
            health_color = (0, 0, 255)  # Red when low
        elif self.health < 60:
            health_color = (0, 165, 255)  # Orange when medium
            
        cv2.rectangle(frame, 
                     (health_bar_x, health_bar_y), 
                     (health_bar_x + health_width, health_bar_y + health_bar_height), 
                     health_color, -1)
        
        # Border
        cv2.rectangle(frame, 
                     (health_bar_x, health_bar_y), 
                     (health_bar_x + health_bar_width, health_bar_y + health_bar_height), 
                     (255, 255, 255), 1)
        
        # Health text
        health_text = f"{int(self.health)}%"
        text_size = cv2.getTextSize(health_text, config.FONT_FACE, 
                                  config.FONT_SCALE * 0.7, config.FONT_THICKNESS)[0]
        text_x = health_bar_x + (health_bar_width - text_size[0]) // 2
        text_y = health_bar_y + (health_bar_height + text_size[1]) // 2
        
        cv2.putText(frame, health_text, (text_x, text_y), 
                   config.FONT_FACE, config.FONT_SCALE * 0.7, 
                   (0, 0, 0), config.FONT_THICKNESS)
        
    def _draw_freeze_indicator(self, frame):
        if time.time() < self.freeze_until:
            freeze_text = f"FREEZE! {int(self.freeze_until - time.time())}s"
            text_size = cv2.getTextSize(freeze_text, config.FONT_FACE, 
                                      config.FONT_SCALE, config.FONT_THICKNESS)[0]
            text_x = (config.WINDOW_WIDTH - text_size[0]) // 2
            text_y = config.WINDOW_HEIGHT - 30
            
            cv2.putText(frame, freeze_text, (text_x, text_y), 
                       config.FONT_FACE, config.FONT_SCALE, 
                       (255, 255, 255), config.FONT_THICKNESS + 1)
    
    def _draw_countdown(self, frame):
        elapsed = time.time() - self.start_time
        if elapsed < config.INITIAL_COUNTDOWN:
            countdown = int(config.INITIAL_COUNTDOWN - elapsed) + 1
            text = str(countdown) if countdown > 0 else "GO!"
            text_size = cv2.getTextSize(text, config.FONT_FACE, 
                                      config.FONT_SCALE * 4, config.FONT_THICKNESS * 2)[0]
            
            text_x = (config.WINDOW_WIDTH - text_size[0]) // 2
            text_y = (config.WINDOW_HEIGHT + text_size[1]) // 2
            
            # Shadow
            cv2.putText(frame, text, (text_x + 3, text_y + 3), 
                       config.FONT_FACE, config.FONT_SCALE * 4, 
                       (100, 100, 100), config.FONT_THICKNESS * 2)
            
            # Main text
            cv2.putText(frame, text, (text_x, text_y), 
                       config.FONT_FACE, config.FONT_SCALE * 4, 
                       (255, 255, 255), config.FONT_THICKNESS * 2)
        else:
            self.state = GameState.RUNNING
    
    def _draw_game_over(self, frame):
        # Create a copy of the frame to work on
        overlay = frame.copy()
        
        # Draw semi-transparent black overlay
        cv2.rectangle(overlay, (0, 0), (config.WINDOW_WIDTH, config.WINDOW_HEIGHT), 
                     (0, 0, 0), -1)
        alpha = 0.8  # 80% opacity
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Game Over text with shadow for better visibility
        text = "GAME OVER"
        text_scale = config.FONT_SCALE * 3
        text_thickness = config.FONT_THICKNESS * 2
        text_size = cv2.getTextSize(text, config.FONT_FACE, text_scale, text_thickness)[0]
        text_x = (config.WINDOW_WIDTH - text_size[0]) // 2
        text_y = config.WINDOW_HEIGHT // 3
        
        # Draw shadow
        cv2.putText(frame, text, (text_x + 2, text_y + 2), 
                   config.FONT_FACE, text_scale, 
                   (0, 0, 0), text_thickness)
        # Draw main text
        cv2.putText(frame, text, (text_x, text_y), 
                   config.FONT_FACE, text_scale, 
                   (0, 0, 255), text_thickness)
        
        # Score with shadow
        score_text = f"Final Score: {self.score}"
        score_scale = config.FONT_SCALE * 1.5
        score_size = cv2.getTextSize(score_text, config.FONT_FACE, 
                                   score_scale, config.FONT_THICKNESS)[0]
        score_x = (config.WINDOW_WIDTH - score_size[0]) // 2
        score_y = text_y + 100
        
        # Draw shadow
        cv2.putText(frame, score_text, (score_x + 1, score_y + 1), 
                   config.FONT_FACE, score_scale, 
                   (0, 0, 0), config.FONT_THICKNESS + 1)
        # Draw main text
        cv2.putText(frame, score_text, (score_x, score_y), 
                   config.FONT_FACE, score_scale, 
                   (255, 255, 255), config.FONT_THICKNESS)
        
        # Make sure to return the modified frame
        return frame

    
    def process_frame(self, frame):
        """Process a single frame - update hand tracking and game state"""
        # Make a copy of the frame to prevent modifying the original
        frame_copy = frame.copy()
        
        # Update hand tracking
        self.hand_tracker.process_frame(frame_copy)
        
        # Update game state
        current_time = time.time()
        last_time = getattr(self, '_last_update_time', current_time)
        dt = current_time - last_time
        self._last_update_time = current_time
        
        # Only update game logic if we're in the right state
        if self.state != GameState.GAME_OVER:
            self.update(dt)
        
        # Draw the game on the frame copy
        self.draw(frame_copy)
        
        # Return the modified frame
        return frame_copy
    
    def handle_key(self, key: int):
        """Handle keyboard input"""
        if key == 27:  # ESC
            return False
        elif key == ord('r') and self.state == GameState.GAME_OVER:
            self.reset()
        return True
    
    def reset(self):
        """Reset the game to its initial state"""
        self.state = GameState.INIT
        self.score = 0
        self.health = config.INITIAL_HEALTH
        self.frame_count = 0
        self.last_collision_check = 0
        self.start_time = time.time()
        self.freeze_until = 0
        self.is_frozen = False
        
        # Reset components
        self.object_manager.reset()
    
    def cleanup(self):
        """Clean up resources"""
        self.event_manager.stop_dispatch_loop()
        self.hand_tracker.cleanup()
