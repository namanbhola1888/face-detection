"""Face detection using OpenCV's built-in Haar Cascade classifier."""

import cv2

from config import MIN_FACE_SIZE, MIN_NEIGHBORS, SCALE_FACTOR


class FaceDetector:
    """Detects faces in a camera frame using OpenCV."""

    def __init__(self):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self._classifier = cv2.CascadeClassifier(cascade_path)

        if self._classifier.empty():
            raise RuntimeError(
                "Failed to load Haar Cascade model. "
                "Check that OpenCV is installed correctly."
            )

    def detect(self, frame):
        """
        Find faces in a BGR camera frame.

        Returns a list of (x, y, width, height) rectangles.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = self._classifier.detectMultiScale(
            gray,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_FACE_SIZE,
        )

        return faces
