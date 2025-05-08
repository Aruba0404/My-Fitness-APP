import numpy as np

def calculate_angle(a, b, c):
    """Calculate angle between 3 Mediapipe landmarks"""
    a = np.array([a.x, a.y])  # First
    b = np.array([b.x, b.y])  # Middle
    c = np.array([c.x, c.y])  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    return angle if angle <= 180 else 360 - angle
