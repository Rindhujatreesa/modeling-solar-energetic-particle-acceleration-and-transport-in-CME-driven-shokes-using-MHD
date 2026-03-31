import numpy as np
from .config import N_PARTICLES

def initialize_particles(N=N_PARTICLES):
    # Start at realistic heliospheric distance (in meters)
    AU = 1.496e11

    positions = np.zeros((N, 3))
    positions[:, 0] = AU  # start at 1 AU along x-axis

    velocities = np.random.normal(size=(N, 3))
    velocities /= np.linalg.norm(velocities, axis=1)[:, None]

    # Add energy spread
    speeds = np.random.uniform(1e7, 3e7, size=N)
    velocities *= speeds[:, None]

    return positions, velocities