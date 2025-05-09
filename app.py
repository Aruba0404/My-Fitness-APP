import streamlit as st
import cv2
from pose_estimation.detect_pose import get_pose_model, detect_pose
from pose_estimation.draw_landmarks import draw_landmarks, visualize_angles
from posture_analysis.evaluate_posture import evaluate_posture
from utils.text_to_speech import audio_feedback, intro_voice

# Page Config
st.set_page_config(page_title="🏋️ Real-Time Exercise Feedback", layout="wide")

# Session state setup
if "intro_spoken" not in st.session_state:
    st.session_state.intro_spoken = False

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913466.png", width=100)
    st.title("Fitness AI Trainer")
    st.markdown("---")
    page = st.radio("📌 Navigate", ["Home", "Live Mode", "Upload Mode"])

# --- HOME PAGE ---
if page == "Home":
    st.markdown("""
        <h2>👋 Welcome to the AI Fitness Trainer App</h2>
        <p>This app gives you real-time feedback for <b>Squats</b>, <b>Push-ups</b>, and <b>Planks</b>.</p>
        <div style='padding:10px;border-radius:10px;'>
            <ul>
                <li>📹 <b>Live Mode:</b> Use your webcam for real-time form correction</li>
                <li>📁 <b>Upload Mode:</b> Analyze your recorded workout video</li>
                <li>🎯 <b>Posture Feedback, Rep Counting, and Angle Visualizations</b></li>
            </ul>
        </div>
        <h4>✅ Pro Tips:</h4>
        <ul>
            <li>Keep your full body visible to the camera</li>
            <li>Use good lighting and avoid cluttered backgrounds</li>
            <li>Follow on-screen feedback to correct your form</li>
        </ul>
    """, unsafe_allow_html=True)

# --- LIVE MODE ---
elif page == "Live Mode":
    st.header("📹 Live Mode: Real-Time Exercise Feedback")
    exercise = st.selectbox("🏋️ Select Exercise:", ["Squats", "Pushups", "Planks"], key="live_exercise")
    start_button = st.button("▶️ Start Live Session")
    FRAME_WINDOW = st.image([])

    if start_button:
        cap = cv2.VideoCapture(0)
        pose_model = get_pose_model()
        intro_voice()  # 🔊 Welcome voice
        st.info("📸 Camera started. Click the Stop button to end the session.")
        stop_button = st.button("⛔ Stop")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Failed to capture frame.")
                break

            landmarks, results = detect_pose(frame, pose_model)
            if landmarks:
                correct, incorrect, feedback, posture = evaluate_posture(
                    landmarks, frame.shape[1], frame.shape[0], exercise
                )

                frame = visualize_angles(frame, landmarks, exercise)
                frame = draw_landmarks(results.pose_landmarks, frame, feedback_text=feedback, rep_count=correct)

                # 🔊 Smart Voice Feedback
                audio_feedback(feedback, posture, landmarks)

            else:
                cv2.putText(frame, "⚠️ Unable to detect pose.", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)

            if stop_button:
                break

        cap.release()
        st.success("✅ Session Ended.")

# --- UPLOAD MODE ---
elif page == "Upload Mode":
    st.header("📁 Upload Exercise Video")
    exercise = st.selectbox("🏋️ Select Exercise:", ["Squats", "Pushups", "Planks"], key="upload_exercise")
    uploaded_video = st.file_uploader("📤 Upload a video file", type=["mp4", "mov", "avi"])

    if uploaded_video is not None:
        st.video(uploaded_video)
        st.warning("🚧 Video analysis coming soon!")

# --- FOOTER ---
st.markdown("---")
st.caption("🚀 Made with ❤️ and ☕ by Aruba & Zainab")
