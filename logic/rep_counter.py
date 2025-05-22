from collections import deque
from logic.angle_utils import calculate_angle
import time


class BaseAnalyzer:
    def __init__(self, up_threshold, down_threshold, valid_range):
        self.state = "UP"  # Initial state: standing/plank up position
        self.rep_count = 0
        self.incorrect_count = 0
        self.prev_angles = deque(maxlen=5)
        self.last_posture = None
        self.last_feedback = ""
        self.feedback_given = False
        self.up_threshold = up_threshold
        self.down_threshold = down_threshold
        self.valid_range = valid_range

    def _smooth_angle(self, angle):
        self.prev_angles.append(angle)
        if len(self.prev_angles) < self.prev_angles.maxlen:
            return angle
        return sum(self.prev_angles) / len(self.prev_angles)

    def _handle_feedback_logic(self, posture_state, feedback_text):
        # Reset feedback if new posture
        if posture_state != self.last_posture:
            self.feedback_given = False
            self.last_posture = posture_state

        # Only give new feedback if not repeated
        if not self.feedback_given and feedback_text:
            self.last_feedback = feedback_text
            self.feedback_given = True
            return feedback_text
        return ""

    def get_common_outputs(self, correct, incorrect, feedback, posture_state):
        filtered_feedback = self._handle_feedback_logic(posture_state, feedback)
        return correct, incorrect, filtered_feedback, posture_state


class SquatAnalyzer(BaseAnalyzer):
    def __init__(self):
        # Squat angle at knee between hip-knee-ankle
        super().__init__(up_threshold=165, down_threshold=90, valid_range=(85, 105))

    def update(self, landmarks, width, height):
        try:
            hip = (int(landmarks[23].x * width), int(landmarks[23].y * height))
            knee = (int(landmarks[25].x * width), int(landmarks[25].y * height))
            ankle = (int(landmarks[27].x * width), int(landmarks[27].y * height))

            angle = self._smooth_angle(calculate_angle(hip, knee, ankle))

            posture, feedback = "unknown", ""

            if angle > self.up_threshold:
                posture = "standing"
                feedback = "Stand tall and prepare to squat"
                if self.state == "DOWN":
                    self.rep_count += 1
                self.state = "UP"

            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture = "perfect"
                feedback = "✅ Perfect squat!"
                if self.state == "UP":
                    self.state = "DOWN"

            elif angle < self.valid_range[0]:
                if angle < 70:
                    posture = "too_low"
                    feedback = "❌ Too deep! Stay above 70°"
                    if self.state == "UP":
                        self.incorrect_count += 1
                        self.state = "DOWN"
                else:
                    posture = "almost_there"
                    feedback = "⬇️ Lower just a bit more"

            elif angle > self.valid_range[1]:
                posture = "too_shallow"
                feedback = "⬇️ Go deeper to reach 90°"

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Squat ERROR] {e}", "error")


class PushupAnalyzer(BaseAnalyzer):
    def __init__(self):
        # Pushup elbow angle between shoulder-elbow-wrist
        super().__init__(up_threshold=150, down_threshold=90, valid_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            shoulder = (int(landmarks[11].x * width), int(landmarks[11].y * height))
            elbow = (int(landmarks[13].x * width), int(landmarks[13].y * height))
            wrist = (int(landmarks[15].x * width), int(landmarks[15].y * height))

            angle = self._smooth_angle(calculate_angle(shoulder, elbow, wrist))

            posture, feedback = "unknown", ""

            if angle > self.up_threshold:
                posture = "up"
                feedback = "💪 Hold plank and stay strong"
                if self.state == "DOWN":
                    self.rep_count += 1
                self.state = "UP"

            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture = "perfect"
                feedback = "✅ Perfect push-up!"
                if self.state == "UP":
                    self.state = "DOWN"

            elif angle < self.valid_range[0]:
                posture = "too_low"
                feedback = "❌ Too low! Lift up slightly"
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            elif angle > self.valid_range[1]:
                posture = "too_shallow"
                feedback = "⬇️ Go lower for full push-up"

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Push-up ERROR] {e}", "error")


class PlankTimer:
    """
    Simple Plank hold timer and feedback system based on elbow angle and time held.
    Counts one 'rep' per successful hold > threshold time.
    """

    def __init__(self, hold_time=30):
        # hold_time in seconds for a successful plank rep
        self.hold_time = hold_time
        self.start_time = None
        self.is_holding = False
        self.rep_count = 0
        self.incorrect_count = 0
        self.last_posture = None
        self.feedback_given = False
        self.last_feedback = ""

    def _handle_feedback_logic(self, posture_state, feedback_text):
        if posture_state != self.last_posture:
            self.feedback_given = False
            self.last_posture = posture_state

        if not self.feedback_given and feedback_text:
            self.last_feedback = feedback_text
            self.feedback_given = True
            return feedback_text
        return ""

    def update(self, landmarks, width, height):
        try:
            shoulder = (int(landmarks[11].x * width), int(landmarks[11].y * height))
            elbow = (int(landmarks[13].x * width), int(landmarks[13].y * height))
            wrist = (int(landmarks[15].x * width), int(landmarks[15].y * height))

            angle = calculate_angle(shoulder, elbow, wrist)

            posture, feedback = "unknown", ""

            # Ideal plank elbow angle ~ 90 degrees (+-15)
            if 75 <= angle <= 105:
                if not self.is_holding:
                    self.start_time = time.time()
                    self.is_holding = True
                elapsed = time.time() - self.start_time
                posture = "holding"
                feedback = f"Hold plank: {int(elapsed)}s / {self.hold_time}s"
                if elapsed >= self.hold_time:
                    self.rep_count += 1
                    feedback = f"✅ Plank hold successful! {self.rep_count} reps"
                    self.is_holding = False  # Reset hold state for next rep
            else:
                if self.is_holding:
                    # Interrupted hold = incorrect rep
                    self.incorrect_count += 1
                    feedback = "❌ Keep your elbows bent at ~90°"
                self.is_holding = False
                self.start_time = None
                posture = "bad_form"

            filtered_feedback = self._handle_feedback_logic(posture, feedback)
            return self.rep_count, self.incorrect_count, filtered_feedback, posture

        except Exception as e:
            return self.rep_count, self.incorrect_count, f"[Plank ERROR] {e}", "error"
