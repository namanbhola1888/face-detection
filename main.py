"""
Face Presence Detection demo.

Captures webcam frames, detects faces with OpenCV, and shows Active/Away status.
Press 'q' or ESC to quit.
"""

import sys

import cv2

from config import (
    CAMERA_INDEX,
    PROCESS_EVERY_N_FRAMES,
    WINDOW_TITLE,
)
from face_detector import FaceDetector
from presence_state import PresenceState


def draw_overlay(frame, faces, state):
    """Draw face boxes and the current Active/Away label on the frame."""
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    color = (0, 200, 0) if state == PresenceState.ACTIVE else (0, 0, 255)
    cv2.putText(
        frame,
        f"Status: {state}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        color,
        2,
        cv2.LINE_AA,
    )


def open_camera(index):
    """Open the webcam and verify that frames can be read."""
    camera = cv2.VideoCapture(index)

    if not camera.isOpened():
        return None

    success, _ = camera.read()
    if not success:
        camera.release()
        return None

    return camera


def run():
    camera = open_camera(CAMERA_INDEX)
    if camera is None:
        print("Error: Could not open the camera.")
        print("Check that a webcam is connected and not used by another app.")
        sys.exit(1)

    detector = FaceDetector()
    presence = PresenceState()

    frame_count = 0
    last_faces = []

    print("Face Presence Detection started.")
    print("Press 'q' or ESC to stop.")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Warning: Failed to read a frame from the camera.")
                break

            frame_count += 1

            if frame_count % PROCESS_EVERY_N_FRAMES == 0:
                last_faces = detector.detect(frame)
                face_detected = len(last_faces) > 0
                presence.update(face_detected)

            draw_overlay(frame, last_faces, presence.state)
            cv2.imshow(WINDOW_TITLE, frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("Face Presence Detection stopped.")


if __name__ == "__main__":
    run()
