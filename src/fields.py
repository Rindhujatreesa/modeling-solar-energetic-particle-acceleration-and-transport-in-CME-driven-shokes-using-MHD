import numpy as np
from .config import B0, r0, Vsw, Omega

def parker_spiral(position):
    r = np.linalg.norm(position)
    if r == 0:
        return np.zeros(3)

    x, y, z = position
    phi = np.arctan2(y, x)

    Br = B0 * (r0 / r)**2
    Bphi = - (Omega * r / Vsw) * Br

    # Convert properly
    Bx = Br * np.cos(phi) - Bphi * np.sin(phi)
    By = Br * np.sin(phi) + Bphi * np.cos(phi)

    # Add small z component to avoid planar trapping
    Bz = 0.1 * Br

    return np.array([Bx, By, Bz])