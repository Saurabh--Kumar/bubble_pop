import unittest
import numpy as np
from objects.bubble import Bubble
from objects.power import Power
from config.game_config import config

class TestCollision(unittest.TestCase):
    def setUp(self):
        self.width = 800
        self.height = 600
        self.bubble = Bubble(self.width, self.height)
        self.power = Power(self.width, self.height, 'F')  # Freeze power
        
        # Position objects at known locations
        self.bubble.x = 100
        self.bubble.y = 100
        self.bubble.radius = 30
        
        self.power.x = 200
        self.power.y = 200
        self.power.radius = 20
    
    def test_bubble_hit_detection(self):
        """Test that hit detection works when fist is inside bubble."""
        # Fist position inside bubble
        fist_pos = (105, 105)
        self.assertTrue(self.bubble.is_hit(fist_pos))
    
    def test_bubble_miss_detection(self):
        """Test that hit detection fails when fist is outside bubble."""
        # Fist position outside bubble
        fist_pos = (200, 200)
        self.assertFalse(self.bubble.is_hit(fist_pos))
    
    def test_power_hit_detection(self):
        """Test that power-up hit detection works."""
        # Fist position inside power-up
        fist_pos = (205, 205)
        self.assertTrue(self.power.is_hit(fist_pos))
    
    def test_edge_case_hit(self):
        """Test hit detection at the edge of the bubble."""
        # Fist position exactly at bubble's edge (x + radius)
        edge_pos = (self.bubble.x + self.bubble.radius, self.bubble.y)
        self.assertTrue(self.bubble.is_hit(edge_pos))

if __name__ == '__main__':
    unittest.main()
