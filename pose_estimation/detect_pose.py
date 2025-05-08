import mediapipe as mp
import cv2
import time

mp_pose = mp.solutions.pose

def get_pose_model():
    """
    Returns a configured MediaPipe Pose object.
    Use within a 'with' block to manage resources properly.
    """
    return mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=False,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

def detect_pose(frame, pose_model, debug=False):
    """
    Detect pose landmarks using MediaPipe BlazePose.
    
    Args:
        frame (np.ndarray): Input video frame.
        pose_model: A MediaPipe pose object created from get_pose_model().
        debug (bool): If True, prints logs for debugging.

    Returns:
        tuple: (landmarks_list, full_results) or (None, None) on failure.
    """
    try:
        start_time = time.time()
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose_model.process(image_rgb)

        if results.pose_landmarks:
            if debug:
                print(f"[INFO] Pose detected. Time: {time.time() - start_time:.4f}s")
            return results.pose_landmarks.landmark, results
        else:
            if debug:
                print(f"[WARNING] Pose not detected. Time: {time.time() - start_time:.4f}s")
            return None, None

    except Exception as e:
        print(f"[ERROR] Pose detection failed: {e}")
        return None, None
