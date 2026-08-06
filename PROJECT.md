## Objective

## Project Objectives

The overarching goal of this framework is to pioneer a physics-informed computational pipeline that leverages machine learning architectures to resolve spatial-temporal data anomalies and structural dropouts in space weather telemetry. The project targets three primary milestones:

### 1. High-Fidelity Macro-to-Kinetic Solar Weather Simulation
* **Objective:** Synthesize continuous macro-scale fluid profiles (simulating Coronal Mass Ejection (CME) shock boundaries via Rankine-Hugoniot jump relations) with fine-scale kinetic particle transport dynamics.
* **Impact:** Delivers an independent, physically accurate baseline engine that models how Solar Energetic Particles (SEPs) scatter and accelerate under dynamic heliospheric variations.

### 2. Multi-Mission Spacecraft Telemetry Degradation Modeling
* **Objective:** Code reproducible mathematical frameworks to emulate real-world instrument limitations, capturing both systematic directional sensor blindspots (`patch` dropouts) and geometry-driven pitch-angle loss (`random` dropouts).
* **Impact:** Provides a strict, high-uncertainty validation testbed that exposes Pitch-Angle Distribution (PAD) sequences to actual mission constraint profiles encountered by spacecraft like Parker Solar Probe and Solar Orbiter. The masking now follows the instrument geometry: fixed telescope look directions are combined with evolving magnetic field directions, and the blind spots are placed at pitch-angle bins where the dot product $\mu = \hat{u}_p \cdot \hat{B}$ approaches zero. This makes the missing-data structure tied to the physical observing configuration, while also supporting time-series pitch-angle intensity maps.

### 3. Physics-Inspired Deep Learning Data Imputation
* **Objective:** Architect a deep neural autoencoder optimized through a custom Masked Mean Squared Error (M-MSE) loss function to reconstruct sparse particle continuums without introducing unphysical artifacts.
* **Impact:** Demonstrates how data-driven AI models can exploit latent physical manifolds to robustly bridge observational gaps and enhance the predictive resolution of heliospheric radiation tracking systems.

## Project Directory Structure

```
modeling-sep-acceleration-mhd/
│
├── .gitignore
├── README.md                  # Comprehensive research overview and math guide
├── requirements.txt           # Explicit pinning of scientific packages
│
├── core/                      # Pure physics engine
│   ├── __init__.py
│   ├── mhd_shock.py           # CME shock boundary layer generator
│   └── transport_solver.py    # Finite-difference solver for transport equations
│
├── ml_gap_filling/            # AIPAD Project alignment module
│   ├── __init__.py
│   ├── data_degrader.py       # Artificially injects gaps/dropouts into PADs
│   └── reconstructor.py       # Deep learning / ML architecture for data imputation
│
└── notebooks/                 # Reproducible execution & plotting tracks
    └── research_demo.ipynb    # Walkthrough notebook creating the figures below
```