import streamlit as st
import cv2
import os
from pose_estimation.detect_pose import get_pose_model, detect_pose
from pose_estimation.draw_landmarks import draw_landmarks, visualize_angles
from posture_analysis.evaluate_posture import evaluate_posture
from utils.text_to_speech import audio_feedback, intro_voice

# ---- PAGE CONFIG ----
st.set_page_config(page_title="🏋️ AI Fitness Trainer", layout="wide")

# ---- SESSION STATE INIT ----
if "intro_spoken" not in st.session_state:
    st.session_state.intro_spoken = False

# ---- SIDEBAR NAVIGATION ----
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

# ---- LIVE MODE ----
elif page == "Live Mode":
    st.header("📹 Live Mode: Real-Time Feedback")
    exercise = st.selectbox("🏋️ Select Exercise:", ["Squats", "Pushups", "Planks"], key="live_exercise")
    enable_audio = st.checkbox("🔊 Enable Voice Feedback", value=True)
    start_button = st.button("▶️ Start Live Session")

    if start_button:
        pose_model = get_pose_model()
        if enable_audio and not st.session_state.intro_spoken:
            intro_voice()
            st.session_state.intro_spoken = True

        cap = cv2.VideoCapture(0)
        FRAME_WINDOW = st.empty()
        stop_signal = False

        stop_btn_placeholder = st.empty()
        if stop_btn_placeholder.button("⛔ Stop"):
            stop_signal = True

        while cap.isOpened() and not stop_signal:
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Failed to access webcam.")
                break

            landmarks, results = detect_pose(frame, pose_model)
            feedback, rep_count = "Waiting for pose...", 0

            if landmarks:
                correct, incorrect, feedback, posture = evaluate_posture(
                    landmarks, frame.shape[1], frame.shape[0], exercise
                )
                rep_count = correct
                frame = visualize_angles(frame, landmarks, exercise)
                frame = draw_landmarks(results.pose_landmarks, frame)

                if enable_audio:
                    audio_feedback(feedback, posture, landmarks)
            else:
                cv2.putText(frame, "⚠️ Pose not detected", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Overlay feedback and rep count
            cv2.rectangle(frame, (0, frame.shape[0] - 40), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
            cv2.putText(frame, feedback, (50, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.rectangle(frame, (10, frame.shape[0] - 90), (160, frame.shape[0] - 50), (0, 100, 0), -1)
            cv2.putText(frame, f"Reps: {rep_count}", (20, frame.shape[0] - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)

            if stop_btn_placeholder.button("⛔ Stop"):
                break

        cap.release()
        st.success("✅ Session Ended.")

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

        cap = cv2.VideoCapture(temp_path)
        FRAME_WINDOW = st.empty()
        pose_model = get_pose_model()

        if enable_audio and not st.session_state.intro_spoken:
            intro_voice()
            st.session_state.intro_spoken = True

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            landmarks, results = detect_pose(frame, pose_model)
            feedback, rep_count = "Analyzing...", 0

            if landmarks:
                correct, incorrect, feedback, posture = evaluate_posture(
                    landmarks, frame.shape[1], frame.shape[0], exercise
                )
                rep_count = correct
                frame = visualize_angles(frame, landmarks, exercise)
                frame = draw_landmarks(results.pose_landmarks, frame)

                if enable_audio:
                    audio_feedback(feedback, posture, landmarks)
            else:
                cv2.putText(frame, "⚠️ Pose not detected", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.rectangle(frame, (0, frame.shape[0] - 40), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
            cv2.putText(frame, feedback, (50, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.rectangle(frame, (10, frame.shape[0] - 90), (160, frame.shape[0] - 50), (0, 100, 0), -1)
            cv2.putText(frame, f"Reps: {rep_count}", (20, frame.shape[0] - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)

        cap.release()
        os.remove(temp_path)

# ---- FOOTER ----
st.markdown("---")
st.caption("🚀 Made with ❤️ and ☕ by Aruba & Zainab")
