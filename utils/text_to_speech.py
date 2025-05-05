import pyttsx3
import streamlit as st
import threading
import time
import random

# Initialize shared session state
if "last_voice_time" not in st.session_state:
    st.session_state.last_voice_time = 0
if "intro_spoken" not in st.session_state:
    st.session_state.intro_spoken = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    engine.say(text)
    engine.runAndWait()

def intro_voice():
    if not st.session_state.intro_spoken:
        welcome = (
            "Welcome to your AI Fitness Trainer. "
            "Stand in front of the camera to begin squats with real-time feedback."
        )
        threading.Thread(target=speak, args=(welcome,)).start()
        st.session_state.intro_spoken = True

def is_valid_pose(landmarks):
    required = [23, 25, 27]  # hip, knee, ankle
    return all(idx < len(landmarks) and landmarks[idx].visibility > 0.6 for idx in required)

def audio_feedback(text, landmarks=None):
    now = time.time()

    # Cooldown: 2 seconds
    if now - st.session_state.last_voice_time < 2:
        return

    # Skip if same feedback or boring
    if text == st.session_state.last_feedback:
        return

    # Don't speak if only face is detected
    if landmarks and not is_valid_pose(landmarks):
        return

    # Short, clean coaching phrases
    phrase_map = {
        "perfect": ["Perfect squat.", "You got it!", "Great form!", "Nice rep!"],
        "too_shallow": ["Go lower.", "Lower your hips."],
        "too_low": ["Not too deep.", "Raise a little."],
        "standing": ["Stand tall.", "Ready for next rep."],
        "mid": ["Almost there.", "Almost at squat depth."],
    }

    spoken = None

    for key in phrase_map:
        if key in text.lower():
            spoken = random.choice(phrase_map[key])
            break

    if not spoken:
        spoken = text

    threading.Thread(target=speak, args=(spoken,)).start()
    st.session_state.last_feedback = text
    st.session_state.last_voice_time = now
