import unittest
import cv2
import numpy as np
from pathlib import Path

from objects.bubble import Bubble
from config.game_config import config

class TestBubble(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.width = 800
        self.height = 600
        self.bubble = Bubble(self.width, self.height)
        
        # Create a blank test image
        self.test_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    def test_initial_position(self):
        """Test that bubble is initialized within screen bounds."""
        self.assertGreaterEqual(self.bubble.x, 0)
        self.assertLessEqual(self.bubble.x, self.width)
        self.assertEqual(self.bubble.y, self.height)  # Should start at bottom
    
    def test_update(self):
        """Test that bubble moves up when updated."""
        initial_y = self.bubble.y
        self.bubble.update(1.0)  # 1 second has passed
        self.assertLess(self.bubble.y, initial_y)  # Should move up
    
    def test_draw(self):
        """Test that drawing doesn't raise exceptions."""
        try:
            self.bubble.draw(self.test_img)
        except Exception as e:
            self.fail(f"Drawing bubble raised an exception: {e}")
    
    def test_reset(self):
        """Test that reset puts bubble back to bottom with new x position."""
        initial_x = self.bubble.x
        self.bubble.update(1.0)  # Move up
        self.bubble.reset()
        self.assertEqual(self.bubble.y, self.height)  # Back to bottom
        self.assertNotEqual(self.bubble.x, initial_x)  # New x position

if __name__ == '__main__':
    unittest.main()
