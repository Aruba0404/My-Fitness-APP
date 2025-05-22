import cv2
import math
from typing import Optional
import mediapipe as mp
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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

    # Draw lines and points
    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
    cv2.line(frame, (x2, y2), (x3, y3), (0, 255, 255), 3)
    for (x, y) in [(x1, y1), (x2, y2), (x3, y3)]:
        cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)

    # Draw angle label
    cv2.putText(frame, f"{label}: {angle}°", (x2 + 10, y2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def draw_landmarks(
    frame,
    landmark_obj,
    feedback_text: Optional[str] = None,
    rep_count: Optional[int] = None,
    incorrect_reps: Optional[int] = None,
    exercise: Optional[str] = None,
    posture_status: Optional[str] = None,
    duration: Optional[float] = None
):
    h, w = frame.shape[:2]

    # Draw landmarks
    if landmark_obj:
        mp_drawing.draw_landmarks(
            frame,
            landmark_obj,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=5),
            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
        )

        landmarks = landmark_obj.landmark
        if exercise == "Squats":
            _draw_angle(frame, landmarks, 24, 26, 28, "Knee")
            _draw_angle(frame, landmarks, 12, 24, 26, "Hip")
        elif exercise == "Pushups":
            _draw_angle(frame, landmarks, 12, 14, 16, "Elbow")
            _draw_angle(frame, landmarks, 24, 12, 14, "Shoulder")
        elif exercise == "Planks":
            _draw_angle(frame, landmarks, 12, 14, 16, "Elbow")
            _draw_angle(frame, landmarks, 24, 12, 14, "Shoulder")
            _draw_angle(frame, landmarks, 12, 24, 26, "Hip")

    # Feedback text (bottom center in black bar)
    if feedback_text:
        bar_height = 60
        cv2.rectangle(frame, (0, h - bar_height), (w, h), (0, 0, 0), -1)
        text_size = cv2.getTextSize(feedback_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = (w - text_size[0]) // 2
        text_y = h - 20
        cv2.putText(frame, feedback_text, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Rep count (bottom-left with margin)
    if rep_count is not None:
        box_text = f"Reps: {rep_count}"
        font_scale = 0.8
        text_size = cv2.getTextSize(box_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        box_w, box_h = text_size[0] + 20, text_size[1] + 20
        box_x, box_y = 20, h - 80 - 40  # Added 40px margin
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 100, 0), -1)
        cv2.putText(frame, box_text, (box_x + 10, box_y + box_h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)

    # Incorrect reps (bottom-right)
    if incorrect_reps is not None:
        box_text = f"Incorrect: {incorrect_reps}"
        font_scale = 0.8
        text_size = cv2.getTextSize(box_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        box_w, box_h = text_size[0] + 20, text_size[1] + 20
        box_x, box_y = w - box_w - 20, h - 80
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 0, 150), -1)
        cv2.putText(frame, box_text, (box_x + 10, box_y + box_h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)

    # Plank timer (top-right)
    if duration is not None:
        time_text = f"Time: {duration:.1f}s"
        font_scale = 0.8
        text_size = cv2.getTextSize(time_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        box_w, box_h = text_size[0] + 20, text_size[1] + 20
        box_x, box_y = w - box_w - 20, 20
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_w, box_y + box_h), (40, 40, 200), -1)
        cv2.putText(frame, time_text, (box_x + 10, box_y + box_h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)

    return frame
