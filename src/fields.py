import numpy as np
from .config import B0, r0, Vsw, Omega

def parker_spiral(position):
    r = np.linalg.norm(position)
    if r == 0:
        return np.zeros(3)

    Br = B0 * (r0 / r)**2
    Bphi = - (Omega * r / Vsw) * Br

    # Convert to Cartesian approximation
    x, y, z = position
    phi = np.arctan2(y, x)

    Bx = Br * np.cos(phi) - Bphi * np.sin(phi)
    By = Br * np.sin(phi) + Bphi * np.cos(phi)

    return np.array([Bx, By, 0.0])