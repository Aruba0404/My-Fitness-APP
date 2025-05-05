import mediapipe as mp
import cv2

# High-accuracy BlazePose with upgraded model complexity
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,  # 🔥 Better accuracy than default (0 or 1)
    enable_segmentation=False,
    min_detection_confidence=0.7,  # 🔒 Avoid false detections
    min_tracking_confidence=0.7    # 🔒 Better tracking stability
)

def detect_pose(frame):
    """
    Detect pose landmarks using MediaPipe BlazePose.
    Returns (landmarks, results) or (None, None) if detection fails.
    """
    try:
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results and results.pose_landmarks:
            return results.pose_landmarks.landmark, results
        else:
            return None, None

    except Exception as e:
        print(f"[ERROR] Pose detection failed: {e}")
        return None, None
