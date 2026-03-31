import numpy as np
from .config import N_PARTICLES

def initialize_particles(N=N_PARTICLES):
    positions = np.zeros((N, 3))

    velocities = np.random.normal(size=(N, 3))
    velocities /= np.linalg.norm(velocities, axis=1)[:, None]

    speeds = np.random.uniform(1e7, 2e7, size=N)
    velocities *= speeds[:, None]

    return positions, velocities