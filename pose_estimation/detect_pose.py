import mediapipe as mp
import cv2
import time

# High-accuracy BlazePose with upgraded model complexity
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,  # Better accuracy than default (0 or 1)
    enable_segmentation=False,
    min_detection_confidence=0.7,  # Avoid false detections
    min_tracking_confidence=0.7    # Better tracking stability
)

def detect_pose(frame):
    """
    Detect pose landmarks using MediaPipe BlazePose.
    Returns (landmarks, results) or (None, None) if detection fails.
    """
    try:
        # Start timer to measure processing time
        start_time = time.time()

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        # Log the confidence levels for debugging
        detection_confidence = results.pose_landmarks is not None
        tracking_confidence = results.pose_landmarks is not None

        if detection_confidence and tracking_confidence:
            # Log successful detection
            print(f"[INFO] Pose detected with confidence. Time taken: {time.time() - start_time:.4f}s")
            return results.pose_landmarks.landmark, results
        else:
            # Log failure or low confidence
            print(f"[WARNING] Pose detection failed or had low confidence. Time taken: {time.time() - start_time:.4f}s")
            return None, None

    except Exception as e:
        # Enhanced error logging
        print(f"[ERROR] Pose detection failed: {e}")
        return None, None
