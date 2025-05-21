import time
from logic.angle_utils import calculate_angle

class PlankTimer:
    def __init__(self, threshold_angle_range=(160, 180), min_duration=1):
        self.threshold = threshold_angle_range
        self.min_duration = min_duration
        self.start_time = None
        self.is_timing = False
        self.total_duration = 0

    def update(self, angle):
        if angle is None:
            self.reset()
            return 0, False

        if self.threshold[0] <= angle <= self.threshold[1]:
            if not self.is_timing:
                if self.start_time is None:
                    self.start_time = time.time()
                elif time.time() - self.start_time >= self.min_duration:
                    self.is_timing = True
            if self.is_timing:
                self.total_duration = time.time() - self.start_time
        else:
            self.reset()

        return round(self.total_duration, 2), self.is_timing

    def reset(self):
        self.start_time = None
        self.is_timing = False
        self.total_duration = 0


class PlankAnalyzer:
    def __init__(self):
        self.timer = PlankTimer()

    def update(self, landmarks, width, height):
        try:
            shoulder = (int(landmarks[11].x * width), int(landmarks[11].y * height))
            hip = (int(landmarks[23].x * width), int(landmarks[23].y * height))
            ankle = (int(landmarks[27].x * width), int(landmarks[27].y * height))

            angle = calculate_angle(shoulder, hip, ankle)
            duration, is_good = self.timer.update(angle)

            if angle is None:
                return 0, "not_visible", "📷 Body not detected clearly."
            elif angle < 150:
                return duration, "hips_down", "🔼 Raise your hips!"
            elif angle > 185:
                return duration, "hips_up", "🔽 Lower your hips!"
            else:
                return duration, "perfect", "💪 Perfect plank! Hold steady."

        except Exception as e:
            return 0, "error", f"[Plank ERROR] {e}"
