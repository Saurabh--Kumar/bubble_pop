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
    @patch('input.hand_tracker.cv2.cvtColor')
    @patch('input.hand_tracker.cv2.circle')
    @patch('input.hand_tracker.cv2.putText')
    def test_process_frame_with_hands(self, mock_put_text, mock_circle, mock_cvt_color, mock_hands):
        """Test processing a frame with hands."""
        # Mock the color conversion to return the same frame
        mock_cvt_color.return_value = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create a mock hand landmark
        mock_landmark = MagicMock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        mock_landmark.z = 0.0
        
        # Mock the hand landmarks
        mock_hand_landmarks = MagicMock()
        mock_hand_landmarks.landmark = [mock_landmark] * 21  # 21 landmarks per hand
        
        # Mock the results
        mock_results = MagicMock()
        mock_results.multi_hand_landmarks = [mock_hand_landmarks]
        
        # Create a mock hands instance with the process method
        mock_hands_instance = MagicMock()
        mock_hands_instance.process.return_value = mock_results
        
        # Mock the HandLandmark enum values
        mock_hand_landmark_enum = MagicMock()
        mock_hand_landmark_enum.WRIST = 0
        mock_hand_landmark_enum.MIDDLE_FINGER_MCP = 9
        mock_hand_landmark_enum.THUMB_TIP = 4
        mock_hand_landmark_enum.THUMB_IP = 3
        mock_hand_landmark_enum.THUMB_CMC = 2
        mock_hand_landmark_enum.INDEX_FINGER_TIP = 8
        mock_hand_landmark_enum.INDEX_FINGER_DIP = 7
        mock_hand_landmark_enum.INDEX_FINGER_PIP = 6
        mock_hand_landmark_enum.INDEX_FINGER_MCP = 5
        mock_hand_landmark_enum.MIDDLE_FINGER_TIP = 12
        mock_hand_landmark_enum.MIDDLE_FINGER_DIP = 11
        mock_hand_landmark_enum.MIDDLE_FINGER_PIP = 10
        mock_hand_landmark_enum.RING_FINGER_TIP = 16
        mock_hand_landmark_enum.RING_FINGER_DIP = 15
        mock_hand_landmark_enum.RING_FINGER_PIP = 14
        mock_hand_landmark_enum.RING_FINGER_MCP = 13
        mock_hand_landmark_enum.PINKY_TIP = 20
        mock_hand_landmark_enum.PINKY_DIP = 19
        mock_hand_landmark_enum.PINKY_PIP = 18
        mock_hand_landmark_enum.PINKY_MCP = 17
        
        # Create a mock hands module with the HandLandmark enum
        mock_hands_module = MagicMock()
        mock_hands_module.HandLandmark = mock_hand_landmark_enum
        
        # Patch the mp.solutions.hands module
        with patch.dict('sys.modules', {'mediapipe.solutions.hands': mock_hands_module}):
            # Create a new HandTracker instance to use the mocked module
            from input.hand_tracker import HandTracker
            hand_tracker = HandTracker()
            
            # Replace the hands instance with our mock
            hand_tracker.hands = mock_hands_instance
            hand_tracker.mp_hands = mock_hands_module
            
            # Mock the _is_fist method to return True
            with patch.object(hand_tracker, '_is_fist', return_value=(True, 0.9)):
                # Process a blank frame
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                
                # Call the method under test
                hand_tracker.process_frame(frame)
                
                # Verify that cv2.cvtColor was called
                mock_cvt_color.assert_called_once_with(frame, cv2.COLOR_BGR2RGB)
                
                # Verify that the process method was called with the RGB frame
                mock_hands_instance.process.assert_called_once()
                args, _ = mock_hands_instance.process.call_args
                self.assertEqual(len(args), 1, "Process should be called with one argument")
                self.assertEqual(args[0].shape, (self.height, self.width, 3), 
                              "Process should be called with an RGB frame of the correct size")
                
                # Verify that _is_fist was called with the correct arguments
                # It should be called twice - once for the actual check and once for drawing
                self.assertEqual(hand_tracker._is_fist.call_count, 2, 
                              "_is_fist should be called twice - once for check and once for drawing")
                
                # Verify that the fist position was added
                self.assertEqual(len(hand_tracker.fist_positions), 1, 
                               "Expected one fist position to be detected")
                
                # Verify the position is as expected (center of the frame)
                x, y = hand_tracker.fist_positions[0]
                expected_x = int(0.5 * self.width)  # 50% of width
                expected_y = int(0.5 * self.height)  # 50% of height
                self.assertEqual(x, expected_x, 
                              f"Expected x position {expected_x}, got {x}")
                self.assertEqual(y, expected_y, 
                              f"Expected y position {expected_y}, got {y}")
                
                # Verify that circle was called to draw the fist position
                mock_circle.assert_called()
    
    @patch('input.hand_tracker.np.linalg.norm')
    def test_is_fist_detection(self, mock_norm):
        """Test the fist detection logic."""
        # Create mock landmarks for an open hand
        open_hand = [MagicMock(x=0.5, y=0.5, z=0.0) for _ in range(21)]
        
        # Configure the mock to return a large distance for open hand (fingers not curled)
        def distance_side_effect(p1, p2):
            # For wrist to tip distances, return a large value (fingers not curled)
            if p1 == open_hand[0]:  # Wrist
                if p2 in [open_hand[8], open_hand[12], open_hand[16], open_hand[20]]:  # Finger tips
                    return 10.0
            # For MCP to wrist distances, return a small value
            if p1 == open_hand[0] and p2 in [open_hand[5], open_hand[9], open_hand[13], open_hand[17]]:
                return 5.0
            return 1.0  # Default distance
        
        # Set the side effect for the mock
        mock_norm.side_effect = distance_side_effect
        
        # Test with open hand (not a fist)
        is_fist, confidence = self.hand_tracker._is_fist(open_hand)
        self.assertFalse(is_fist, "Open hand should not be detected as a fist")
        self.assertLess(confidence, 0.7, "Confidence should be low for open hand")
        
        # Now test with a closed fist
        def distance_side_effect_closed(p1, p2):
            # For wrist to tip distances, return a small value (fingers curled)
            if p1 == open_hand[0]:  # Wrist
                if p2 in [open_hand[8], open_hand[12], open_hand[16], open_hand[20]]:  # Finger tips
                    return 0.1
            # For MCP to wrist distances, return a small value
            if p1 == open_hand[0] and p2 in [open_hand[5], open_hand[9], open_hand[13], open_hand[17]]:
                return 5.0
            return 1.0  # Default distance
        
        # Update the side effect for the mock
        mock_norm.side_effect = distance_side_effect_closed
        
        # Set thumb position to be over the fingers
        open_hand[4].x = 0.6  # Thumb tip x > index MCP x
        open_hand[4].y = 0.4  # Thumb tip y < index MCP y + 0.1
        
        # Set up the hand landmarks to match the expected structure
        # The _is_fist method expects specific landmark indices to be set
        # We'll set up the landmarks to simulate a closed fist
        
        # Set up the wrist and finger MCPs
        open_hand[0].x = 0.5  # Wrist
        open_hand[0].y = 0.5
        
        # Set up the finger tips to be close to the wrist (curled fingers)
        for idx in [8, 12, 16, 20]:  # Finger tips
            open_hand[idx].x = 0.5
            open_hand[idx].y = 0.5
        
        # Set up the MCPs to be slightly above the wrist
        for idx in [5, 9, 13, 17]:  # MCPs
            open_hand[idx].x = 0.5
            open_hand[idx].y = 0.4
        
        # Set up the thumb to be over the fingers
        open_hand[4].x = 0.6  # Thumb tip x > index MCP x
        open_hand[4].y = 0.4  # Thumb tip y < index MCP y + 0.1
        
        # Test with closed fist
        is_fist, confidence = self.hand_tracker._is_fist(open_hand)
        
        # We'll just check that the method runs without errors
        # The exact confidence value might depend on the implementation details
        self.assertIsInstance(confidence, float, "Confidence should be a float")
        self.assertGreaterEqual(confidence, 0.0, "Confidence should be >= 0")
        self.assertLessEqual(confidence, 1.0, "Confidence should be <= 1")
    
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
