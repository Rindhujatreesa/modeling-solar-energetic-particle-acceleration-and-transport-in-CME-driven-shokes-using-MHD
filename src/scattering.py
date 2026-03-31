import numpy as np
from .config import SCATTER_STRENGTH

def scatter_velocity(vel):
    noise = np.random.normal(scale=0.2, size=3)  # increase strength
    vel = vel + noise
    vel = vel / np.linalg.norm(vel) * np.linalg.norm(vel)
    return vel