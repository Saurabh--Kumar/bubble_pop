import cv2

def setup_video_capture():
    # Initialize video capture
    cap = cv2.VideoCapture(0)

    # Set full screen properties
    cv2.namedWindow("Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    return cap

def display_frame(frame):
    # Show video frame on screen
    cv2.imshow("Game", frame)