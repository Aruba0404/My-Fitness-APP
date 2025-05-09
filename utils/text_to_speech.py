import pyttsx3
import streamlit as st
import time
import threading

# Initialize session state for voice
def init_voice_states():
    if "intro_spoken" not in st.session_state:
        st.session_state.intro_spoken = False
    if "last_voice_time" not in st.session_state:
        st.session_state.last_voice_time = 0
    if "last_feedback" not in st.session_state:
        st.session_state.last_feedback = ""
    if "last_posture" not in st.session_state:
        st.session_state.last_posture = ""

init_voice_states()

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # You can adjust the speaking speed
engine.setProperty('volume', 1.0)  # Volume level

# Function to speak text
def speak(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except RuntimeError:
            pass  # Engine is already running

    threading.Thread(target=run).start()

# Intro voice that plays once
def intro_voice():
    if not st.session_state.intro_spoken:
        speak("Welcome to your AI Fitness Trainer.")
        st.session_state.intro_spoken = True

# Audio feedback function with frequency control and posture state check
def audio_feedback(feedback_text, posture_state, landmarks=None):
    now = time.time()

    # Avoid feedback being too frequent (adjust the cooldown period)
    if now - st.session_state.last_voice_time < 3:
        return

    # Avoid repeating the same feedback if posture hasn't changed
    if (
        feedback_text == st.session_state.last_feedback and
        posture_state == st.session_state.last_posture
    ):
        return

    # Speak the feedback
    speak(feedback_text)

    # Update session state for feedback and posture
    st.session_state.last_voice_time = now
    st.session_state.last_feedback = feedback_text
    st.session_state.last_posture = posture_state
