import cv2
import math
from typing import List, Optional
import mediapipe as mp
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# ---------- ANGLE UTILS ----------
def _calc_2d_angle(a: NormalizedLandmark, b: NormalizedLandmark, c: NormalizedLandmark) -> float:
    ax, ay = a.x - b.x, a.y - b.y
    cx, cy = c.x - b.x, c.y - b.y
    dot = ax * cx + ay * cy
    mag_ab = math.hypot(ax, ay)
    mag_cb = math.hypot(cx, cy)
    if mag_ab == 0 or mag_cb == 0:
        return 0.0
    cos_angle = dot / (mag_ab * mag_cb)
    cos_angle = max(min(cos_angle, 1.0), -1.0)
    return math.degrees(math.acos(cos_angle))

def _draw_angle(frame, landmarks, p1, p2, p3, label):
    h, w = frame.shape[:2]
    x1, y1 = int(landmarks[p1].x * w), int(landmarks[p1].y * h)
    x2, y2 = int(landmarks[p2].x * w), int(landmarks[p2].y * h)
    x3, y3 = int(landmarks[p3].x * w), int(landmarks[p3].y * h)
    angle = int(_calc_2d_angle(landmarks[p1], landmarks[p2], landmarks[p3]))

    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
    cv2.line(frame, (x2, y2), (x3, y3), (0, 255, 255), 3)
    for (x, y) in [(x1, y1), (x2, y2), (x3, y3)]:
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    cv2.putText(frame, f"{label}: {angle}°", (x2 + 10, y2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# ---------- PUBLIC FUNCTION ----------
def draw_landmarks(frame, landmark_obj, feedback_text=None, rep_count=None, exercise: Optional[str] = None):
    if landmark_obj:
        mp_drawing.draw_landmarks(
            frame,
            landmark_obj,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=4, circle_radius=5),
            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=2)
        )

        # Optional: draw joint labels
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

        # Draw angles depending on exercise
        if exercise:
            ex = exercise.lower()
            if ex == "squats":
                _draw_angle(frame, landmarks, 23, 25, 27, "Left Knee")
                _draw_angle(frame, landmarks, 24, 26, 28, "Right Knee")
            elif ex == "pushups":
                _draw_angle(frame, landmarks, 11, 13, 15, "Left Elbow")
                _draw_angle(frame, landmarks, 12, 14, 16, "Right Elbow")
            elif ex == "plank":
                _draw_angle(frame, landmarks, 11, 23, 25, "Left Hip")
                _draw_angle(frame, landmarks, 12, 24, 26, "Right Hip")

    # 🗣️ Feedback Text
    if feedback_text:
        color = (0, 255, 0)
        if "❌" in feedback_text or "too" in feedback_text.lower():
            color = (0, 0, 255)
        elif "⬇️" in feedback_text:
            color = (0, 255, 255)
        cv2.putText(frame, feedback_text, (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3, cv2.LINE_AA)

    # 🔢 Rep Count
    if rep_count is not None and rep_count != "-":
        cv2.putText(frame, f"Reps: {rep_count}", (10, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)

    return frame
