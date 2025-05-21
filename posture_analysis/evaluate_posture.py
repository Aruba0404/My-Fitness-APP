import streamlit as st
from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from utils.plank_timer import PlankAnalyzer

# Initialize posture analyzers in Streamlit session state
if "squat_tracker" not in st.session_state:
    st.session_state.squat_tracker = SquatAnalyzer()

if "pushup_tracker" not in st.session_state:
    st.session_state.pushup_tracker = PushupAnalyzer()

if "plank_tracker" not in st.session_state:
    st.session_state.plank_tracker = PlankAnalyzer()

def evaluate_posture(landmarks, width, height, exercise):
    """
    Analyze posture based on selected exercise and return:
    - (correct_reps, incorrect_reps, feedback_text, posture_state)
    """
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


# Feedback helpers per exercise
def get_squat_feedback(state, fallback):
    return {
        "too_shallow": "⬇️ Lower your hips to reach proper squat depth.",
        "too_low": "🛑 Too deep — rise up slightly.",
        "mid": "↕️ You're close! Just a bit lower.",
        "perfect": "✅ Great squat! Keep it up.",
        "standing": "🧍 Stand tall. Get ready for the next rep!"
    }.get(state, fallback)

def get_pushup_feedback(state, fallback):
    return {
        "too_shallow": "⬇️ Lower your chest closer to the ground.",
        "too_low": "⬆️ You're too low — raise a bit.",
        "mid": "↕️ Almost perfect — go lower slightly.",
        "perfect": "✅ Excellent push-up!",
        "up": "🧍 Hold steady in plank position."
    }.get(state, fallback)

def get_plank_feedback(state, fallback):
    return {
        "hips_up": "⬇️ Lower your hips — keep back flat.",
        "hips_down": "⬆️ Lift your hips to avoid sagging.",
        "perfect": "✅ Perfect posture! Keep holding.",
        "start": "🎯 Get into plank position — back straight, core tight.",
        "not_visible": "⚠️ Pose not fully visible. Please adjust."
    }.get(state, fallback)
