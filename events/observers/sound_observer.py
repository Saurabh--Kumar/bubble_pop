import os
import pygame
from typing import Dict

from events.base_event import GameEvent, EventType, IObserver


class SoundObserver(IObserver):
    """Handles sound effects for game events."""

    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self._initialized = False
        self._init_sound_system()

    def _init_sound_system(self) -> None:
        """Initializes the sound system and loads all required sounds."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self._load_sounds()
            self._initialized = True
        except Exception as e:
            print(f"Failed to initialize sound system: {e}")

    def _load_sounds(self) -> None:
        """Loads all sound files."""
        sound_files = {
            "pop": os.path.join("assets", "sounds", "pop.wav"),
            "powerup": os.path.join("assets", "sounds", "powerup.wav"),
            "game_over": os.path.join("assets", "sounds", "game_over.wav"),
        }
        for name, path in sound_files.items():
            self._load_sound(name, path)

    def _load_sound(self, name: str, path: str) -> None:
        """Loads a single sound file."""
        if not os.path.exists(path):
            print(f"Sound file not found: {path}")
            return
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Failed to load sound {path}: {e}")

    def play_sound(self, name: str, volume: float = 1.0) -> None:
        """Plays a sound by its name."""
        if not self._initialized or name not in self.sounds:
            return
        try:
            sound = self.sounds[name]
            sound.set_volume(volume)
            sound.play()
        except pygame.error as e:
            print(f"Error playing sound {name}: {e}")

    def handle(self, event: GameEvent) -> None:
        """Handles a game event and plays the corresponding sound."""
        if not self._initialized:
            return

        sound_map = {
            EventType.BUBBLE_HIT: "pop",
            EventType.POWER_ACTIVATED: "powerup",
            EventType.GAME_OVER: "game_over",
        }

        if event.event_type in sound_map:
            self.play_sound(sound_map[event.event_type])

    def cleanup(self) -> None:
        """Cleans up resources used by the sound system."""
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        self._initialized = False
