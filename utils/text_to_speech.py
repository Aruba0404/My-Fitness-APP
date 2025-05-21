import pyttsx3
import streamlit as st
import time
import threading
import random

# --- Session State Initialization ---
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

# --- Global Engine Setup ---
engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)

# --- Threaded Speech Function ---
def speak(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except RuntimeError:
            pass  # Avoid runtime conflict if engine already running
    threading.Thread(target=run).start()

# --- One-time Intro Voice ---
def intro_voice():
    if not st.session_state.intro_spoken:
        intro = (
            "👋 Welcome to your AI Fitness Trainer! "
            "Get ready to improve your squats, push-ups, and planks with real-time feedback. "
            "Align yourself in front of the camera and let’s begin!"
        )
        speak(intro)
        st.session_state.intro_spoken = True

# --- Smart Audio Feedback ---
def audio_feedback(feedback_text, posture_state=None):
    now = time.time()

    # Cooldown: 2.5 seconds
    if now - st.session_state.last_voice_time < 2.5:
        return

    # Prevent repetition if same feedback + posture
    if (
        feedback_text == st.session_state.last_feedback and
        posture_state == st.session_state.last_posture
    ):
        return

    # --- Friendly feedback phrases ---
    positive_responses = [
        "Nice one!", "Perfect squat!", "Hold that!", "Great job!", "Keep it steady!"
    ]
    correction_responses = [
        "Straighten your back.", "Lower your hips a bit.", "Don't go too low.",
        "Keep your knees behind your toes.", "Try again!"
    ]

    # Choose voice response based on feedback type
    feedback_text_lower = feedback_text.lower()
    if "perfect" in feedback_text_lower or "✅" in feedback_text:
        spoken = random.choice(positive_responses)
    elif "❌" in feedback_text or any(word in feedback_text_lower for word in ["back", "hip", "knee", "low"]):
        spoken = random.choice(correction_responses)
    else:
        spoken = feedback_text

    # Speak it!
    speak(spoken)

    # Update state
    st.session_state.last_voice_time = now
    st.session_state.last_feedback = feedback_text
    st.session_state.last_posture = posture_state or ""
