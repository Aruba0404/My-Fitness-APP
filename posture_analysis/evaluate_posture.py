import streamlit as st
from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from logic.timer_utils import update_plank_timer

# Initialize analyzers once
if "squat_tracker" not in st.session_state:
    st.session_state.squat_tracker = SquatAnalyzer()
if "pushup_tracker" not in st.session_state:
    st.session_state.pushup_tracker = PushupAnalyzer()

def evaluate_posture(landmarks, width, height, exercise):
    """
    Returns (correct, incorrect, feedback) for squat and push-up.
    For plank, returns (duration, "-", feedback).
    """

    if not landmarks or len(landmarks) < 33:
        return 0, 0, "Pose not fully visible."

    exercise = exercise.strip().lower()

    # 🏋️ SQUAT MODE
    if exercise == "squats":
        try:
            correct, incorrect, feedback, state = st.session_state.squat_tracker.update(
                landmarks, width, height
            )
        except:
            return 0, 0, "Squat tracking error."

        if state == "too_shallow":
            feedback = "Lower your hips to reach squat depth."
        elif state == "too_low":
            feedback = "You're going too low — raise slightly."
        elif state == "mid":
            feedback = "Almost there. Go slightly deeper."
        elif state == "perfect":
            feedback = "Perfect squat! Hold it."
        elif state == "standing":
            feedback = "Stand tall. Ready for next rep."

        return correct, incorrect, feedback

    # 🤸 PUSH-UP MODE
    elif exercise == "push-ups":
        try:
            correct, incorrect, feedback, state = st.session_state.pushup_tracker.update(
                landmarks, width, height
            )
        except:
            return 0, 0, "Push-up tracking error."

        if state == "too_shallow":
            feedback = "Go lower for a full push-up."
        elif state == "too_low":
            feedback = "Too low — raise slightly."
        elif state == "mid":
            feedback = "Almost there — lower a bit more."
        elif state == "perfect":
            feedback = "Perfect push-up!"
        elif state == "up":
            feedback = "Hold the plank position."

        return correct, incorrect, feedback

    # 🪵 PLANK MODE
    elif exercise == "planks":
        try:
            duration, is_good, feedback = update_plank_timer(landmarks, width, height)
        except:
            return 0, 0, "Plank tracking error."
        return duration, "-", feedback

    return 0, 0, "Unknown exercise selected."
