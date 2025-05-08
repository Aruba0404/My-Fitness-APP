import time
import math

class PlankTimer:
    def __init__(self, threshold_angle_range=(160, 180), min_duration=1):
        self.threshold_angle_range = threshold_angle_range
        self.min_duration = min_duration
        self.start_time = None
        self.is_timing = False
        self.total_duration = 0

    def update(self, angle):
        if angle is None:
            self.reset()
            return 0, False

        if self.threshold_angle_range[0] <= angle <= self.threshold_angle_range[1]:
            if not self.is_timing:
                if self.start_time is None:
                    self.start_time = time.time()
                elif time.time() - self.start_time >= self.min_duration:
                    self.is_timing = True
            if self.is_timing:
                self.total_duration = time.time() - self.start_time
        else:
            if self.is_timing:
                self.reset()

        return round(self.total_duration, 2), self.is_timing

    def reset(self):
        self.start_time = None
        self.is_timing = False
        self.total_duration = 0

def calculate_angle(a, b, c):
    try:
        a = [a.x, a.y]
        b = [b.x, b.y]
        c = [c.x, c.y]

        ba = [a[0] - b[0], a[1] - b[1]]
        bc = [c[0] - b[0], c[1] - b[1]]

        dot_product = ba[0] * bc[0] + ba[1] * bc[1]
        magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
        magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

        angle = math.degrees(math.acos(dot_product / (magnitude_ba * magnitude_bc)))
        return angle
    except Exception as e:
        print(f"[ERROR] Angle calculation failed: {e}")
        return None

# 🔍 PlankAnalyzer now returns posture state and detailed feedback
class PlankAnalyzer:
    def __init__(self):
        self.timer = PlankTimer()

    def update(self, landmarks):
        try:
            left_shoulder = landmarks[11]
            left_hip = landmarks[23]
            left_ankle = landmarks[27]

            angle = calculate_angle(left_shoulder, left_hip, left_ankle)
            duration, is_good = self.timer.update(angle)

            # Classify posture state
            if angle is None:
                state = "not_visible"
                feedback = "Body not detected clearly. 📷"
            elif angle < 150:
                state = "hips_down"
                feedback = "Raise your hips! 🔼"
            elif angle > 185:
                state = "hips_up"
                feedback = "Lower your hips! 🔽"
            else:
                state = "perfect"
                feedback = "Perfect plank! Hold steady. 💪"

            return round(duration, 2), is_good, feedback
        except Exception as e:
            return 0, False, f"[Plank ERROR] {e}"
