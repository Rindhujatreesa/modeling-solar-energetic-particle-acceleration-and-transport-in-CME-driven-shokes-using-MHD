import numpy as np

# Physical constants
q = 1.602e-19       # charge (C)
m = 1.673e-27       # proton mass (kg)

# Solar parameters
B0 = 5e-9           # Tesla at reference distance
r0 = 1.0            # AU
Vsw = 400e3         # m/s
Omega = 2.7e-6      # rad/s

# Simulation parameters
DT = 0.01
STEPS = 500
N_PARTICLES = 500
SCATTER_STRENGTH = 0.05