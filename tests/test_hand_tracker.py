import unittest
import cv2
import numpy as np
from unittest.mock import patch, MagicMock

from input.hand_tracker import HandTracker

class TestHandTracker(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.width = 800
        self.height = 600
        self.hand_tracker = HandTracker()
        
        # Create a blank test image
        self.test_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    def test_initialization(self):
        """Test that the hand tracker initializes correctly."""
        self.assertIsNotNone(self.hand_tracker.hands)
        self.assertEqual(len(self.hand_tracker.fist_positions), 0)
        self.assertEqual(len(self.hand_tracker.position_history), 0)
    
    @patch('input.hand_tracker.mp.solutions.hands.Hands')
    def test_process_frame_no_hands(self, mock_hands):
        """Test processing a frame with no hands."""
        # Mock the hands.process method to return no hands
        mock_results = MagicMock()
        mock_results.multi_hand_landmarks = None
        mock_hands.return_value.process.return_value = mock_results
        
        # Process a blank frame
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.hand_tracker.process_frame(frame)
        
        # No fists should be detected
        self.assertEqual(len(self.hand_tracker.fist_positions), 0)
    
    @patch('input.hand_tracker.mp.solutions.hands.Hands')
    def test_process_frame_with_hands(self, mock_hands):
        """Test processing a frame with hands."""
        # Create a mock hand landmark
        mock_landmark = MagicMock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        
        # Mock the hand landmarks
        mock_hand_landmarks = MagicMock()
        mock_hand_landmarks.landmark = [mock_landmark] * 21  # 21 landmarks per hand
        
        # Mock the results
        mock_results = MagicMock()
        mock_results.multi_hand_landmarks = [mock_hand_landmarks]
        mock_hands.return_value.process.return_value = mock_results
        
        # Mock the _is_fist method to return True
        with patch.object(self.hand_tracker, '_is_fist', return_value=(True, 0.9)):
            # Process a blank frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            self.hand_tracker.process_frame(frame)
            
            # Should detect one fist
            self.assertEqual(len(self.hand_tracker.fist_positions), 1)
            
            # Position should be in the center of the frame
            x, y = self.hand_tracker.fist_positions[0]
            self.assertAlmostEqual(x, self.width // 2, delta=1)
            self.assertAlmostEqual(y, self.height // 2, delta=1)
    
    def test_is_fist_detection(self):
        """Test the fist detection logic."""
        # Create mock landmarks for an open hand
        open_hand = [MagicMock(x=0.5, y=0.5) for _ in range(21)]
        
        # Test with open hand (not a fist)
        is_fist, confidence = self.hand_tracker._is_fist(open_hand)
        self.assertFalse(is_fist)
        
        # Create mock landmarks for a closed fist
        # In a real test, we would set up specific landmark positions
        # that match a closed fist configuration
        closed_hand = [MagicMock(x=0.5, y=0.5) for _ in range(21)]
        # Set up specific landmark positions that would indicate a fist
        # This is a simplified version - in reality, you'd need to set up
        # the exact landmark positions for a closed fist
        
        # Mock the distance calculation to return a small value (fist)
        with patch('numpy.linalg.norm', return_value=0.1):
            is_fist, confidence = self.hand_tracker._is_fist(closed_hand)
            self.assertTrue(is_fist)
    
    def test_cleanup(self):
        """Test that cleanup doesn't raise exceptions."""
        try:
            self.hand_tracker.cleanup()
        except Exception as e:
            self.fail(f"Cleanup raised an exception: {e}")
        
        # The hands object should be closed
        self.hand_tracker.hands.close = MagicMock()
        self.hand_tracker.cleanup()
        self.hand_tracker.hands.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
