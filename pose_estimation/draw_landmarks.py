import cv2
import mediapipe as mp

# Initialize MediaPipe Drawing Utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_landmarks(landmark_obj, frame, feedback_text=None, rep_count=None):
    """
    Draws the pose landmarks, feedback, and rep count on the frame.
    
    Args:
    landmark_obj (obj): The MediaPipe pose landmark object.
    frame (ndarray): The frame (image) to draw landmarks and feedback on.
    feedback_text (str, optional): Text for feedback to be displayed on the frame.
    rep_count (int, optional): Number of repetitions to display on the frame.

    Returns:
    frame (ndarray): The frame with landmarks and feedback drawn on it.
    """
    if landmark_obj is not None:
        # Draw pose landmarks on the frame
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=landmark_obj,
            connections=mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=4, circle_radius=5),  # Red dots
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=2)  # Yellow lines
        )

        # Label key joints (Shoulder, Hip, Knee, Ankle)
        if hasattr(landmark_obj, 'landmark'):
            h, w = frame.shape[:2]
            landmarks = landmark_obj.landmark
            point_map = {
                "Shoulder": 11,
                "Hip": 23,
                "Knee": 25,
                "Ankle": 27
            }

            for label, idx in point_map.items():
                if idx < len(landmarks):  # Ensure index is within bounds
                    cx, cy = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
                    cv2.putText(frame, label, (cx + 5, cy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Draw feedback text at the bottom of the frame
    if feedback_text:
        color = (0, 255, 0)  # Default green for positive feedback

        # Dynamic feedback color based on message
        if "❌" in feedback_text or "too" in feedback_text.lower():
            color = (0, 0, 255)  # Red for error feedback
        elif "⬇️" in feedback_text:
            color = (0, 255, 255)  # Yellow for warning feedback

        # Adjust position dynamically to avoid overlap with the frame's bottom
        y_pos = frame.shape[0] - 20
        cv2.putText(frame, feedback_text, (10, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3, cv2.LINE_AA)

    # Draw the rep count at the bottom-left of the frame
    if rep_count is not None and rep_count != "-":
        cv2.putText(frame, f"Reps: {rep_count}", (10, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)

    return frame
