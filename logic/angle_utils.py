import math
from collections import deque

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points in 2D space.
    :param a, b, c: Landmarks with .x and .y attributes (MediaPipe format)
    :return: Angle in degrees or -1 on failure
    """
    try:
        a = [a.x, a.y]
        b = [b.x, b.y]
        c = [c.x, c.y]

        ab = [a[0] - b[0], a[1] - b[1]]
        cb = [c[0] - b[0], c[1] - b[1]]

        dot_product = ab[0] * cb[0] + ab[1] * cb[1]
        magnitude_ab = math.sqrt(ab[0]**2 + ab[1]**2)
        magnitude_cb = math.sqrt(cb[0]**2 + cb[1]**2)

        if magnitude_ab == 0 or magnitude_cb == 0:
            return -1

        angle_rad = math.acos(dot_product / (magnitude_ab * magnitude_cb))
        return round(math.degrees(angle_rad), 2)
    except:
        return -1


class SmoothedAngle:
    """
    Smooths out jitter by averaging recent angle values using a fixed-size buffer.
    """
    def __init__(self, maxlen=5):
        self.buffer = deque(maxlen=maxlen)

    def update(self, new_angle):
        if new_angle == -1:
            return -1
        self.buffer.append(new_angle)
        return round(sum(self.buffer) / len(self.buffer), 2)


def is_angle_in_range(angle, min_angle, max_angle):
    """
    Check if an angle is within the desired range.
    """
    return min_angle <= angle <= max_angle


def deviation_from_ideal(angle, ideal_angle):
    """
    Compute how far the angle is from the ideal.
    """
    if angle == -1:
        return float('inf')
    return abs(angle - ideal_angle)


def posture_score(angle, ideal_angle, tolerance=15):
    """
    Return a posture score: 1 = perfect, 0.5 = close, 0 = poor
    """
    deviation = deviation_from_ideal(angle, ideal_angle)
    if deviation <= tolerance / 2:
        return 1.0
    elif deviation <= tolerance:
        return 0.5
    return 0.0
