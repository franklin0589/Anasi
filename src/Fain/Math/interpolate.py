import math

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)




def lerp(t: float, a: float, b: float) -> float:
    """Linearly interpolate between a and b by t."""
    return a * (1 - t) + b * t


def polar(x: float, y: float, rlen: float, ang: float) -> tuple[float, float]:
    """Calculate the polar coordinates based on the given parameters."""
    return (x + rlen * math.cos(ang), y + rlen * math.sin(ang))

clamp = lambda x, min_, max_: max(min(x, max_), min_)
