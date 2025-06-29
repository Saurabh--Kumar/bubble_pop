import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from objects.bubble import Bubble
from objects.power import Power, PowerType

class TestPowerObject(unittest.TestCase):
    def setUp(self):
        self.x = 400
        self.y = 100
        self.power_type = PowerType.FREEZE
        self.power = Power(x=self.x, y=self.y, power_type=self.power_type)
        
        # Create a test image
        self.test_img = np.zeros((600, 800, 3), dtype=np.uint8)
    
    def test_initial_properties(self):
        """Test that power-up is initialized with correct properties."""
        self.assertEqual(self.power.x, self.x)
        self.assertEqual(self.power.y, self.y)
        self.assertEqual(self.power.radius, Power.POWER_RADIUS)
        self.assertEqual(self.power.speed, Power.POWER_SPEED)
        self.assertEqual(self.power.power_type, self.power_type)
        self.assertTrue(self.power.active)
    
    def test_update(self):
        """Test that power-up updates position and animation."""
        initial_y = self.power.y
        initial_angle = self.power.angle
        initial_pulse = self.power.pulse_timer
        
        dt = 0.1
        self.power.update(dt)
        
        # Should move down
        self.assertGreater(self.power.y, initial_y)
        self.assertAlmostEqual(self.power.y, initial_y + self.power.speed * dt, places=5)
        
        # Animation should update
        self.assertNotEqual(self.power.angle, initial_angle)
        self.assertNotEqual(self.power.pulse_timer, initial_pulse)
    
    def test_draw(self):
        """Test that drawing doesn't raise exceptions."""
        try:
            self.power.draw(self.test_img)
        except Exception as e:
            self.fail(f"Drawing power-up raised an exception: {e}")
    
    def test_reset(self):
        """Test that reset updates power-up properties."""
        new_x = 200
        new_y = 50
        new_type = PowerType.DESTROY
        
        self.power.reset(x=new_x, y=new_y)
        
        self.assertEqual(self.power.x, new_x)
        self.assertEqual(self.power.y, new_y)
        self.assertEqual(self.power.power_type, self.power_type)  # Type shouldn't change on reset
        self.assertTrue(self.power.active)
    
    def test_power_type_enum(self):
        """Test that power type is a valid enum value."""
        self.assertIn(self.power.power_type, list(PowerType))
    
    def test_power_colors(self):
        """Test that all power types have a color defined."""
        for power_type in PowerType:
            power = Power(self.x, self.y, power_type)
            self.assertIn(power.power_type, Power.POWER_COLORS)

class TestBubbleObject(unittest.TestCase):
    def test_bubble_creation(self):
        """Test that Bubble can be created with required parameters."""
        bubble = Bubble(x=100, y=200, radius=30, speed=100)
        self.assertIsInstance(bubble, Bubble)
        self.assertEqual(bubble.x, 100)
        self.assertEqual(bubble.y, 200)
        self.assertEqual(bubble.radius, 30)
        self.assertEqual(bubble.speed, 100)
        self.assertTrue(bubble.active)

if __name__ == '__main__':
    unittest.main()
