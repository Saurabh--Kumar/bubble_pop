# Bubble Pop Game

A fun and interactive game where you pop falling bubbles using your hands, powered by computer vision. Built with Python, OpenCV, and MediaPipe.

📖 [Architecture Documentation](docs/ARCHITECTURE.md) - Learn about the system design and architecture.

## 🎮 Features

- Real-time hand tracking using MediaPipe
- Multiple power-ups (Freeze, Destroy, Heal)
- Score tracking and health system
- Smooth animations and visual effects
- Sound effects and game states
- Configurable game settings

## 🛠️ Prerequisites

- Python 3.8+
- Webcam
- Python packages (install via `requirements.txt`)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bubble_pop.git
   cd bubble_pop
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   .\.venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Play

1. **Start the game**
   ```bash
   python main.py
   ```

2. **Game Controls**
   - Use your fists to pop the falling bubbles
   - Collect power-ups:
     - ❄️ `F` - Freeze: Freezes all bubbles temporarily
     - 💥 `D` - Destroy: Removes all bubbles
     - ❤️ `H` - Health: Restores your health
   - Press `R` to restart after game over
   - Press `Q` or `ESC` to quit

3. **Scoring**
   - Pop a bubble: +1 point
   - Miss a bubble: -10% health
   - Game ends when health reaches 0%

## 🏗️ Project Structure

```
bubble_pop/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # This file
├── assets/                # Game assets
│   └── sounds/            # Sound effects
└── bubble_pop/            # Main package
    ├── __init__.py
    ├── config/            # Game configuration
    │   └── game_config.py
    ├── core/              # Core game logic
    │   ├── game_engine.py
    │   └── game_state.py
    ├── input/             # Input handling
    │   └── hand_tracker.py
    ├── objects/           # Game objects
    │   ├── base_object.py
    │   ├── bubble.py
    │   ├── power.py
    │   └── object_manager.py
    ├── rendering/         # Rendering logic
    │   └── renderer.py
    └── events/            # Event system
        ├── base_event.py
        ├── event_manager.py
        └── observers/     # Event observers
            ├── score_observer.py
            ├── health_observer.py
            ├── sound_observer.py
            ├── spawner_observer.py
            └── freeze_observer.py
```

## 🧪 Testing

The project includes unit tests to ensure code quality and functionality. Here's how to run them:

1. **Install test dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run all tests** with coverage report:
   ```bash
   pytest --cov=./ --cov-report=html
   ```
   This will generate an HTML coverage report in the `htmlcov` directory.

3. **Run specific test files**:
   ```bash
   # Run all tests in a specific file
   pytest tests/test_collision.py -v
   
   # Run a specific test case
   pytest tests/test_event_dispatch.py::TestEventDispatch::test_register_and_notify_observer -v
   ```

4. **Test coverage report**:
   After running tests with coverage, open `htmlcov/index.html` in your browser to see the coverage report.

## ⚙️ Configuration

You can modify game settings in `bubble_pop/config/game_config.py`:
- Window size and FPS
- Game difficulty
- Bubble properties
- Power-up spawn rates
- And more!

## 🎯 Tips

- Make quick, deliberate movements to pop bubbles
- Try to hit multiple bubbles in one motion
- Save power-ups for when you really need them
- Keep an eye on your health!

## 🐛 Troubleshooting

- **Camera not working**
  - Ensure no other application is using the camera
  - Check your system's camera permissions

- **Dependency issues**
  - Make sure you've installed all requirements
  - Try creating a fresh virtual environment

- **Performance problems**
  - Reduce the game resolution in `game_config.py`
  - Close other resource-intensive applications

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) for computer vision
- [MediaPipe](https://mediapipe.dev/) for hand tracking
- [PyGame](https://www.pygame.org/) for audio
- All contributors and testers