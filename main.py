import cv2
import sys
import time
import pygame
import numpy as np
from typing import Tuple, Optional

# Initialize pygame for sound
pygame.mixer.init()

from core.game_engine import GameEngine
from config.game_config import config, GameState
from input.hand_tracker import HandTracker


def main():
    """Main entry point for the Bubble Pop game."""
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.WINDOW_HEIGHT)
    
    # Create window
    cv2.namedWindow('Bubble Pop', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Bubble Pop', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Create game engine
    game_engine = GameEngine()
    
    # Game loop
    last_time = time.time()
    running = True
    
    try:
        while running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Read frame from camera
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame through game engine
            modified_frame = game_engine.process_frame(frame)
            
            # Display the frame
            cv2.imshow('Bubble Pop', modified_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if not game_engine.handle_key(key):
                running = False
                
            # Check for game over
            if game_engine.state == GameState.GAME_OVER:
                # Show game over screen for 3 seconds
                cv2.waitKey(3000)
                
                # Ask for restart
                modified_frame = cv2.putText(
                    modified_frame,
                    "Press 'R' to restart or 'Q' to quit", 
                    (config.WINDOW_WIDTH // 2 - 200, config.WINDOW_HEIGHT // 2 + 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, 
                    (255, 255, 255), 
                    2, 
                    cv2.LINE_AA
                )
                cv2.imshow('Bubble Pop', modified_frame)
                
                # Wait for restart or quit
                while True:
                    key = cv2.waitKey(100) & 0xFF
                    if key == ord('r') or key == ord('R'):
                        game_engine.reset()
                        last_time = time.time()
                        break
                    elif key == ord('q') or key == 27:  # 'q' or ESC
                        running = False
                        break
    
    except KeyboardInterrupt:
        print("Game stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        game_engine.cleanup()
        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()


if __name__ == "__main__":
    main()
