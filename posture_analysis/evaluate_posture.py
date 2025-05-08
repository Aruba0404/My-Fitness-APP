import streamlit as st
from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from logic.timer_utils import PlankAnalyzer

# Initialize analyzers once
if "squat_tracker" not in st.session_state:
    st.session_state.squat_tracker = SquatAnalyzer()

if "pushup_tracker" not in st.session_state:
    st.session_state.pushup_tracker = PushupAnalyzer()

if "plank_tracker" not in st.session_state:
    st.session_state.plank_tracker = PlankAnalyzer()

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
            correct, incorrect, feedback, state = st.session_state.squat_tracker.update(landmarks, width, height)
            feedback = get_squat_feedback(state, feedback)
        except Exception as e:
            return 0, 0, f"Squat tracking error: {str(e)}"
        return correct, incorrect, feedback

    # 🤸 PUSH-UP MODE
    elif exercise == "pushups":
        try:
            correct, incorrect, feedback, state = st.session_state.pushup_tracker.update(landmarks, width, height)
            feedback = get_pushup_feedback(state, feedback)
        except Exception as e:
            return 0, 0, f"Push-up tracking error: {str(e)}"
        return correct, incorrect, feedback

    # 🪵 PLANK MODE
    elif exercise == "planks":
        try:
            duration, is_good, feedback = st.session_state.plank_tracker.update(landmarks)
        except Exception as e:
            return 0, 0, f"Plank tracking error: {str(e)}"
        return duration, "-", feedback

    return 0, 0, "Unknown exercise selected."

def get_squat_feedback(state, feedback):
    """Generate feedback based on the squat state."""
    feedback_dict = {
        "too_shallow": "Lower your hips to reach squat depth.",
        "too_low": "You're going too low — raise slightly.",
        "mid": "Almost there. Go slightly deeper.",
        "perfect": "Perfect squat! Hold it.",
        "standing": "Stand tall. Ready for next rep."
    }
    return feedback_dict.get(state, feedback)

def get_pushup_feedback(state, feedback):
    """Generate feedback based on the push-up state."""
    feedback_dict = {
        "too_shallow": "Go lower for a full push-up.",
        "too_low": "Too low — raise slightly.",
        "mid": "Almost there — lower a bit more.",
        "perfect": "Perfect push-up!",
        "up": "Hold the plank position."
    }
    return feedback_dict.get(state, feedback)
