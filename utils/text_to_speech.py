import pyttsx3
import streamlit as st
import threading
import time
import random

# -----------------------------
# 🔁 Session State Initialization
# -----------------------------
if "last_voice_time" not in st.session_state:
    st.session_state.last_voice_time = 0
if "intro_spoken" not in st.session_state:
    st.session_state.intro_spoken = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

# -----------------------------
# 🎙️ TTS Engine Initialization
# -----------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)  # Max volume

# -----------------------------
# 🗣️ Speak Function
# -----------------------------
def speak(text):
    """
    Speaks the given text using pyttsx3 in a separate thread.
    """
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# 🎉 Introductory Welcome Voice
# -----------------------------
def intro_voice():
    """
    Plays a welcome message once per session.
    """
    if not st.session_state.intro_spoken:
        welcome = (
            "Welcome to your AI Fitness Trainer. "
            "Stand in front of the camera to begin squats with real-time feedback."
        )
        threading.Thread(target=speak, args=(welcome,)).start()
        st.session_state.intro_spoken = True

# -----------------------------
# ✅ Pose Detection Check
# -----------------------------
def is_valid_pose(landmarks):
    """
    Returns True if required body landmarks (hip, knee, ankle) are visible.
    """
    required = [23, 25, 27]  # hip, knee, ankle
    return all(
        idx < len(landmarks) and landmarks[idx].visibility > 0.6
        for idx in required
    )

# -----------------------------
# 🎧 Context-Aware Feedback
# -----------------------------
def audio_feedback(text, landmarks=None):
    """
    Provide audio feedback based on the evaluation result.
    """
    now = time.time()

    # Cooldown: prevent speaking too frequently (2 seconds cooldown)
    if now - st.session_state.last_voice_time < 2:
        return

    # Skip speaking if feedback is the same as the previous
    if text == st.session_state.last_feedback:
        return

    # Don't speak if only face is detected or pose is invalid
    if landmarks and not is_valid_pose(landmarks):
        return

    # Mapping coaching phrases based on feedback text
    phrase_map = {
        "perfect": ["Perfect squat!", "You got it!", "Great form!", "Nice rep!"],
        "too_shallow": ["Go lower.", "Lower your hips."],
        "too_low": ["Not too deep.", "Raise a little."],
        "standing": ["Stand tall.", "Ready for next rep."],
        "mid": ["Almost there.", "Almost at squat depth."],
    }

    spoken = None

    # Select appropriate spoken feedback from phrase_map
    for key in phrase_map:
        if key in text.lower():
            spoken = random.choice(phrase_map[key])
            break

    # Fallback to the original text if no specific phrase is found
    if not spoken:
        spoken = text

    # Speak the feedback in a separate thread to avoid blocking
    threading.Thread(target=speak, args=(spoken,)).start()

    # Update session state to prevent repeating the same feedback
    st.session_state.last_feedback = text
    st.session_state.last_voice_time = now
