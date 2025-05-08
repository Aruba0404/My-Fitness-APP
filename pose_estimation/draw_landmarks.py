import cv2
import mediapipe as mp
from logic.angle_utils import calculate_angle  # You must have this function

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def get_feedback_color(text):
    if "❌" in text or "too" in text.lower():
        return (0, 0, 255)
    elif "⬇️" in text:
        return (0, 255, 255)
    return (0, 255, 0)

def draw_landmarks(landmark_obj, frame, feedback_text=None, rep_count=None, show_labels=True):
    if not landmark_obj or not hasattr(landmark_obj, 'landmark'):
        return frame

    mp_drawing.draw_landmarks(
        image=frame,
        landmark_list=landmark_obj,
        connections=mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=4),
        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
    )

    h, w = frame.shape[:2]
    lm = landmark_obj.landmark

    def get_point(idx):
        return int(lm[idx].x * w), int(lm[idx].y * h)

    def draw_angle(a, b, c, label):
        angle = int(calculate_angle(lm[a], lm[b], lm[c]) or 0)
        px, py = get_point(b)
        cv2.putText(frame, f"{label}: {angle}°", (px + 10, py - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show angles for: knee, hip, and elbow (both sides)
    try:
        draw_angle(23, 25, 27, "LKnee")   # Left Knee
        draw_angle(11, 23, 25, "LHip")    # Left Hip
        draw_angle(13, 11, 23, "LTrunk")  # Left Trunk
        draw_angle(11, 13, 15, "LElbow")  # Left Elbow
        draw_angle(24, 26, 28, "RKnee")   # Right Knee
        draw_angle(12, 24, 26, "RHip")    # Right Hip
        draw_angle(14, 12, 24, "RTrunk")  # Right Trunk
        draw_angle(12, 14, 16, "RElbow")  # Right Elbow
    except:
        pass  # Avoid crash if landmark is missing

    # Feedback text
    if feedback_text:
        color = get_feedback_color(feedback_text)
        y_pos = frame.shape[0] - 20
        cv2.putText(frame, feedback_text, (10, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3, cv2.LINE_AA)

    # Rep count
    if rep_count is not None and rep_count != "-":
        cv2.putText(frame, f"Reps: {rep_count}", (10, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)

    return frame
