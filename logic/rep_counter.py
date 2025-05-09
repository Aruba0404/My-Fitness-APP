from collections import deque
from logic.angle_utils import calculate_angle

class BaseAnalyzer:
    def __init__(self, up_threshold, down_threshold, valid_range):
        self.state = "UP"
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

    def get_common_outputs(self, correct, incorrect, feedback, posture_state):
        # Only trigger feedback when posture actually changes
        if posture_state != self.last_posture:
            self.feedback_given = False
            self.last_posture = posture_state

        if not self.feedback_given and feedback:
            self.last_feedback = feedback
            self.feedback_given = True
        else:
            feedback = ""

        return correct, incorrect, feedback, posture_state

class SquatAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=160, down_threshold=90, valid_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            hip, knee, ankle = landmarks[23], landmarks[25], landmarks[27]
            angle = self._smooth_angle(calculate_angle(hip, knee, ankle))

            posture, feedback = "unknown", ""
            if angle > self.up_threshold:
                posture, feedback = "up", "Stand tall and prepare to squat"
                if self.state == "DOWN":
                    self.rep_count += 1
                self.state = "UP"
            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture, feedback = "perfect", "Perfect squat! ✅"
                if self.state == "UP":
                    self.state = "DOWN"
            elif angle > self.valid_range[1]:
                posture, feedback = "too_shallow", "Go lower to reach squat depth ⬇️"
            elif angle < self.valid_range[0]:
                posture, feedback = "too_low", "You're going too low ❌"
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Squat ERROR] {e}", "error")

class PushupAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=150, down_threshold=90, valid_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            shoulder, elbow, wrist = landmarks[11], landmarks[13], landmarks[15]
            angle = self._smooth_angle(calculate_angle(shoulder, elbow, wrist))

            posture, feedback = "unknown", ""
            if angle > self.up_threshold:
                posture, feedback = "up", "Hold plank and stay strong 💪"
                if self.state == "DOWN":
                    self.rep_count += 1
                self.state = "UP"
            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture, feedback = "perfect", "Perfect push-up! ✅"
                if self.state == "UP":
                    self.state = "DOWN"
            elif angle > self.valid_range[1]:
                posture, feedback = "too_shallow", "Go lower for a full push-up ⬇️"
            elif angle < self.valid_range[0]:
                posture, feedback = "too_low", "Too low! Raise slightly ❌"
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Push-up ERROR] {e}", "error")
