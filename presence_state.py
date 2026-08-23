"""Active / Away state logic based on face presence."""

import time

from config import AWAY_TIMEOUT_SECONDS


class PresenceState:
    """
    Tracks whether the user is Active (face present) or Away (no face).

    Uses a timeout so brief missed detections do not immediately switch to Away.
    """

    ACTIVE = "Active"
    AWAY = "Away"

    def __init__(self, away_timeout_seconds=AWAY_TIMEOUT_SECONDS):
        self._away_timeout = away_timeout_seconds
        self._state = self.AWAY
        self._last_face_seen_at = None

    @property
    def state(self):
        return self._state

    def update(self, face_detected):
        """
        Update state based on whether a face was found in the current check.

        Returns the current state after the update.
        """
        now = time.time()

        if face_detected:
            self._last_face_seen_at = now
            self._state = self.ACTIVE
        elif self._last_face_seen_at is None:
            self._state = self.AWAY
        elif now - self._last_face_seen_at >= self._away_timeout:
            self._state = self.AWAY

        return self._state
