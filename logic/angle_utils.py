import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the angle between three points (in 3D space).
    Points must be MediaPipe landmarks with .x, .y, .z attributes.

    Arguments:
    a, b, c -- landmarks where 'b' is the vertex point

    Returns:
    angle in degrees
    """
    a = np.array([a.x, a.y, a.z])
    b = np.array([b.x, b.y, b.z])
    c = np.array([c.x, c.y, c.z])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    angle = np.arccos(cosine_angle)
    return np.degrees(angle)
