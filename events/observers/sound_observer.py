import os
import random
import pygame
from typing import Dict, Any, Optional

from core.game_engine import GameEngine
from events.base_event import GameEvent, EventType, IObserver
from config.game_config import config

class SoundObserver(IObserver):
    """Handles sound effects for game events."""
    
    def __init__(self):
        """Initialize the sound observer."""
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self._initialized = False
        self._init_sound_system()
    
    def _init_sound_system(self):
        """Initialize the sound system and load sounds."""
        try:
            # Initialize pygame mixer if not already done
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Load sounds
            self._load_sound("pop", os.path.join("assets", "sounds", "pop.wav"))
            self._load_sound("powerup", os.path.join("assets", "sounds", "powerup.wav"))
            self._load_sound("game_over", os.path.join("assets", "sounds", "game_over.wav"))
            
            self._initialized = True
        except Exception as e:
            print(f"Failed to initialize sound system: {e}")
    
    def _load_sound(self, name: str, path: str):
        """
        Load a sound file.
        
        Args:
            name: Name to store the sound under
            path: Path to the sound file
        """
        try:
            # Check if file exists
            if not os.path.exists(path):
                print(f"Sound file not found: {path}")
                return
                
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
        except Exception as e:
            print(f"Failed to load sound {path}: {e}")
    
    def play_sound(self, name: str, volume: float = 1.0):
        """
        Play a sound by name.
        
        Args:
            name: Name of the sound to play
            volume: Volume level (0.0 to 1.0)
        """
        if not self._initialized or name not in self.sounds:
            return
            
        try:
            sound = self.sounds[name]
            sound.set_volume(volume)
            sound.play()
        except Exception as e:
            print(f"Error playing sound {name}: {e}")
    
    def handle(self, event: GameEvent):
        """
        Handle a game event and play appropriate sounds.
        
        Args:
            event: The game event to handle
        """
        if not self._initialized:
            return
            
        try:
            if event.event_type == EventType.BUBBLE_HIT:
                self.play_sound("pop")
                
            elif event.event_type == EventType.POWER_ACTIVATED:
                self.play_sound("powerup")
                
            elif event.event_type == EventType.GAME_OVER:
                self.play_sound("game_over")
                
        except Exception as e:
            print(f"Error in sound observer: {e}")
    
    def cleanup(self):
        """Clean up resources."""
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        self._initialized = False
