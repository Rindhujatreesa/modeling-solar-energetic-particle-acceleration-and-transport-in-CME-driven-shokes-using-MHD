import numpy as np
from .config import q, m
from .fields import parker_spiral

def lorentz_step(pos, vel, dt):
    B = parker_spiral(pos)
    acc = (q / m) * np.cross(vel, B)

    vel_new = vel + acc * dt
    pos_new = pos + vel_new * dt

    return pos_new, vel_new