import streamlit as st
import cv2
import os
import time
from pose_estimation.detect_pose import get_pose_model, detect_pose
from pose_estimation.draw_landmarks import draw_landmarks
from posture_analysis.evaluate_posture import evaluate_posture
from utils.text_to_speech import audio_feedback, intro_voice
from utils.timer_utils import PlankAnalyzer

# ---- PAGE CONFIG ----
st.set_page_config(page_title="🏋️ AI Fitness Trainer", layout="wide")

# ---- SESSION STATE ----
if "intro_spoken" not in st.session_state:
    st.session_state.intro_spoken = False
if "rep_count" not in st.session_state:
    st.session_state.rep_count = 0
if "plank_timer" not in st.session_state:
    st.session_state.plank_timer = PlankAnalyzer()

# ---- SIDEBAR ----
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/128/3344/3344147.png", width=100)
    st.title("Fitness AI Trainer")
    st.markdown("---")
    page = st.radio("📌 Navigate", ["Home", "Live Mode", "Upload Mode"])

# ---- HOME PAGE ----
if page == "Home":
    st.markdown("""
        <h1 style='color: yellow;'>👋 Welcome to the AI Fitness Trainer App</h1>
        <p>This app gives you real-time feedback for <b>Squats</b>, <b>Push-ups</b>, and <b>Planks</b>.</p>
        <ul>
            <li>📹 <b>Live Mode:</b> Use your webcam for real-time form correction</li>
            <li>📁 <b>Upload Mode:</b> Analyze your recorded workout video</li>
            <li>🎯 <b>Posture Feedback, Rep Counting, and Angle Visualizations</b></li>
        </ul>
        <h4>✅ Pro Tips:</h4>
        <ul>
            <li>Keep your full body visible to the camera</li>
            <li>Use good lighting and avoid cluttered backgrounds</li>
            <li>Follow on-screen feedback to correct your form</li>
        </ul>
    """, unsafe_allow_html=True)

# ---- COMMON FRAME PROCESSING FUNCTION ----
def process_frame(frame, exercise, pose_model, enable_audio, is_live=True):
    landmarks, results = detect_pose(frame, pose_model)

    if landmarks:
        if exercise == "Planks":
            duration, posture, feedback = st.session_state.plank_timer.update(
                landmarks, frame.shape[1], frame.shape[0]
            )
            if enable_audio:
                audio_feedback(feedback, posture)
            return draw_landmarks(
                frame,
                results.pose_landmarks,
                rep_count=None,
                feedback_text=f"{feedback} | ⏱️ {int(duration)} sec",
                posture_status=posture
            )
        else:
            correct, incorrect, feedback, posture = evaluate_posture(
                landmarks, frame.shape[1], frame.shape[0], exercise
            )
            st.session_state.rep_count = correct
            if enable_audio:
                audio_feedback(feedback, posture)
            return draw_landmarks(
                frame,
                results.pose_landmarks,
                rep_count=correct,
                feedback_text=feedback,
                posture_status=posture
            )
    else:
        return draw_landmarks(
            frame,
            None,
            rep_count=st.session_state.rep_count,
            feedback_text="⚠️ Pose not detected",
            posture_status="error"
        )

# ---- LIVE MODE ----
if page == "Live Mode":
    st.header("📹 Live Mode: Real-Time Feedback")
    exercise = st.selectbox("🏋️ Select Exercise:", ["Squats", "Pushups", "Planks"], key="live_exercise")
    enable_audio = st.checkbox("🔊 Enable Voice Feedback", value=True)
    start_button = st.button("▶️ Start Live Session")

    if start_button:
        st.session_state.rep_count = 0
        st.session_state.plank_timer = PlankAnalyzer()
        pose_model = get_pose_model()

        if enable_audio and not st.session_state.intro_spoken:
            intro_voice()
            st.session_state.intro_spoken = True

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("❌ Webcam not accessible. Please check your camera.")
        else:
            FRAME_WINDOW = st.empty()
            stop_button = st.button("⛔ Stop Live Session")
            stop_signal = False

            while cap.isOpened() and not stop_signal:
                ret, frame = cap.read()
                if not ret:
                    st.error("❌ Failed to read from webcam.")
                    break

                processed_frame = process_frame(frame, exercise, pose_model, enable_audio)
                rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(rgb_frame)

                if stop_button:
                    stop_signal = True
                time.sleep(0.06)

            cap.release()
            st.success("✅ Session Ended.")
            st.session_state.intro_spoken = False

# ---- UPLOAD MODE ----
elif page == "Upload Mode":
    st.header("📁 Upload Video for Feedback")
    exercise = st.selectbox("🏋️ Select Exercise:", ["Squats", "Pushups", "Planks"], key="upload_exercise")
    enable_audio = st.checkbox("🔊 Enable Voice Feedback", value=True)
    uploaded_video = st.file_uploader("📤 Upload a video", type=["mp4", "mov", "avi"])

    if uploaded_video:
        st.video(uploaded_video)

        temp_path = f"temp_{uploaded_video.name}"
        with open(temp_path, 'wb') as f:
            f.write(uploaded_video.read())

        pose_model = get_pose_model()
        FRAME_WINDOW = st.empty()
        st.session_state.plank_timer = PlankAnalyzer()

        if enable_audio and not st.session_state.intro_spoken:
            intro_voice()
            st.session_state.intro_spoken = True

        cap = cv2.VideoCapture(temp_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_frame(frame, exercise, pose_model, enable_audio, is_live=False)
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(rgb_frame)
            time.sleep(0.06)

        cap.release()
        os.remove(temp_path)
        st.success("✅ Video analysis complete.")
        st.session_state.intro_spoken = False

# ---- FOOTER ----
st.markdown("---")
st.caption("🚀 Made with ❤️ and ☕ by Aruba & Zainab")
