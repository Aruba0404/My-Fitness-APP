import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# ------------------ ANGLE CALCULATION ------------------
def calculate_angle(a, b, c):
    try:
        a = [a.x, a.y]
        b = [b.x, b.y]
        c = [c.x, c.y]

        ba = [a[0] - b[0], a[1] - b[1]]
        bc = [c[0] - b[0], c[1] - b[1]]

        dot_product = ba[0]*bc[0] + ba[1]*bc[1]
        mag_ba = math.hypot(ba[0], ba[1])
        mag_bc = math.hypot(bc[0], bc[1])
        if mag_ba == 0 or mag_bc == 0:
            return 0

        angle = math.acos(dot_product / (mag_ba * mag_bc))
        return math.degrees(angle)
    except:
        return 0

# ------------------ VISUALIZATION FUNCTIONS ------------------
def draw_angle(frame, landmarks, p1, p2, p3, label):
    h, w = frame.shape[:2]
    try:
        x1, y1 = int(landmarks[p1].x * w), int(landmarks[p1].y * h)
        x2, y2 = int(landmarks[p2].x * w), int(landmarks[p2].y * h)
        x3, y3 = int(landmarks[p3].x * w), int(landmarks[p3].y * h)

        angle = int(calculate_angle(landmarks[p1], landmarks[p2], landmarks[p3]))

        # Draw lines and points
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
        cv2.line(frame, (x2, y2), (x3, y3), (0, 255, 255), 4)
        cv2.circle(frame, (x1, y1), 6, (0, 0, 255), -1)
        cv2.circle(frame, (x2, y2), 6, (0, 0, 255), -1)
        cv2.circle(frame, (x3, y3), 6, (0, 0, 255), -1)

        # Label angle
        cv2.putText(frame, f"{label}: {angle}°", (x2 + 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    except:
        pass
    return frame


def visualize_angles(frame, landmarks, exercise):
    if exercise.lower() == "squats":
        # Right and Left Knee
        draw_angle(frame, landmarks, 24, 26, 28, "Right Knee")
        draw_angle(frame, landmarks, 23, 25, 27, "Left Knee")
    elif exercise.lower() == "pushups":
        # Right and Left Elbow
        draw_angle(frame, landmarks, 12, 14, 16, "Right Elbow")
        draw_angle(frame, landmarks, 11, 13, 15, "Left Elbow")
    elif exercise.lower() == "planks":
        # Shoulder-hip-knee angles to monitor straight body
        draw_angle(frame, landmarks, 12, 24, 26, "Right Side")
        draw_angle(frame, landmarks, 11, 23, 25, "Left Side")
    return frame

# ------------------ LANDMARK DRAWING ------------------
def draw_landmarks(landmarks, frame, feedback_text=None, rep_count=None):
    if landmarks:
        mp_drawing.draw_landmarks(
            frame,
            landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=4),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=2),
        )

    # Feedback and Reps
    if feedback_text:
        cv2.putText(frame, feedback_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    if rep_count is not None:
        cv2.putText(frame, f"Reps: {rep_count}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame
