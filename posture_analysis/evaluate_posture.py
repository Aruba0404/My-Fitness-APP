from logic.angle_utils import calculate_angle, SmoothedAngle

class SquatPostureEvaluator:
    def __init__(self):
        self.angle_smoother = SmoothedAngle(maxlen=5)
        self.rep_state = "standing"
        self.correct_reps = 0
        self.incorrect_reps = 0
        self.feedback = "🧍 Stand tall. Get ready!"
        self.last_feedback_state = None

    def update(self, landmarks, width, height):
        if not landmarks or len(landmarks) < 33:
            return self.correct_reps, self.incorrect_reps, "⚠️ Pose not fully visible.", "not_visible"

        left_hip = calculate_angle(landmarks[23], landmarks[25], landmarks[27])
        right_hip = calculate_angle(landmarks[24], landmarks[26], landmarks[28])
        hip = min(left_hip, right_hip)

        hip_smoothed = self.angle_smoother.update(hip)

        if hip_smoothed == -1:
            return self.correct_reps, self.incorrect_reps, "⚠️ Cannot detect squat posture.", "error"
        elif hip_smoothed > 160:
            state, feedback = "standing", "🧍 Stand tall. Ready for next rep!"
        elif 120 < hip_smoothed <= 160:
            state, feedback = "too_shallow", "⬇️ Lower your hips more."
        elif 90 < hip_smoothed <= 120:
            state, feedback = "mid", "↕️ Almost there! Just a bit deeper."
        elif hip_smoothed <= 90:
            state, feedback = "perfect", "✅ Nice squat!"
        else:
            state, feedback = "too_low", "🛑 Too low! Come up slightly."

        if self.rep_state == "standing" and state in ["too_shallow", "mid", "perfect"]:
            self.rep_state = "going_down"
        elif self.rep_state == "going_down" and state == "perfect":
            self.rep_state = "bottom"
        elif self.rep_state == "bottom" and state == "standing":
            self.correct_reps += 1
            self.rep_state = "standing"

        if state != self.last_feedback_state:
            self.feedback = feedback
            self.last_feedback_state = state

        return self.correct_reps, self.incorrect_reps, self.feedback, state


class PushupPostureEvaluator:
    def __init__(self):
        self.angle_smoother = SmoothedAngle(maxlen=5)
        self.rep_state = "start"
        self.correct_reps = 0
        self.incorrect_reps = 0
        self.feedback = "Get ready! Keep elbows close."
        self.last_feedback_state = None

    def update(self, landmarks, width, height):
        if not landmarks or len(landmarks) < 33:
            return self.correct_reps, self.incorrect_reps, "⚠️ Pose not fully visible.", "not_visible"

        left_elbow = calculate_angle(landmarks[11], landmarks[13], landmarks[15])
        right_elbow = calculate_angle(landmarks[12], landmarks[14], landmarks[16])
        elbow_angle = min(left_elbow, right_elbow)

        elbow_smoothed = self.angle_smoother.update(elbow_angle)

        if elbow_smoothed == -1:
            return self.correct_reps, self.incorrect_reps, "⚠️ Elbow not detected properly.", "error"
        elif elbow_smoothed > 160:
            state, feedback = "start", "🧍 Start position. Lower slowly!"
        elif 90 < elbow_smoothed <= 160:
            state, feedback = "going_down", "⬇️ Lower yourself with control."
        elif elbow_smoothed <= 90:
            state, feedback = "bottom", "✅ Great! Now push up!"
        else:
            state, feedback = "too_low", "⬆️ Too low! Come up slightly."

        if self.rep_state == "start" and state == "going_down":
            self.rep_state = "going_down"
        elif self.rep_state == "going_down" and state == "bottom":
            self.rep_state = "bottom"
        elif self.rep_state == "bottom" and state == "start":
            self.correct_reps += 1
            self.rep_state = "start"

        if state != self.last_feedback_state:
            self.feedback = feedback
            self.last_feedback_state = state

        return self.correct_reps, self.incorrect_reps, self.feedback, state


class PlankPostureEvaluator:
    def __init__(self):
        self.start_time = None
        self.feedback = "📏 Keep your body straight!"
        self.state = "start"

    def update(self, landmarks):
        import time

        if not landmarks or len(landmarks) < 33:
            self.start_time = None
            return 0, "not_visible", "⚠️ Pose not fully visible."

        left_angle = calculate_angle(landmarks[11], landmarks[23], landmarks[27])
        right_angle = calculate_angle(landmarks[12], landmarks[24], landmarks[28])
        plank_angle = max(left_angle, right_angle)

        if plank_angle == -1:
            self.start_time = None
            return 0, "error", "⚠️ Cannot detect plank posture."

        if 170 <= plank_angle <= 190:
            state = "perfect"
            if self.start_time is None:
                self.start_time = time.time()
            duration = time.time() - self.start_time
            feedback = "✅ Great plank! Hold steady!"
        elif plank_angle < 170:
            state = "hips_down"
            self.start_time = None
            duration = 0
            feedback = "⬆️ Raise your hips slightly."
        else:
            state = "hips_up"
            self.start_time = None
            duration = 0
            feedback = "⬇️ Lower your hips slightly."

        self.state = state
        self.feedback = feedback
        return round(duration, 1), state, feedback


# Main wrapper function
def evaluate_posture(landmarks, width, height, exercise):
    if not landmarks or len(landmarks) < 33:
        return 0, 0, "⚠️ Pose not fully visible.", "not_visible"

    exercise = exercise.strip().lower()

    global squat_evaluator, pushup_evaluator, plank_evaluator

    if "squat_evaluator" not in globals():
        squat_evaluator = SquatPostureEvaluator()
    if "pushup_evaluator" not in globals():
        pushup_evaluator = PushupPostureEvaluator()
    if "plank_evaluator" not in globals():
        plank_evaluator = PlankPostureEvaluator()

    try:
        if exercise == "squats":
            return squat_evaluator.update(landmarks, width, height)
        elif exercise == "pushups":
            return pushup_evaluator.update(landmarks, width, height)
        elif exercise == "planks":
            return plank_evaluator.update(landmarks)
        else:
            return 0, 0, "⚠️ Unknown exercise selected.", "unknown"
    except Exception as e:
        print(f"[Posture ERROR] {e}")
        return 0, 0, f"❌ Error: {str(e)}", "error"
