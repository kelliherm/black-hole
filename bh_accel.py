import math

from constants import *


def bh_accel(px, py, M, r_s, softening=1e-3):
    """Returns the acceleration of a ray using Paczynski-Wiita"""
    rx, ry = px, py
    r = math.hypot(rx, ry)

    if r <= r_s + 1e-6:
        r = r_s + 1e-6
    
    denom = (r - r_s)
    if denom < softening:
        denom = softening

    a_mag = - G * M / (denom * denom)

    ax = a_mag * (rx / r)
    ay = a_mag * (ry / r)

    return ax, ay