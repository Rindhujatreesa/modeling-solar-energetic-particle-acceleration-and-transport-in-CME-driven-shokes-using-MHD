## Objective

- A Monte Carlo particle transport model was developed to simulate solar energetic particle propagation in a Parker spiral magnetic field. 
- Particle trajectories were computed using the Lorentz force, while pitch-angle scattering was implemented as a stochastic process to emulate diffusion in turbulent magnetic fields. 
- The model captures key features of SEP transport, including anisotropy evolution and spatial diffusion.

## Project Directory Structure

```
sep_simulation/
│
├── src/
│   ├── config.py
│   ├── fields.py
│   ├── particles.py
│   ├── integrator.py
│   ├── scattering.py
│   ├── simulation.py
│   └── utils.py
│
├── app/
│   └── main.py   # Streamlit dashboard
│
├── requirements.txt
└── README.md
```