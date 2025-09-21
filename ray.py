from collections import deque

from bh_accel import bh_accel
from constants import *


class Ray:
    __slots__ = ("x", "y", "vx", "vy", "trail")
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.trail = deque(maxlen=MAX_TRAIL)
    
    def step(self, dt, M, r_s):
        ax, ay = bh_accel(self.x, self.y, M, r_s)

        self.x += self.vx * dt + 0.5 * ax * dt * dt
        self.y += self.vy * dt + 0.5 * ay * dt * dt

        ax2, ay2 = bh_accel(self.x, self.y, M, r_s)

        self.vx += 0.5 * (ax + ax2) * dt
        self.vy += 0.5 * (ay + ay2) * dt

        self.trail.appendleft((self.x, self.y))
