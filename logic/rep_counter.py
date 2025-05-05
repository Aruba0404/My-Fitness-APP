import math
import time
from collections import deque
from logic.angle_utils import calculate_angle


class BaseExerciseAnalyzer:
    def __init__(self, up_threshold, down_threshold, valid_angle_range):
        self.state = "UP"
        self.rep_count = 0
        self.incorrect_count = 0
        self.feedback = ""
        self.prev_angles = deque(maxlen=5)
        self.up_threshold = up_threshold
        self.down_threshold = down_threshold
        self.valid_angle_range = valid_angle_range

    def _update_common(self, avg_angle):
        self.prev_angles.append(avg_angle)
        delta = self.prev_angles[-1] - self.prev_angles[0] if len(self.prev_angles) == 5 else 0
        return delta

    def _check_rep(self, avg_angle, delta):
        raise NotImplementedError("Implement this method in subclasses")

    def update(self, landmarks):
        raise NotImplementedError("Implement this method in subclasses")


class SquatAnalyzer(BaseExerciseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=160, down_threshold=90, valid_angle_range=(80, 100))

    def update(self, landmarks):
        left_angle = calculate_angle(landmarks[23], landmarks[25], landmarks[27])
        right_angle = calculate_angle(landmarks[24], landmarks[26], landmarks[28])
        avg_angle = (left_angle + right_angle) / 2
        delta = self._update_common(avg_angle)

        if avg_angle < self.down_threshold and self.state == "UP" and delta < -10:
            self.state = "DOWN"
            self.feedback = "Going down..."

        elif avg_angle > self.up_threshold and self.state == "DOWN" and delta > 10:
            self.state = "UP"
            if self.valid_angle_range[0] <= min(self.prev_angles) <= self.valid_angle_range[1]:
                self.rep_count += 1
                self.feedback = "✅ Perfect Squat!"
            else:
                self.incorrect_count += 1
                self.feedback = "❌ Incomplete Squat – Try deeper!"

        return self.rep_count, self.feedback, self.incorrect_count


class PushupAnalyzer(BaseExerciseAnalyzer):
    def __init__(self):
        super().__init__(up_threshold=150, down_threshold=90, valid_angle_range=(80, 100))

    def update(self, landmarks):
        left_angle = calculate_angle(landmarks[11], landmarks[13], landmarks[15])
        right_angle = calculate_angle(landmarks[12], landmarks[14], landmarks[16])
        avg_angle = (left_angle + right_angle) / 2
        delta = self._update_common(avg_angle)

        if avg_angle < self.down_threshold and self.state == "UP" and delta < -10:
            self.state = "DOWN"
            self.feedback = "Lowering..."

        elif avg_angle > self.up_threshold and self.state == "DOWN" and delta > 10:
            self.state = "UP"
            if self.valid_angle_range[0] <= min(self.prev_angles) <= self.valid_angle_range[1]:
                self.rep_count += 1
                self.feedback = "✅ Pushup Done!"
            else:
                self.incorrect_count += 1
                self.feedback = "❌ Not Low Enough"

        return self.rep_count, self.feedback, self.incorrect_count
