import cv2
import mediapipe as mp
from mediapipe.python.solutions.pose import Pose
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark
from typing import Tuple, List, Optional

mp_pose = mp.solutions.pose

def get_pose_model(
    static_image_mode=False,
    model_complexity=2,
    enable_segmentation=False,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
) -> Pose:
    return mp_pose.Pose(
        static_image_mode=static_image_mode,
        model_complexity=model_complexity,
        enable_segmentation=enable_segmentation,
        smooth_landmarks=True,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

# Global instance
_default_pose_model = get_pose_model()

def detect_pose(frame, pose_model: Optional[Pose] = None, debug: bool = False):
    try:
        if frame is None or frame.size == 0:
            if debug: print("[DEBUG] Empty frame input.")
            return None, None

        if pose_model is None:
            pose_model = _default_pose_model

        if len(frame.shape) == 2 or frame.shape[2] == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose_model.process(image_rgb)

        if results and results.pose_landmarks:
            if debug: print("[INFO] ✅ Pose detected.")
            return results.pose_landmarks.landmark, results
        else:
            if debug: print("[DEBUG] ⚠️ No pose detected.")
            return None, None

    except Exception as e:
        if debug: print(f"[ERROR] Pose detection failed: {e}")
        return None, None
