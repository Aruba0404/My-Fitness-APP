import streamlit as st
from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from utils.timer_utils import PlankAnalyzer

# Initialize analyzers only once
if "squat_tracker" not in st.session_state:
    st.session_state.squat_tracker = SquatAnalyzer()

if "pushup_tracker" not in st.session_state:
    st.session_state.pushup_tracker = PushupAnalyzer()

if "plank_tracker" not in st.session_state:
    st.session_state.plank_tracker = PlankAnalyzer()

def evaluate_posture(landmarks, width, height, exercise):
    if not landmarks or len(landmarks) < 33:
        return 0, 0, "⚠️ Pose not fully visible.", "not_visible"

    exercise = exercise.strip().lower()

    try:
        if exercise == "squats":
            correct, incorrect, raw_feedback, state = st.session_state.squat_tracker.update(landmarks, width, height)
            return correct, incorrect, get_squat_feedback(state, raw_feedback), state

        elif exercise == "pushups":
            correct, incorrect, raw_feedback, state = st.session_state.pushup_tracker.update(landmarks, width, height)
            return correct, incorrect, get_pushup_feedback(state, raw_feedback), state

        elif exercise == "planks":
            duration, state, raw_feedback = st.session_state.plank_tracker.update(landmarks)
            return duration, "-", get_plank_feedback(state, raw_feedback), state

        else:
            return 0, 0, "⚠️ Unknown exercise selected.", "unknown"

    except Exception as e:
        return 0, 0, f"❌ {exercise.capitalize()} tracking error: {str(e)}", "error"

# Feedback dictionaries
def get_squat_feedback(state, fallback):
    return {
        "too_shallow": "⬇️ Lower your hips to reach squat depth.",
        "too_low": "⬆️ You're going too low — raise slightly.",
        "mid": "↕️ Almost there. Go slightly deeper.",
        "perfect": "✅ Perfect squat! Hold it.",
        "standing": "🧍 Stand tall. Ready for next rep."
    }.get(state, fallback)

def get_pushup_feedback(state, fallback):
    return {
        "too_shallow": "⬇️ Go lower for a full push-up.",
        "too_low": "⬆️ Too low — raise slightly.",
        "mid": "↕️ Almost there — lower a bit more.",
        "perfect": "✅ Perfect push-up!",
        "up": "📏 Hold the plank position."
    }.get(state, fallback)

def get_plank_feedback(state, fallback):
    return {
        "hips_up": "⬇️ Lower your hips to keep a flat back.",
        "hips_down": "⬆️ Lift your hips to avoid sagging.",
        "perfect": "✅ Perfect plank posture! Keep holding.",
        "start": "📢 Get into plank position — back straight, core tight!",
        "not_visible": "⚠️ Pose not fully visible."
    }.get(state, fallback)
