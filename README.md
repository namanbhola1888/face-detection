# Face Presence Detection

A simple OpenCV-based module that detects whether a face is present in front of the webcam and reports an **Active** or **Away** status — useful for user activity monitoring during a session.

> This is a lightweight learning/demo project focused on **face presence detection**, not face recognition.

## Features

- Live webcam capture using OpenCV
- Face detection with Haar Cascade (`haarcascade_frontalface_default.xml`)
- **Active / Away** state based on face presence
- 2-second timeout to avoid flickering from blinks or brief movement
- Configurable detection settings in `config.py`

## Demo

```bash
python main.py
```

- Sit in front of the camera → **Active** (green box + label)
- Move away for ~2 seconds → **Away** (red label)
- Press `q` or `ESC` to quit

## Setup

**Requirements:** Python 3.8+

```bash
git clone [https://github.com/your-username/face-presence-detection.git](https://github.com/namanbhola1888/face-detection.git)
cd face-presence-detection

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
python main.py
```

## Project Structure

```
├── main.py              # Entry point — camera loop and display
├── face_detector.py     # OpenCV face detection
├── presence_state.py    # Active / Away logic
├── config.py            # Settings and thresholds
├── ARCHITECTURE.md      # System design overview
└── IMPLEMENTATION.md    # Detailed code walkthrough + interview script
```

## How It Works

1. Capture frames from the webcam
2. Every 2nd frame → convert to grayscale → run Haar Cascade face detector
3. Face found → **Active** immediately
4. No face for 2 seconds → **Away**
5. Draw face boxes and status on screen

## Tech Stack

- Python 3
- OpenCV
- NumPy

## Limitations

- Works best with frontal faces and good lighting
- Does not identify *who* the user is — only whether a face is present
- CPU-only; not intended for production-scale deployment

## License

MIT
