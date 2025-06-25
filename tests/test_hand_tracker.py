import unittest
import cv2
import numpy as np
from pathlib import Path

from input.hand_tracker import HandTracker
from config.game_config import config

class TestHandTracker(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.width = 640
        self.height = 480
        self.hand_tracker = HandTracker()
        
        # Create a blank test image
        self.test_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    def test_process_frame_no_hands(self):
        """Test processing a frame with no hands."""
        # Create a blank image (no hands)
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        fists = self.hand_tracker.detect_fists(frame)
        self.assertEqual(len(fists), 0)
    
    def test_draw_fists(self):
        """Test that drawing fists doesn't raise exceptions."""
        try:
            # Test with empty fists list
            self.hand_tracker.draw_fists(self.test_img, [])
            
            # Test with some dummy fist positions
            dummy_fists = [(100, 100), (200, 200)]
            self.hand_tracker.draw_fists(self.test_img, dummy_fists)
        except Exception as e:
            self.fail(f"Drawing fists raised an exception: {e}")
    
    def test_cleanup(self):
        """Test that cleanup doesn't raise exceptions."""
        try:
            self.hand_tracker.cleanup()
        except Exception as e:
            self.fail(f"Cleanup raised an exception: {e}")
        
        # Test that we can still use the tracker after cleanup
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        fists = self.hand_tracker.detect_fists(frame)
        self.assertIsInstance(fists, list)

if __name__ == '__main__':
    unittest.main()
