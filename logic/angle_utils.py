import numpy as np

def calculate_angle(a, b, c):
    """
    Calculate the 3D angle between Mediapipe landmarks a, b, and c.
    Returns the angle in degrees (0° to 180°).
    """
    try:
        a = np.array([a.x, a.y, a.z])
        b = np.array([b.x, b.y, b.z])
        c = np.array([c.x, c.y, c.z])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # numerical safety

        angle = np.degrees(np.arccos(cosine_angle))
        return angle

    except Exception as e:
        print(f"[Angle ERROR] {e}")
        return None
