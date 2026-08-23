# Face Presence Detection — Complete Implementation Guide

This document walks through every part of the project so you can understand, explain, and demonstrate it confidently.

---

## How to Explain This Feature (Internship Script)

Use this as a spoken script in interviews, project discussions, or while demoing the project. Keep it natural — you do not need to say every line word-for-word.

---

### Short version (~30 seconds)

> "During my internship, I worked on a **face presence detection module** for user activity monitoring. The goal was simple: check whether a user was still in front of the camera during a session.
>
> I used **OpenCV** to capture webcam frames and detect faces using a built-in **Haar Cascade** classifier. If a face was detected, the user was marked as **Active**. If no face was seen for a few seconds, the status changed to **Away**.
>
> I added a small **timeout** so brief missed detections — like blinking or turning slightly — did not cause the status to flicker. The module was kept lightweight and focused only on presence detection, not face recognition."

---

### Full version (~2 minutes)

> "During my internship, I implemented a **face presence detection module** that supported the application's **user activity monitoring** feature.
>
> **The problem:** The application needed to know whether a user was still present and engaged during a session — not who they were, just whether someone was actively in front of the camera.
>
> **My approach:** I built a small module using **Python** and **OpenCV**. The flow was straightforward:
>
> 1. Capture live frames from the user's webcam.
> 2. Convert each frame to grayscale and run OpenCV's **Haar Cascade** face detector on it.
> 3. If a face is found, mark the user as **Active**.
> 4. If no face is found for about **2 seconds**, mark the user as **Away**.
>
> **Why OpenCV and Haar Cascade?** OpenCV is a standard computer vision library, and Haar Cascade comes built in — no extra model downloads, works on CPU, and is fast enough for real-time use. For presence detection, we did not need face recognition; we only needed to answer: *is there a face in the frame?*
>
> **Design decisions I made:**
> - Process every **second frame** instead of every frame to reduce CPU usage.
> - Use a **2-second timeout** before switching to Away, so blinks or small head movements do not cause flickering.
> - Keep detection settings configurable — things like minimum face size and detection strictness — in a separate config file.
>
> **The result:** The module gave the application a reliable **Active / Away** signal that could be used for session monitoring — for example, detecting when a user stepped away from their desk.
>
> **Limitations I was aware of:** It works best with frontal faces and good lighting. It does not identify the person — only whether a face is present. In a production setting, you could improve it with a more modern detector or expose the status through an API for other parts of the system."

---

### If they ask you to walk through the code

> "The project is split into small, clear parts:
>
> - **`main.py`** — opens the camera, runs the loop, and displays the result.
> - **`face_detector.py`** — handles the OpenCV face detection logic.
> - **`presence_state.py`** — tracks Active or Away based on whether a face was recently seen.
> - **`config.py`** — holds all the thresholds and settings.
>
> The camera sends frames continuously. Every second frame goes to the face detector. The result updates the presence state, and the status is shown on screen. When the user closes the app, the camera is released cleanly."

---

### If they ask "What was your role?" or "What did you specifically do?"

> "I implemented the detection module end to end — setting up the camera input, integrating OpenCV's face detector, writing the Active/Away logic with a timeout to handle edge cases, and tuning parameters like detection sensitivity and the away timeout. I also made sure the module was simple and easy to plug into the larger application's activity monitoring flow."

---

### If they ask "What challenges did you face?"

> "The main challenges were **false detections** in busy backgrounds, **missed detections** in poor lighting, and **status flickering** when the user blinked or moved slightly.
>
> I handled flickering with a timeout — the status only goes to Away after 2 seconds of no detection. For false positives, I tuned `minNeighbors` and minimum face size. For lighting, I applied histogram equalization on the grayscale frame before detection. These are simple fixes, but they made the module much more stable in practice."

---

### Demo script (while running `python main.py`)

> "Let me show you quickly. When I sit in front of the camera, you can see a green box around my face and the status shows **Active**. If I move away and stay out of frame for a couple of seconds, it switches to **Away**. When I come back, it goes to **Active** again immediately. The 2-second delay prevents it from flickering when I blink or turn my head slightly."

---

### One-line summary (for resume follow-ups)

> "I built a lightweight OpenCV module that monitors webcam input, detects face presence using Haar Cascade, and outputs an Active/Away state for session activity tracking."

---

## 1. Project Structure

```
Face Detection/
├── main.py              ← Start here. Runs the camera loop and display.
├── face_detector.py     ← Finds faces in a frame using OpenCV.
├── presence_state.py    ← Tracks Active / Away status.
├── config.py            ← All settings (thresholds, camera index, etc.)
├── requirements.txt     ← Python package: opencv-python
├── ARCHITECTURE.md      ← System design overview
└── IMPLEMENTATION.md    ← This file
```

**How to run:**
```bash
pip install -r requirements.txt
python main.py
```

Press `q` or `ESC` to stop.

---

## 2. Technologies and Libraries

| Technology        | Role                                              |
|-------------------|---------------------------------------------------|
| **Python 3**      | Programming language                              |
| **OpenCV**        | Camera capture, image processing, face detection  |
| **NumPy**         | Array format for images (comes with OpenCV)       |

Only one external package is needed: `opencv-python`.

---

## 3. How Camera Input Is Captured

The webcam is opened using OpenCV's `VideoCapture` class:

```python
camera = cv2.VideoCapture(0)   # 0 = first webcam
success, frame = camera.read() # read one frame
```

- `success` — `True` if a frame was read successfully
- `frame` — a NumPy array representing the image in **BGR** color format (Blue, Green, Red — OpenCV's default)

Frames are read continuously inside a `while True` loop, roughly 30 times per second (depending on the camera).

---

## 4. How OpenCV Processes Frames

For each frame that is selected for detection:

```
Step 1: Receive color frame (BGR, from camera)
Step 2: Convert to grayscale (single channel — faster to process)
Step 3: Apply histogram equalization (improve contrast)
Step 4: Pass grayscale image to Haar Cascade classifier
Step 5: Receive list of face rectangles (or empty list)
```

OpenCV functions used:

| Function                        | Purpose                                    |
|---------------------------------|--------------------------------------------|
| `cv2.cvtColor()`                | Convert BGR → grayscale                    |
| `cv2.equalizeHist()`            | Improve brightness/contrast distribution   |
| `cv2.CascadeClassifier()`       | Load the face detection model              |
| `detectMultiScale()`            | Scan image at multiple sizes for faces     |
| `cv2.rectangle()`               | Draw green box around detected face        |
| `cv2.putText()`                 | Draw Active/Away label on screen           |
| `cv2.imshow()`                  | Display the frame in a window              |
| `cv2.waitKey()`                 | Wait for keyboard input (to detect quit)   |

---

## 5. Face Detection Method and Why It Was Chosen

**Method:** OpenCV Haar Cascade Classifier  
**Model file:** `haarcascade_frontalface_default.xml` (included with OpenCV)

**Why this method:**
- Built into OpenCV — no separate download
- Fast on a normal CPU — no GPU needed
- Well-documented and widely used in tutorials
- Good enough for "is someone there?" — which is all this project needs
- Easy to explain in an interview

**Alternatives considered (not used):**
- **YuNet / DNN-based detectors** — more accurate but need extra model files
- **MediaPipe** — Google's library, very accurate, but adds a dependency outside OpenCV
- **Face recognition (e.g., face_recognition library)** — identifies *who*, not just *if* — overkill for presence detection

---

## 6. How Face Detection Works (Basic Level)

Haar Cascade detection works in three simple ideas:

1. **Features:** The model knows simple patterns that faces have — for example, eyes are darker than cheeks, and the nose area is brighter than the eye region. These are called Haar-like features.

2. **Cascade:** Instead of checking every possible location at full detail, the detector uses a "cascade" of stages. Easy checks happen first; if a region fails early, it is discarded quickly. This makes it fast.

3. **Multi-scale scanning:** Faces can appear at different sizes depending on distance from the camera. `detectMultiScale()` shrinks the image step by step (`scaleFactor=1.1`) and runs the detector at each size.

**Result:** A list of rectangles `(x, y, width, height)` — one per detected face. An empty list means no face was found.

---

## 7. Important Functions — Detailed Explanation

---

### `run()` — main.py

**Purpose:** Main entry point. Opens the camera, runs the detection loop, and handles cleanup.

**Input:** None

**Logic:**
1. Call `open_camera()` to connect to the webcam
2. Create a `FaceDetector` and `PresenceState` object
3. Enter a loop:
   - Read a frame from the camera
   - Every 2nd frame (`PROCESS_EVERY_N_FRAMES`): run face detection and update presence state
   - Draw face boxes and status label on the frame
   - Show the frame in a window
   - Check if user pressed `q` or `ESC` → if yes, break
4. In the `finally` block: release camera and close windows

**Output:** Runs until the user quits. Prints start/stop messages to the terminal.

---

### `open_camera(index)` — main.py

**Purpose:** Safely open the webcam and confirm it can actually read frames.

**Input:** `index` — integer camera ID (0 for default webcam)

**Logic:**
1. Create `cv2.VideoCapture(index)`
2. Check `camera.isOpened()` — if False, return None
3. Try reading one test frame — if it fails, release camera and return None
4. Return the working camera object

**Output:** A working `VideoCapture` object, or `None` if the camera is unavailable.

**Why the test read?** Some systems report the camera as "open" but cannot actually deliver frames. The test read catches this early.

---

### `draw_overlay(frame, faces, state)` — main.py

**Purpose:** Draw visual feedback on the camera frame before displaying it.

**Input:**
- `frame` — the current camera image
- `faces` — list of `(x, y, w, h)` rectangles from the detector
- `state` — `"Active"` or `"Away"` string

**Logic:**
1. For each face rectangle: draw a green box using `cv2.rectangle()`
2. Choose label color: green for Active, red for Away
3. Write `"Status: Active"` or `"Status: Away"` at the top-left using `cv2.putText()`

**Output:** The same frame, now annotated (modified in place).

---

### `FaceDetector.__init__()` — face_detector.py

**Purpose:** Load the Haar Cascade model when the detector is created.

**Input:** None

**Logic:**
1. Build the path to `haarcascade_frontalface_default.xml` using `cv2.data.haarcascades`
2. Load it into a `cv2.CascadeClassifier`
3. If loading failed (`classifier.empty()`), raise an error

**Output:** A ready-to-use `FaceDetector` object.

---

### `FaceDetector.detect(frame)` — face_detector.py

**Purpose:** Find all faces in one camera frame.

**Input:** `frame` — BGR color image (NumPy array from the camera)

**Logic:**
1. Convert frame to grayscale: `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`
2. Improve contrast: `cv2.equalizeHist(gray)`
3. Run detection:
   ```python
   faces = classifier.detectMultiScale(
       gray,
       scaleFactor=1.1,    # shrink 10% at each step
       minNeighbors=5,     # need 5 overlapping detections to confirm
       minSize=(60, 60),   # ignore detections smaller than 60×60 pixels
   )
   ```
4. Return the list of face rectangles

**Output:** List of `(x, y, width, height)` tuples. Empty list `[]` if no face found.

---

### `PresenceState.__init__(away_timeout_seconds)` — presence_state.py

**Purpose:** Initialize the state tracker.

**Input:** `away_timeout_seconds` — how long to wait before switching to Away (default: 2.0)

**Logic:**
- Set initial state to `"Away"`
- Set `_last_face_seen_at` to `None` (no face seen yet)

**Output:** A `PresenceState` object starting in Away state.

---

### `PresenceState.update(face_detected)` — presence_state.py

**Purpose:** Update Active/Away status based on the latest detection result.

**Input:** `face_detected` — boolean, `True` if at least one face was found

**Logic:**
```
IF face_detected is True:
    record current time as last_face_seen_at
    set state = "Active"

ELSE (no face detected):
    IF no face has ever been seen:
        state = "Away"
    ELSE IF (current time - last_face_seen_at) >= 2 seconds:
        state = "Away"
    ELSE:
        keep state = "Active"  (grace period)
```

**Output:** Returns the current state string (`"Active"` or `"Away"`).

---

## 8. Active / Away Decision — Full Logic

```
Every 2nd frame:
    Run face detection
    │
    ├── Face found → presence.update(True)
    │       → state = Active immediately
    │       → last_face_seen_at = now
    │
    └── No face   → presence.update(False)
            │
            ├── Never seen a face before → Away
            ├── Last face seen < 2 sec ago → stay Active (grace period)
            └── Last face seen ≥ 2 sec ago → Away
```

**Why immediate Active but delayed Away?**
- When you return to the desk, you want the system to recognize you instantly.
- When you leave, a 2-second delay prevents false Away triggers from blinks or brief movements.

---

## 9. Continuous Detection — How the Loop Works

```python
while True:
    success, frame = camera.read()       # 1. Get frame (~30 FPS)
    frame_count += 1

    if frame_count % 2 == 0:             # 2. Detect every 2nd frame
        last_faces = detector.detect(frame)
        presence.update(len(last_faces) > 0)

    draw_overlay(frame, last_faces, presence.state)  # 3. Draw
    cv2.imshow(WINDOW_TITLE, frame)      # 4. Show

    if key == 'q' or ESC: break          # 5. Check quit
```

The loop runs as fast as the camera delivers frames. Detection runs at half that rate. The display always shows the most recent detection result.

---

## 10. What Happens When a Face Is Detected

1. `detectMultiScale()` returns one or more rectangles
2. `presence.update(True)` is called
3. State immediately becomes `"Active"`
4. `_last_face_seen_at` is updated to the current time
5. Green rectangle(s) drawn around the face(s)
6. Green `"Status: Active"` text shown at top of window

---

## 11. What Happens When No Face Is Detected

1. `detectMultiScale()` returns an empty list
2. `presence.update(False)` is called
3. System checks how long since the last face was seen:
   - Less than 2 seconds → status stays `"Active"` (grace period)
   - 2+ seconds → status becomes `"Away"`
4. No rectangles drawn
5. Red `"Status: Away"` text shown at top of window

---

## 12. How the Program Starts and Stops

**Start:**
```bash
python main.py
```
- Camera opens
- Haar Cascade model loads
- Window appears with live feed
- Terminal prints: `"Face Presence Detection started."`

**Stop:**
- Press `q` or `ESC`
- Loop breaks
- `finally` block runs:
  - `camera.release()` — frees the webcam
  - `cv2.destroyAllWindows()` — closes all OpenCV windows
- Terminal prints: `"Face Presence Detection stopped."`

The `finally` block guarantees cleanup even if an unexpected error occurs mid-loop.

---

## 13. Important Parameters and Thresholds

| Parameter                | Value   | What it controls                              |
|--------------------------|---------|-----------------------------------------------|
| `CAMERA_INDEX`           | 0       | Which camera to use                           |
| `PROCESS_EVERY_N_FRAMES` | 2       | Detect every 2nd frame                        |
| `SCALE_FACTOR`           | 1.1     | Image shrink step during multi-scale scan     |
| `MIN_NEIGHBORS`          | 5       | Detection strictness (higher = fewer false positives) |
| `MIN_FACE_SIZE`          | (60,60) | Minimum face size in pixels to accept         |
| `AWAY_TIMEOUT_SECONDS`   | 2.0     | Seconds without face before going Away        |

---

## 14. Why These Parameters Were Chosen

**`PROCESS_EVERY_N_FRAMES = 2`**
At 30 FPS, detecting 15 times per second is plenty for a 2-second timeout. Halves CPU usage with no noticeable impact on responsiveness.

**`SCALE_FACTOR = 1.1`**
A 10% shrink at each step gives a good balance between detection speed and accuracy. Smaller steps (e.g., 1.05) are slower but catch more sizes. Larger steps (e.g., 1.3) are faster but may miss faces at certain distances.

**`MIN_NEIGHBORS = 5`**
OpenCV's recommended starting value. Lower values (3) detect more faces but increase false positives. Higher values (7+) are stricter. Five is a practical default for a webcam setup.

**`MIN_FACE_SIZE = (60, 60)`**
Faces smaller than 60×60 pixels are likely far away or noise. Ignoring them reduces false detections on background patterns.

**`AWAY_TIMEOUT_SECONDS = 2.0`**
A blink takes ~300 ms. Looking down briefly might take 1 second. Two seconds covers normal micro-movements without keeping Away status stuck on Active when the user has actually left.

---

## 15. Limitations

| Limitation                          | Explanation                                           |
|-------------------------------------|-------------------------------------------------------|
| Frontal faces only                  | Side profiles or back of head are not detected        |
| Lighting dependent                  | Very dark or backlit scenes reduce accuracy           |
| No identity check                   | Cannot tell *who* is present, only *that* someone is  |
| Single camera                       | No support for multiple camera inputs                 |
| CPU-only                            | No GPU acceleration; may be slow on very old hardware |
| False positives possible            | Posters, photos, or patterns may trigger detection    |
| No network/API                      | Status is local only; not exposed to other systems    |
| Blocking loop                       | Runs in main thread; not suitable for complex UIs without refactoring |

---

## 16. Possible Future Improvements

| Improvement                        | Benefit                                           |
|------------------------------------|---------------------------------------------------|
| Use YuNet or MediaPipe detector    | Better accuracy, especially in varied lighting    |
| Add a callback/event system        | Notify other modules when state changes           |
| Expose status via a simple REST API| Allow web apps to read Active/Away state          |
| Add a configurable UI settings panel| Let users tune thresholds without editing code   |
| Save session logs                  | Record Active/Away timestamps for analytics       |
| Multi-threading                    | Separate capture and detection threads for smoother FPS |
| Region of Interest (ROI)           | Only scan the center of the frame where the user sits |
| Confidence score threshold         | Filter out low-confidence detections              |

---

## 17. Potential Interview Questions & Answers

### Why OpenCV?

It is free, widely used, has built-in face detection, works on CPU, and has excellent Python support. For a simple presence check, it is the most practical choice.

### Why Haar Cascade and not a neural network?

Haar Cascade is built into OpenCV, requires no extra downloads, runs fast on CPU, and is sufficient for detecting whether *a* face is present. Neural networks add complexity that is not needed for this use case.

### How does Haar Cascade detect a face?

It scans the image at multiple sizes looking for simple brightness patterns typical of faces (dark eye region, lighter cheeks). A cascade of classifiers filters out non-face regions quickly. Regions that pass all stages are reported as faces.

### How are camera frames captured?

`cv2.VideoCapture(0)` opens the default webcam. `camera.read()` returns one frame per call as a NumPy array in BGR format. This happens in a loop ~30 times per second.

### How is a face detected in a frame?

The color frame is converted to grayscale, contrast is improved with histogram equalization, then `detectMultiScale()` scans the image and returns rectangles around detected faces.

### How is Active/Away status determined?

Active = face detected now, or face was seen within the last 2 seconds. Away = no face detected for 2 or more continuous seconds.

### What if multiple faces are detected?

Any face counts as "present." If one or more faces are found, status is Active. This is correct for a general session monitor.

### What if the face moves?

Movement may cause 1–2 missed frames, but the 2-second timeout prevents status from changing. As long as the face returns to view within 2 seconds, status stays Active.

### What happens in low light?

Detection becomes less reliable because facial feature contrast is reduced. Histogram equalization helps moderately. Good lighting is the best fix.

### What if the face is partially covered (mask, hand)?

Partial coverage may cause missed detections. Haar Cascade needs eyes and nose region visible for reliable detection. A mask covering the lower face may still work; covering eyes will likely fail.

### How can false detections happen?

Patterns that resemble face features — photos, posters, dolls, or high-contrast objects — may trigger detection. Increasing `MIN_NEIGHBORS` and `MIN_FACE_SIZE` reduces this.

### How can false detections be reduced?

- Increase `MIN_NEIGHBORS` from 5 to 7
- Increase `MIN_FACE_SIZE` to (80, 80)
- Ensure the camera is not pointed at posters or screens showing faces
- Improve lighting so real faces have clearer contrast

### Why was MIN_NEIGHBORS = 5 chosen?

It is OpenCV's recommended default. It balances sensitivity (detecting real faces) with specificity (avoiding false positives). Good starting point for a webcam at arm's length.

### Why not process every frame?

Detection is the slowest step. At 30 FPS with a 2-second timeout, detecting 15 times per second is more than sufficient. Skipping every other frame saves ~50% CPU.

### Performance / CPU / FPS considerations?

Typical CPU usage: low to moderate (10–30% on a modern laptop). Display runs at camera FPS (~30). Detection runs at half that (~15/sec). Memory usage is minimal — only the current frame and model are in memory.

### What if the camera fails or is unavailable?

`open_camera()` checks both `isOpened()` and reads a test frame. If either fails, the program prints an error message and exits cleanly without crashing.

### What if there is no camera input (frame read fails mid-run)?

The loop prints a warning and breaks. The `finally` block releases the camera and closes windows.

### What happens when the application is closed?

Pressing `q` or ESC breaks the loop. `camera.release()` frees the webcam. `cv2.destroyAllWindows()` closes the display. No background processes remain.

### Security and privacy?

All processing is local. No images are saved, uploaded, or transmitted. In a production system, users should be notified that the camera is active and given an opt-out.

### How could this integrate into a larger application?

Import `PresenceState` and `FaceDetector` into the main app. Poll `presence.state` periodically, or add a callback in `PresenceState.update()` that fires when the state changes. A web backend could expose the state via an API endpoint.

### How could the module communicate Active/Away to another system?

Options: (1) shared variable polled by another thread, (2) callback function called on state change, (3) message queue (e.g., Redis pub/sub), (4) HTTP endpoint returning current state.

### Alternatives to OpenCV?

- **MediaPipe** (Google) — very accurate, easy API, but separate library
- **dlib** — good detection + recognition, heavier install
- **face_recognition** — built on dlib, focused on recognition
- **YOLO / SSD** — deep learning, very accurate, needs GPU for real-time

For a simple presence check, OpenCV Haar Cascade is the most lightweight option.

### Face detection vs face recognition?

| | Face Detection | Face Recognition |
|---|---|---|
| Question answered | Is there a face? | Whose face is it? |
| Output | Face location (rectangle) | Person identity (name/ID) |
| Complexity | Low | High |
| Needed here? | Yes | No |

### Why is face recognition not required?

The resume point says "face presence detection" — monitoring whether the user is active or away. Knowing *who* the user is adds complexity, privacy concerns, and training data requirements that are unnecessary for an activity monitor.

---

## 18. Challenges and Solutions

### False face detections

**Problem:** System shows Active when no one is in front of the camera.  
**Why it happens:** Haar Cascade matches face-like patterns in backgrounds, posters, or screens.  
**Simple solution:** Increase `MIN_NEIGHBORS` to 7 and `MIN_FACE_SIZE` to (80, 80).  
**Why it works:** Stricter thresholds require stronger pattern matches, filtering out weak false positives.

---

### Missed detections

**Problem:** User is present but status shows Away.  
**Why it happens:** Poor lighting, face turned away, or user too far from camera.  
**Simple solution:** Improve lighting, adjust camera angle, and rely on the 2-second timeout to absorb brief misses.  
**Why it works:** The timeout prevents a single missed frame from triggering Away; consistent misses over 2 seconds correctly indicate the user left.

---

### Poor lighting

**Problem:** Detection fails in a dark room or with strong backlight.  
**Why it happens:** Haar features rely on contrast between eyes, nose, and cheeks — low contrast makes these invisible.  
**Simple solution:** Histogram equalization (already in code) plus asking the user to face a light source.  
**Why it works:** Equalization redistributes pixel brightness, making dark features more distinguishable.

---

### Camera positioning

**Problem:** Face is partially out of frame or too small to detect.  
**Why it happens:** Camera mounted too high, too low, or user sits too far away.  
**Simple solution:** Mount camera at eye level, about an arm's length from the user.  
**Why it works:** Frontal face detection needs the full face visible and at least 60×60 pixels in the frame.

---

### Face movement

**Problem:** Status flickers between Active and Away when the user moves.  
**Why it happens:** Motion blur or temporary feature hiding causes missed detections.  
**Simple solution:** The 2-second Away timeout.  
**Why it works:** Normal head movements cause gaps of less than 2 seconds; the status stays Active throughout.

---

### Processing every frame is expensive

**Problem:** High CPU usage, fan noise, or laggy display.  
**Why it happens:** `detectMultiScale()` is the heaviest operation in the loop.  
**Simple solution:** `PROCESS_EVERY_N_FRAMES = 2`.  
**Why it works:** Halves detection calls with no practical impact on a 2-second timeout window.

---

### Temporary detection failures

**Problem:** A blink or sneeze causes a momentary switch to Away.  
**Why it happens:** Eyes closed for ~300 ms — one to two frames have no detectable face.  
**Simple solution:** `AWAY_TIMEOUT_SECONDS = 2.0`.  
**Why it works:** Blinks are far shorter than 2 seconds; status remains Active.

---

### Camera access problems

**Problem:** `"Error: Could not open the camera."`  
**Why it happens:** Webcam not connected, in use by another app, or wrong index.  
**Simple solution:** Close other apps using the camera. Try `CAMERA_INDEX = 1`. Reconnect the webcam.  
**Why it works:** `open_camera()` validates both open status and readable frames, giving a clear early failure message instead of a silent hang.
