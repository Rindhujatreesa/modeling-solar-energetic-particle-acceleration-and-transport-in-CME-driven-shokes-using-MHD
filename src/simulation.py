import numpy as np
from .particles import initialize_particles
from .integrator import lorentz_step
from .scattering import scatter_velocity
from .config import DT, STEPS

def run_simulation(N=None, steps=STEPS, dt=DT):
    pos, vel = initialize_particles(N)

    trajectory = []

    for _ in range(steps):
        for i in range(len(pos)):
            pos[i], vel[i] = lorentz_step(pos[i], vel[i], dt)
            vel[i] = scatter_velocity(vel[i])

        trajectory.append(pos.copy())

    return np.array(trajectory), vel