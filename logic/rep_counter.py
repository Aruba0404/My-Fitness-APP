from collections import deque
from logic.angle_utils import calculate_angle

# ------------------- Base Class -------------------

class BaseAnalyzer:
    def __init__(self, up_threshold, down_threshold, valid_range):
        self.state = "UP"  # Start in UP position
        self.rep_count = 0
        self.incorrect_count = 0
        self.prev_angles = deque(maxlen=5)
        self.up_threshold = up_threshold
        self.down_threshold = down_threshold
        self.valid_range = valid_range
        self.ready_for_count = False  # True when full movement completed

    def _update_angle(self, angle):
        self.prev_angles.append(angle)
        if len(self.prev_angles) < self.prev_angles.maxlen:
            return 0
        return self.prev_angles[-1] - self.prev_angles[0]

    def get_common_outputs(self, correct, incorrect, feedback, posture_state):
        return {
            "reps": correct,
            "incorrect": incorrect,
            "feedback": feedback,
            "posture": posture_state
        }

# ------------------- Squat Analyzer -------------------

class SquatAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=160, down_threshold=90, valid_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            hip = (int(landmarks[23].x * width), int(landmarks[23].y * height))
            knee = (int(landmarks[25].x * width), int(landmarks[25].y * height))
            ankle = (int(landmarks[27].x * width), int(landmarks[27].y * height))

            angle = calculate_angle(hip, knee, ankle)
            delta = self._update_angle(angle)

            posture = "unknown"
            feedback = ""

            # Standing position (UP)
            if angle > self.up_threshold:
                posture = "up"
                feedback = "Stand tall and prepare to squat"
                if self.state == "DOWN":
                    self.rep_count += 1
                    self.state = "UP"
                else:
                    self.state = "UP"

            # Valid squat range (DOWN)
            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture = "perfect"
                feedback = "Perfect squat! ✅"
                if self.state == "UP":
                    self.state = "DOWN"

            # Too shallow
            elif angle > self.valid_range[1]:
                posture = "too_shallow"
                feedback = "Go lower to reach squat depth ⬇️"

            # Too low
            elif angle < self.valid_range[0]:
                posture = "too_low"
                feedback = "You're going too low ❌"
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Squat ERROR] {e}", "error")

# ------------------- Push-up Analyzer -------------------

class PushupAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=150, down_threshold=90, valid_range=(80, 100))

    def update(self, landmarks, width, height):
        try:
            shoulder = (int(landmarks[11].x * width), int(landmarks[11].y * height))
            elbow = (int(landmarks[13].x * width), int(landmarks[13].y * height))
            wrist = (int(landmarks[15].x * width), int(landmarks[15].y * height))

            angle = calculate_angle(shoulder, elbow, wrist)
            delta = self._update_angle(angle)

            posture = "unknown"
            feedback = ""

            # UP / Plank position
            if angle > self.up_threshold:
                posture = "up"
                feedback = "Hold plank and stay strong 💪"
                if self.state == "DOWN":
                    self.rep_count += 1
                    self.state = "UP"
                else:
                    self.state = "UP"

            # Valid push-up range
            elif self.valid_range[0] <= angle <= self.valid_range[1]:
                posture = "perfect"
                feedback = "Perfect push-up! ✅"
                if self.state == "UP":
                    self.state = "DOWN"

            # Too shallow
            elif angle > self.valid_range[1]:
                posture = "too_shallow"
                feedback = "Go lower for a full push-up ⬇️"

            # Too low
            elif angle < self.valid_range[0]:
                posture = "too_low"
                feedback = "Too low! Raise slightly ❌"
                if self.state == "UP":
                    self.incorrect_count += 1
                    self.state = "DOWN"

            return self.get_common_outputs(self.rep_count, self.incorrect_count, feedback, posture)

        except Exception as e:
            return self.get_common_outputs(self.rep_count, self.incorrect_count, f"[Push-up ERROR] {e}", "error")

# ------------------- Plank Placeholder -------------------

class PlankAnalyzer:
    def update(self, landmarks, width, height):
        return {
            "reps": "-",
            "incorrect": "-",
            "feedback": "Plank posture being analyzed...",
            "posture": "plank"
        }
