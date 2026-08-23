"""Configuration values for the face presence detection module."""

# Camera index (0 is usually the built-in or first webcam)
CAMERA_INDEX = 0

# How often to run face detection (process every Nth frame)
# Skipping frames reduces CPU usage while keeping detection responsive
PROCESS_EVERY_N_FRAMES = 2

# OpenCV Haar Cascade detection parameters
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5
MIN_FACE_SIZE = (60, 60)

# How long (seconds) with no face before switching to Away
# Prevents flickering when the user blinks or turns slightly
AWAY_TIMEOUT_SECONDS = 2.0

# Window title shown when running the demo
WINDOW_TITLE = "Face Presence Detection"
