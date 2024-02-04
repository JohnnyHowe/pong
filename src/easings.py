import math


def lerp(a, b, t):
    return clamp(a + (b - a) * t, min(a, b), max(a, b))

def lerp_position(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))

def inverse_lerp(a, b, value):
    return clamp01((value - a) / (b - a))

def ease_in_cubic(x):
    return clamp01(x) ** 3

def ease_out_cubic(x):
    return 1 - math.pow(1 - clamp01(x), 3);

def east_in_then_out(x, ease_in_curve, ease_out_curve, hold=0, hold_value=1):
    x = clamp01(x)
    lower_cutoff = (1 - hold) / 2
    upper_cutoff = (1 + hold) / 2

    if x < lower_cutoff:
        t = x / lower_cutoff
        return ease_in_curve(t)
    elif x > upper_cutoff:
        t = (x - upper_cutoff) / (1 - upper_cutoff)
        return 1 - ease_out_curve(t)

    return hold_value 

def clamp01(value):
    return clamp(value, 0, 1)
    
def clamp(value, min, max):
    return min if value < min else max if value > max else value