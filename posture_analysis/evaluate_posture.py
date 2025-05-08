import streamlit as st
from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from utils.timer_utils import PlankAnalyzer

# 🧠 Initialize analyzers in session state only once
if "squat_tracker" not in st.session_state:
    st.session_state.squat_tracker = SquatAnalyzer()

if "pushup_tracker" not in st.session_state:
    st.session_state.pushup_tracker = PushupAnalyzer()

if "plank_tracker" not in st.session_state:
    st.session_state.plank_tracker = PlankAnalyzer()

def evaluate_posture(landmarks, width, height, exercise):
    """
    Evaluates the current posture based on the exercise type.
    Returns (correct_count, incorrect_count, feedback_text) for squats and push-ups,
    or (duration, '-', feedback_text) for planks.
    """
    if not landmarks or len(landmarks) < 33:
        return 0, 0, "⚠️ Pose not fully visible."

    exercise = exercise.strip().lower()

    # 🏋️ SQUATS
    if exercise == "squats":
        try:
            correct, incorrect, raw_feedback, state = st.session_state.squat_tracker.update(landmarks, width, height)
            feedback = get_squat_feedback(state, raw_feedback)
        except Exception as e:
            return 0, 0, f"❌ Squat tracking error: {str(e)}"
        return correct, incorrect, feedback

    # 🤸 PUSH-UPS
    elif exercise == "pushups":
        try:
            correct, incorrect, raw_feedback, state = st.session_state.pushup_tracker.update(landmarks, width, height)
            feedback = get_pushup_feedback(state, raw_feedback)
        except Exception as e:
            return 0, 0, f"❌ Push-up tracking error: {str(e)}"
        return correct, incorrect, feedback

    # 🪵 PLANKS
    elif exercise == "planks":
        try:
            duration, state, raw_feedback = st.session_state.plank_tracker.update(landmarks)
            feedback = get_plank_feedback(state, raw_feedback)
        except Exception as e:
            return 0, 0, f"❌ Plank tracking error: {str(e)}"
        return duration, "-", feedback

    return 0, 0, "⚠️ Unknown exercise selected."

# 🎯 Squat Feedback
def get_squat_feedback(state, fallback):
    feedback_dict = {
        "too_shallow": "⬇️ Lower your hips to reach squat depth.",
        "too_low": "⬆️ You're going too low — raise slightly.",
        "mid": "↕️ Almost there. Go slightly deeper.",
        "perfect": "✅ Perfect squat! Hold it.",
        "standing": "🧍 Stand tall. Ready for next rep."
    }
    return feedback_dict.get(state, fallback)

# 💪 Push-up Feedback
def get_pushup_feedback(state, fallback):
    feedback_dict = {
        "too_shallow": "⬇️ Go lower for a full push-up.",
        "too_low": "⬆️ Too low — raise slightly.",
        "mid": "↕️ Almost there — lower a bit more.",
        "perfect": "✅ Perfect push-up!",
        "up": "📏 Hold the plank position."
    }
    return feedback_dict.get(state, fallback)

# 🪵 Plank Feedback
def get_plank_feedback(state, fallback):
    feedback_dict = {
        "hips_up": "⬇️ Lower your hips to keep a flat back.",
        "hips_down": "⬆️ Lift your hips to avoid sagging.",
        "perfect": "✅ Perfect plank posture! Keep holding.",
        "start": "📢 Get into plank position — back straight, core tight!"
    }
    return feedback_dict.get(state, fallback)
