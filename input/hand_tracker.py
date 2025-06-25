import cv2
import numpy as np
import mediapipe as mp
from typing import List, Tuple, Optional, Dict, Any

from config.game_config import config


class HandTracker:
    """Hand tracking using MediaPipe."""
    
    def __init__(self):
        """Initialize the hand tracker."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=config.HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=0.5
        )
        
        # Store the most recent fist positions (for each hand)
        self.fist_positions: List[Tuple[float, float]] = []
        
        # For smoothing positions
        self.position_history: Dict[int, List[Tuple[float, float]]] = {}
        self.max_history = 5
    
    def process_frame(self, frame):
        """
        Process a frame to detect hands and update fist positions.
        
        Args:
            frame: Input frame (BGR format)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        # Reset fist positions
        self.fist_positions = []
        
        # Draw hand landmarks for debugging
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw all landmarks (for debugging)
                for landmark in hand_landmarks.landmark:
                    height, width = frame.shape[:2]
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                
                # Get hand landmarks
                landmarks = hand_landmarks.landmark
                
                # Check if hand is a fist (thumb over fingers)
                is_fist, confidence = self._is_fist(landmarks)
                
                if is_fist:
                    # Get center of the fist (using wrist and middle finger MCP)
                    wrist = landmarks[self.mp_hands.HandLandmark.WRIST]
                    mcp = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    
                    # Calculate center between wrist and middle finger MCP
                    x = (wrist.x + mcp.x) / 2
                    y = (wrist.y + mcp.y) / 2
                    
                    # Convert to pixel coordinates
                    height, width = frame.shape[:2]
                    px = int(x * width)
                    py = int(y * height)
                    
                    # Add to positions
                    self.fist_positions.append((px, py))
                    
                    # Update position history for this hand
                    hand_id = id(hand_landmarks)
                    if hand_id not in self.position_history:
                        self.position_history[hand_id] = []
                    
                    self.position_history[hand_id].append((px, py))
                    
                    # Limit history size
                    if len(self.position_history[hand_id]) > self.max_history:
                        self.position_history[hand_id].pop(0)
                    
                    # Draw debug info
                    cv2.circle(frame, (px, py), 10, (0, 0, 255), -1)
                    cv2.putText(frame, f'Fist: {confidence:.2f}', (px + 15, py - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                else:
                    # Draw why it's not a fist (for debugging)
                    wrist = landmarks[self.mp_hands.HandLandmark.WRIST]
                    height, width = frame.shape[:2]
                    wx = int(wrist.x * width)
                    wy = int(wrist.y * height)
                    cv2.putText(frame, f'Not a fist: {confidence:.2f}', (wx, wy - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    def _is_fist(self, landmarks) -> tuple[bool, float]:
        """
        Check if the hand is making a fist.
        
        Args:
            landmarks: Hand landmarks from MediaPipe
            
        Returns:
            tuple: (is_fist, confidence) where confidence is a float between 0 and 1
        """
        # Get relevant landmarks
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = landmarks[self.mp_hands.HandLandmark.THUMB_IP]
        thumb_mcp = landmarks[self.mp_hands.HandLandmark.THUMB_CMC]
        
        index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_dip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_DIP]
        index_pip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        index_mcp = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        
        middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_dip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
        middle_pip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        middle_mcp = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        
        ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_dip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_DIP]
        ring_pip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_PIP]
        ring_mcp = landmarks[self.mp_hands.HandLandmark.RING_FINGER_MCP]
        
        pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_dip = landmarks[self.mp_hands.HandLandmark.PINKY_DIP]
        pinky_pip = landmarks[self.mp_hands.HandLandmark.PINKY_PIP]
        pinky_mcp = landmarks[self.mp_hands.HandLandmark.PINKY_MCP]
        
        wrist = landmarks[self.mp_hands.HandLandmark.WRIST]
        
        # Calculate distances between finger tips and their MCPs
        def distance(p1, p2):
            return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2) ** 0.5
        
        # Check if fingers are curled (tip is close to palm)
        index_curled = distance(index_tip, wrist) < distance(index_mcp, wrist) * 0.9
        middle_curled = distance(middle_tip, wrist) < distance(middle_mcp, wrist) * 0.9
        ring_curled = distance(ring_tip, wrist) < distance(ring_mcp, wrist) * 0.9
        pinky_curled = distance(pinky_tip, wrist) < distance(pinky_mcp, wrist) * 0.9
        
        # Check if thumb is over the fingers
        thumb_over = thumb_tip.x > index_mcp.x and thumb_tip.y < index_mcp.y + 0.1
        
        # Calculate confidence (0 to 1)
        confidence = 0.0
        if index_curled: confidence += 0.25
        if middle_curled: confidence += 0.25
        if ring_curled: confidence += 0.25
        if pinky_curled: confidence += 0.15
        if thumb_over: confidence += 0.1
        
        # Consider it a fist if confidence is above threshold
        is_fist = confidence > 0.7
        
        return is_fist, confidence
        
        # Check if thumb is over the fingers
        thumb_over = thumb_tip.x > index_tip.x and thumb_tip.x < pinky_tip.x
        
        return fingers_closed and thumb_over
    
    def get_fist_positions(self) -> List[Tuple[float, float]]:
        """
        Get the current fist positions.
        
        Returns:
            List of (x, y) positions for each detected fist
        """
        # Apply smoothing by averaging recent positions
        smoothed_positions = []
        
        for hand_id, positions in self.position_history.items():
            if not positions:
                continue
                
            # Simple moving average
            avg_x = sum(p[0] for p in positions) / len(positions)
            avg_y = sum(p[1] for p in positions) / len(positions)
            smoothed_positions.append((avg_x, avg_y))
        
        return smoothed_positions or self.fist_positions
    
    def draw_fists(self, frame):
        """Draw the detected fist positions on the frame with additional debug info."""
        # Draw a larger circle for each fist position
        for x, y in self.fist_positions:
            # Draw outer circle
            cv2.circle(frame, (x, y), 25, (0, 0, 255), 2)
            # Draw inner circle
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            # Draw crosshairs
            cv2.line(frame, (x - 20, y), (x + 20, y), (0, 0, 255), 1)
            cv2.line(frame, (x, y - 20), (x, y + 20), (0, 0, 255), 1)
            # Add position text
            cv2.putText(frame, f'({x}, {y})', (x + 25, y + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            # Draw a border
            cv2.circle(frame, (int(x), int(y)), 
                      config.FIST_RADIUS, (255, 255, 255), 1)
    
    def cleanup(self):
        """Release resources."""
        self.hands.close()
