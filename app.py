import streamlit as st
import cv2
import time
import tempfile
import mediapipe as mp
from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from logic.timer_utils import PlankTimer
from posture_analysis.evaluate_posture import evaluate_posture
from pose_estimation.draw_landmarks import draw_landmarks
from utils.logger import save_session_log

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

st.set_page_config(page_title="Fitness Feedback App", layout="wide")

EXERCISE_OPTIONS = ["Squat", "Pushup", "Plank"]


def main():
    st.title("🏋️ AI Fitness Feedback System")
    st.sidebar.title("Exercise Selection")
    app_mode = st.sidebar.selectbox("Choose Mode", ["Start Page", "Live Camera", "Upload Video"])

    if app_mode == "Start Page":
        show_start_page()
    elif app_mode == "Live Camera":
        show_live_camera()
    elif app_mode == "Upload Video":
        show_upload_video()


def show_start_page():
    st.markdown("""
    ### 🤖 Real-Time Fitness Feedback App
    This app helps you perform exercises like **Squats**, **Pushups**, and **Planks** with instant feedback using your webcam or uploaded video.

    ✅ Get feedback on your posture  
    🎁 Gamified rep tracking  
    🧪 Accuracy scoring  
    📊 CSV logs for each session

    Made with ❤️ and ☕ using OpenCV and Mediapipe.
    """)


def show_live_camera():
    st.header("📷 Live Camera Mode")
    exercise = st.selectbox("Select Exercise", EXERCISE_OPTIONS)
    start_button = st.button("Start")

    if start_button:
        run_live_feedback(exercise)


def run_live_feedback(exercise):
    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose()
    rep_counter = SquatAnalyzer() if exercise == "Squat" else PushupAnalyzer()
    plank_timer = PlankTimer() if exercise == "Plank" else None

    prev_time = time.time()
    session_data = []

    stframe = st.empty()
    stop = st.button("Stop")

    while cap.isOpened() and not stop:
        ret, frame = cap.read()
        if not ret:
            st.warning("Camera not detected!")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            feedback, rep_count, incorrect_count, accuracy_score = evaluate_posture(
                results.pose_landmarks.landmark,
                exercise,
                analyzer=rep_counter,
                timer=plank_timer
            )

            frame = draw_landmarks(results.pose_landmarks, frame, feedback_text=feedback, rep_count=rep_count)

            session_data.append({
                "exercise": exercise,
                "feedback": feedback,
                "reps": rep_count,
                "incorrect": incorrect_count,
                "accuracy": accuracy_score,
                "timestamp": time.time() - prev_time
            })

        stframe.image(frame, channels="BGR")

    cap.release()
    st.success("Session Ended")
    save_session_log(session_data)


def show_upload_video():
    st.header("🎞️ Upload Mode")
    exercise = st.selectbox("Choose Exercise", EXERCISE_OPTIONS)
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
        pose = mp_pose.Pose()
        rep_counter = SquatAnalyzer() if exercise == "Squat" else PushupAnalyzer()
        plank_timer = PlankTimer() if exercise == "Plank" else None

        stframe = st.empty()
        session_data = []
        prev_time = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:
                feedback, rep_count, incorrect_count, accuracy_score = evaluate_posture(
                    results.pose_landmarks.landmark,
                    exercise,
                    analyzer=rep_counter,
                    timer=plank_timer
                )

                frame = draw_landmarks(results.pose_landmarks, frame, feedback_text=feedback, rep_count=rep_count)

                session_data.append({
                    "exercise": exercise,
                    "feedback": feedback,
                    "reps": rep_count,
                    "incorrect": incorrect_count,
                    "accuracy": accuracy_score,
                    "timestamp": time.time() - prev_time
                })

            stframe.image(frame, channels="BGR")

        cap.release()
        st.success("Video analysis complete!")
        save_session_log(session_data)


if __name__ == "__main__":
    main()
