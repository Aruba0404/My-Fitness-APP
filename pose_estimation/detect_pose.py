import cv2
import mediapipe as mp
from typing import Optional, Tuple, List
from mediapipe.python.solutions.pose import Pose, PoseLandmark  # ✅ Proper type support

# ✅ MediaPipe Pose module
mp_pose = mp.solutions.pose

def get_pose_model() -> Pose:
    """
    Returns a configured MediaPipe Pose object.
    """
    return Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=False,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

def detect_pose(frame, pose_model: Pose, debug: bool = False) -> Tuple[Optional[List], Optional[object]]:
    """
    Detect pose landmarks using MediaPipe BlazePose.

    Args:
        frame (np.ndarray): Input video frame.
        pose_model (Pose): A MediaPipe pose model.
        debug (bool): If True, prints debugging info.

    Returns:
        tuple: (landmarks list, full results) or (None, None)
    """
    try:
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose_model.process(image_rgb)

        if results.pose_landmarks:
            if debug:
                print("[INFO] ✅ Pose detected.")
            return results.pose_landmarks.landmark, results
        else:
            if debug:
                print("[WARNING] ⚠️ No pose detected.")
            return None, None
    except Exception as e:
        print(f"[ERROR] ❌ Pose detection failed: {e}")
        return None, None
