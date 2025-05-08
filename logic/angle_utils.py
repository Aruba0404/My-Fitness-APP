import numpy as np

def calculate_angle(a, b, c):
    """
    Calculate angle between three Mediapipe landmarks: a, b, and c.
    Returns the angle in degrees between 0 and 180.
    """
    try:
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        ba = a - b
        bc = c - b

        # Calculate angle between vectors
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Avoid numerical errors

        angle = np.degrees(np.arccos(cosine_angle))
        return angle

    except Exception as e:
        return None  # or return 0 if you prefer
