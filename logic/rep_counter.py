import math
from collections import deque
from logic.angle_utils import calculate_angle


class BaseAnalyzer:
    def __init__(self, up_threshold, down_threshold, valid_angle_range):
        self.state = "UP"
        self.rep_count = 0
        self.incorrect_count = 0
        self.prev_angles = deque(maxlen=5)
        self.up_threshold = up_threshold
        self.down_threshold = down_threshold
        self.valid_range = valid_angle_range

    def _update_angle(self, angle):
        self.prev_angles.append(angle)
        if len(self.prev_angles) < 5:
            return 0
        return self.prev_angles[-1] - self.prev_angles[0]

    def get_common_outputs(self, correct, incorrect, feedback, posture):
        return correct, incorrect, feedback, posture


class SquatAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=160, down_threshold=90, valid_angle_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            hip = (int(landmarks[23].x * width), int(landmarks[23].y * height))
            knee = (int(landmarks[25].x * width), int(landmarks[25].y * height))
            ankle = (int(landmarks[27].x * width), int(landmarks[27].y * height))
            angle = calculate_angle(hip, knee, ankle)

            delta = self._update_angle(angle)
            feedback = ""
            posture = ""

            if angle > 165:
                posture = "standing"
                feedback = "Stand tall. Prepare for squat."
                self.state = "UP"

            elif 80 <= angle <= 100:
                posture = "perfect"
                feedback = "Perfect squat!"
                if self.state == "UP" and delta < -10:
                    self.rep_count += 1
                    self.state = "DOWN"

            elif angle < 70:
                posture = "too_low"
                feedback = "You're going too low. Raise slightly."
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            elif angle < 80:
                posture = "too_shallow"
                feedback = "Go lower to reach squat depth."

            elif angle > 100:
                posture = "mid"
                feedback = "Almost there. Keep going lower."

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Squat ERROR] {e}", "error")


class PushupAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=150, down_threshold=90, valid_angle_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            shoulder = (int(landmarks[11].x * width), int(landmarks[11].y * height))
            elbow = (int(landmarks[13].x * width), int(landmarks[13].y * height))
            wrist = (int(landmarks[15].x * width), int(landmarks[15].y * height))
            angle = calculate_angle(shoulder, elbow, wrist)

            delta = self._update_angle(angle)
            feedback = ""
            posture = ""

            if angle > 165:
                posture = "up"
                feedback = "Hold the plank position."
                self.state = "UP"

            elif 75 <= angle <= 100:
                posture = "perfect"
                feedback = "Perfect push-up!"
                if self.state == "UP" and delta < -10:
                    self.rep_count += 1
                    self.state = "DOWN"

            elif angle < 60:
                posture = "too_low"
                feedback = "You're going too low. Raise slightly."
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            elif angle < 75:
                posture = "too_shallow"
                feedback = "Go lower for a full push-up."

            elif angle > 100:
                posture = "mid"
                feedback = "Almost there. Lower a bit more."

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Push-up ERROR] {e}", "error")


class PlankAnalyzer:
    def update(self, landmarks, width, height):
        """
        Placeholder for plank analysis logic.
        """
        return "-", "-", "Plank posture being analyzed...", "plank"
