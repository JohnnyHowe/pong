def lerp(a, b, t):
    return clamp(a + (b - a) * t, min(a, b), max(a, b))

def clamp(value, min, max):
    return min if value < min else max if value > max else value