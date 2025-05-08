import streamlit as st
import cv2
import tempfile
import mediapipe as mp
from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from utils.timer_utils import PlankTimer
from posture_analysis.evaluate_posture import evaluate_posture
from pose_estimation.draw_landmarks import draw_landmarks
from utils.text_to_speech import audio_feedback  # Ensure you import audio_feedback

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Set the Streamlit page configuration
st.set_page_config(page_title="Fitness Feedback App", layout="wide")

EXERCISE_OPTIONS = ["Squat", "Pushup", "Plank"]

# Initialize analyzers once using session state
if "squat_tracker" not in st.session_state:
    st.session_state.squat_tracker = SquatAnalyzer()

if "pushup_tracker" not in st.session_state:
    st.session_state.pushup_tracker = PushupAnalyzer()

if "plank_timer" not in st.session_state:
    st.session_state.plank_timer = PlankTimer()

def main():
    st.title("🏋️ AI Fitness Feedback System")
    st.sidebar.title("Exercise Selection")
    app_mode = st.sidebar.radio("Navigation", ["Start Page", "Live Camera", "Upload Video"])

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

    # Map UI exercise name to expected lowercase keys
    exercise_map = {
        "Squat": "squats",
        "Pushup": "pushups",
        "Plank": "planks"
    }
    exercise_key = exercise_map.get(exercise.lower().capitalize(), "unknown")

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
            if exercise_key == "planks":
                duration, _, feedback = evaluate_posture(
                    results.pose_landmarks.landmark, frame.shape[1], frame.shape[0], exercise_key
                )
                rep_count = "-"
            else:
                correct, incorrect, feedback = evaluate_posture(
                    results.pose_landmarks.landmark, frame.shape[1], frame.shape[0], exercise_key
                )
                rep_count = correct

            audio_feedback(feedback)
            frame = draw_landmarks(results.pose_landmarks, frame, feedback_text=feedback, rep_count=rep_count)

        stframe.image(frame, channels="BGR")

    cap.release()
    st.success("Session Ended")

def show_upload_video():
    st.header("🎞️ Upload Mode")
    exercise = st.selectbox("Choose Exercise", EXERCISE_OPTIONS)
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        exercise_map = {
            "Squat": "squats",
            "Pushup": "pushups",
            "Plank": "planks"
        }
        exercise_key = exercise_map.get(exercise.lower().capitalize(), "unknown")

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
        pose = mp_pose.Pose()

        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:
                if exercise_key == "planks":
                    duration, _, feedback = evaluate_posture(
                        results.pose_landmarks.landmark, frame.shape[1], frame.shape[0], exercise_key
                    )
                    rep_count = "-"
                else:
                    correct, incorrect, feedback = evaluate_posture(
                        results.pose_landmarks.landmark, frame.shape[1], frame.shape[0], exercise_key
                    )
                    rep_count = correct

                audio_feedback(feedback)
                frame = draw_landmarks(results.pose_landmarks, frame, feedback_text=feedback, rep_count=rep_count)

            stframe.image(frame, channels="BGR")

        cap.release()
        st.success("Video analysis complete!")

if __name__ == "__main__":
    main()
