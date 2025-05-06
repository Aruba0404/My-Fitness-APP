import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the angle between three points (in 3D space).
    Points must be MediaPipe landmarks with .x, .y, .z attributes.

    Arguments:
    a, b, c -- landmarks where 'b' is the vertex point (angle point)

    Returns:
    angle in degrees (float) or None if calculation fails
    """
    try:
        # Convert landmarks to numpy arrays
        a = np.array([a.x, a.y, a.z])
        b = np.array([b.x, b.y, b.z])
        c = np.array([c.x, c.y, c.z])

        # Vectors from b to a and b to c
        ba = a - b
        bc = c - b

        # Calculate cosine of the angle
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))

        # Ensure cosine value is in the domain of arccos [-1, 1]
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

        # Calculate the angle in radians and convert to degrees
        angle = np.arccos(cosine_angle)

        # Return angle in degrees
        return np.degrees(angle)

    except Exception as e:
        print(f"[ERROR] Angle calculation failed: {e}")
        return None
