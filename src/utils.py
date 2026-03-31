import numpy as np

def compute_energy(velocities, mass=1.673e-27):
    speeds = np.linalg.norm(velocities, axis=1)
    return 0.5 * mass * speeds**2

def pitch_angle_cosine(velocities):
    norms = np.linalg.norm(velocities, axis=1)
    return velocities[:, 2] / norms  # assuming B ~ z-direction approx