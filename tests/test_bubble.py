import unittest
import cv2
import numpy as np
from unittest.mock import patch

from objects.bubble import Bubble
from config.game_config import config

class TestBubble(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.width = 800
        self.height = 600
        self.radius = 30
        self.speed = 100
        self.x = 400
        self.y = 100
        self.bubble = Bubble(x=self.x, y=self.y, radius=self.radius, speed=self.speed)
        
        # Create a blank test image
        self.test_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    def test_initial_properties(self):
        """Test that bubble is initialized with correct properties."""
        self.assertEqual(self.bubble.x, self.x)
        self.assertEqual(self.bubble.y, self.y)
        self.assertEqual(self.bubble.radius, self.radius)
        self.assertEqual(self.bubble.speed, self.speed)
        self.assertTrue(self.bubble.active)
    
    def test_update(self):
        """Test that bubble moves down when updated."""
        initial_y = self.bubble.y
        self.bubble.update(1.0)  # 1 second has passed
        self.assertGreater(self.bubble.y, initial_y)  # Should move down
        self.assertAlmostEqual(self.bubble.y, initial_y + self.speed * 1.0, places=5)
    
    def test_draw(self):
        """Test that drawing doesn't raise exceptions."""
        try:
            self.bubble.draw(self.test_img)
        except Exception as e:
            self.fail(f"Drawing bubble raised an exception: {e}")
    
    def test_reset(self):
        """Test that reset updates bubble properties."""
        new_x = 200
        new_y = 50
        new_radius = 20
        new_speed = 150
        
        self.bubble.reset(x=new_x, y=new_y, radius=new_radius, speed=new_speed)
        
        self.assertEqual(self.bubble.x, new_x)
        self.assertEqual(self.bubble.y, new_y)
        self.assertEqual(self.bubble.radius, new_radius)
        self.assertEqual(self.bubble.speed, new_speed)
        self.assertTrue(self.bubble.active)
    
    def test_is_hit(self):
        """Test hit detection."""
        # Position inside bubble
        self.assertTrue(self.bubble.is_hit((self.x, self.y)))
        # Position at edge
        self.assertTrue(self.bubble.is_hit((self.x + self.radius, self.y)))
        # Position outside bubble
        self.assertFalse(self.bubble.is_hit((self.x + self.radius + 1, self.y)))
    
    def test_is_off_screen(self):
        """Test off-screen detection."""
        self.bubble.y = 800  # Off-screen
        self.assertTrue(self.bubble.is_off_screen(600))
        self.bubble.y = 300  # On-screen
        self.assertFalse(self.bubble.is_off_screen(600))

if __name__ == '__main__':
    unittest.main()
