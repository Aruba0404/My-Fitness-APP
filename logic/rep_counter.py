from collections import deque
from logic.angle_utils import calculate_angle

class BaseAnalyzer:
    def __init__(self, up_threshold, down_threshold, valid_range):
        self.state = "UP"
        self.rep_count = 0
        self.incorrect_count = 0
        self.prev_angles = deque(maxlen=5)
        self.up_threshold = up_threshold
        self.down_threshold = down_threshold
        self.valid_range = valid_range

    def _smooth_angle(self, angle):
        self.prev_angles.append(angle)
        if len(self.prev_angles) < self.prev_angles.maxlen:
            return angle
        return sum(self.prev_angles) / len(self.prev_angles)

    def get_common_outputs(self, correct, incorrect, feedback, posture_state):
        return {
            "reps": correct,
            "incorrect": incorrect,
            "feedback": feedback,
            "posture": posture_state
        }

class SquatAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=160, down_threshold=90, valid_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            hip = landmarks[23]
            knee = landmarks[25]
            ankle = landmarks[27]

            angle = calculate_angle(hip, knee, ankle)
            angle = self._smooth_angle(angle)

            posture = "unknown"
            feedback = ""

            if angle > self.up_threshold:
                posture = "up"
                feedback = "Stand tall and prepare to squat"
                if self.state == "DOWN":
                    self.rep_count += 1
                    self.state = "UP"
                else:
                    self.state = "UP"

            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture = "perfect"
                feedback = "Perfect squat! ✅"
                if self.state == "UP":
                    self.state = "DOWN"

            elif angle > self.valid_range[1]:
                posture = "too_shallow"
                feedback = "Go lower to reach squat depth ⬇️"

            elif angle < self.valid_range[0]:
                posture = "too_low"
                feedback = "You're going too low ❌"
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
            shoulder = landmarks[11]
            elbow = landmarks[13]
            wrist = landmarks[15]

            angle = calculate_angle(shoulder, elbow, wrist)
            angle = self._smooth_angle(angle)

            posture = "unknown"
            feedback = ""

            if angle > self.up_threshold:
                posture = "up"
                feedback = "Hold plank and stay strong 💪"
                if self.state == "DOWN":
                    self.rep_count += 1
                    self.state = "UP"
                else:
                    self.state = "UP"

            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture = "perfect"
                feedback = "Perfect push-up! ✅"
                if self.state == "UP":
                    self.state = "DOWN"

            elif angle > self.valid_range[1]:
                posture = "too_shallow"
                feedback = "Go lower for a full push-up ⬇️"

            elif angle < self.valid_range[0]:
                posture = "too_low"
                feedback = "Too low! Raise slightly ❌"
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Push-up ERROR] {e}", "error")

class PlankAnalyzer:
    def update(self, landmarks, width, height):
        return {
            "reps": "-",
            "incorrect": "-",
            "feedback": "Plank posture being analyzed...",
            "posture": "plank"
        }
