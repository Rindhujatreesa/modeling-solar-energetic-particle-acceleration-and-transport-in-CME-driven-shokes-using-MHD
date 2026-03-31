import numpy as np
from .config import SCATTER_STRENGTH

def scatter_velocity(vel):
    noise = np.random.normal(scale=SCATTER_STRENGTH, size=3)
    vel = vel + noise
    vel = vel / np.linalg.norm(vel)
    return vel