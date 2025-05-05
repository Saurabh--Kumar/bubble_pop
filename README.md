# Fruit Ninja-like Game

This project simulates a basic version of the popular mobile game Fruit Ninja, using computer vision techniques. It utilizes OpenCV for video capture and display, and Google MediaPipe for fist detection to mimic the gameplay mechanics.

## Prerequisites

To run this project, you'll need the following installed on your system:

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

You can install the necessary Python packages using pip:

```bash
pip install opencv-python mediapipe numpy
```

## Project Structure

- **main.py**: The entry point of the application. It integrates all components and runs the game loop.
- **video_capture.py**: Handles video capture and display settings.
- **hand_detection.py**: Sets up hand detection using MediaPipe to track fists.
- **gameplay.py**: Contains the logic for generating, updating, and rendering game objects.

## Setting Up and Running the Game

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd bubble_pop
   ```

2. **Run the Game**:
   - Execute the `main.py` script to start the game:
   ```bash
   python src/main.py
   ```

## Gameplay Instructions

- Ensure your computer's front camera is accessible and unobstructed.
- The game runs in fullscreen mode.
- Hit the falling objects with your fist as detected by the camera to gain points.
- Press 'Q' to exit the game.

## Troubleshooting

- **Camera Issues**: Ensure that your camera is properly connected and the correct drivers are installed.
- **Dependency Errors**: Verify that all required packages are installed with the correct versions.

Feel free to modify the code to adjust object speed, size, and game dynamics to better suit your preferences or screen setup.