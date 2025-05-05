import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def draw_landmarks(landmark_obj, frame, feedback_text=None, rep_count=None):
    """
    Draws pose landmarks, joint labels, feedback text, and rep counter on the frame.
    """
    if landmark_obj:
        # 🦴 Draw skeleton
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=landmark_obj,
            connections=mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=4, circle_radius=5),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=2)
        )

        # 🏷️ Label important joints
        h, w = frame.shape[:2]
        landmarks = landmark_obj.landmark
        point_map = {
            "Shoulder": 11,
            "Hip": 23,
            "Knee": 25,
            "Ankle": 27
        }

        for label, idx in point_map.items():
            cx, cy = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
            cv2.putText(frame, label, (cx + 5, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 🗣️ Show feedback message
    if feedback_text:
        color = (0, 255, 0)  # ✅ green
        if "❌" in feedback_text or "too" in feedback_text.lower():
            color = (0, 0, 255)  # ❌ red
        elif "⬇️" in feedback_text or "down" in feedback_text.lower():
            color = (0, 255, 255)  # ⚠️ yellow

        cv2.putText(frame, feedback_text, (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3, cv2.LINE_AA)

    # 🔢 Display rep count
    if rep_count is not None and rep_count != "-":
        cv2.putText(frame, f"Reps: {rep_count}", (10, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)

    return frame
