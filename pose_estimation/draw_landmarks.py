import cv2
import numpy as np
from collections import deque

# 🎨 Colors for feedback
COLORS = {
    "perfect": (0, 255, 0),      # Green
    "mid": (0, 255, 255),        # Yellow
    "too_low": (0, 128, 255),    # Orange
    "too_shallow": (0, 0, 255),  # Red
    "default": (255, 255, 255)   # White
}

# ✨ Smooth angle history (for better visuals)
angle_history = {
    "knee": deque(maxlen=5),
    "elbow": deque(maxlen=5),
    "hip": deque(maxlen=5)
}

def draw_landmarks(image, landmarks, state=None, show_angles=True):
    if not landmarks or len(landmarks) < 33:
        return image

    # 🦵 Squat: Knee angle
    left_hip = landmarks[23]
    left_knee = landmarks[25]
    left_ankle = landmarks[27]

    # 💪 Pushup: Elbow angle
    left_shoulder = landmarks[11]
    left_elbow = landmarks[13]
    left_wrist = landmarks[15]

    # 🪵 Plank: Hip angle (shoulder-hip-ankle)
    shoulder = landmarks[11]
    hip = landmarks[23]
    ankle = landmarks[27]

    # --- Helper: Draw lines and dots
    def draw_line(pt1, pt2, color=(255, 255, 255), thickness=2):
        x1, y1 = int(pt1.x * image.shape[1]), int(pt1.y * image.shape[0])
        x2, y2 = int(pt2.x * image.shape[1]), int(pt2.y * image.shape[0])
        cv2.line(image, (x1, y1), (x2, y2), color, thickness)

    def draw_circle(pt, color=(255, 255, 255), radius=6):
        x, y = int(pt.x * image.shape[1]), int(pt.y * image.shape[0])
        cv2.circle(image, (x, y), radius, color, -1)

    # --- Helper: Angle calculation
    def calculate_angle(a, b, c):
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
        return int(angle)

    # --- Draw Pose Lines and Angles
    feedback_color = COLORS.get(state, COLORS["default"])

    # Squat knee angle
    knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    angle_history["knee"].append(knee_angle)
    smoothed_knee = int(np.mean(angle_history["knee"]))

    draw_line(left_hip, left_knee, feedback_color)
    draw_line(left_knee, left_ankle, feedback_color)
    draw_circle(left_knee, feedback_color)

    if show_angles:
        cv2.putText(image, f'Knee: {smoothed_knee}°', 
                    (int(left_knee.x * image.shape[1]) - 50, int(left_knee.y * image.shape[0]) - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, feedback_color, 2)

    # Push-up elbow angle
    elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    angle_history["elbow"].append(elbow_angle)
    smoothed_elbow = int(np.mean(angle_history["elbow"]))

    draw_line(left_shoulder, left_elbow, feedback_color)
    draw_line(left_elbow, left_wrist, feedback_color)
    draw_circle(left_elbow, feedback_color)

    if show_angles:
        cv2.putText(image, f'Elbow: {smoothed_elbow}°',
                    (int(left_elbow.x * image.shape[1]) - 50, int(left_elbow.y * image.shape[0]) - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, feedback_color, 2)

    # Plank hip angle
    hip_angle = calculate_angle(shoulder, hip, ankle)
    angle_history["hip"].append(hip_angle)
    smoothed_hip = int(np.mean(angle_history["hip"]))

    draw_line(shoulder, hip, feedback_color)
    draw_line(hip, ankle, feedback_color)
    draw_circle(hip, feedback_color)

    if show_angles:
        cv2.putText(image, f'Hip: {smoothed_hip}°',
                    (int(hip.x * image.shape[1]) - 50, int(hip.y * image.shape[0]) - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, feedback_color, 2)

    return image
