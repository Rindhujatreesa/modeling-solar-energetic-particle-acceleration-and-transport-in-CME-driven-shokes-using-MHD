# Code File Explanations

This document provides a detailed breakdown of the purpose, mathematical background, and programmatic implementation of every core code file within the project repository.

---

## 1. core/mhd_shock.py (Macro-Environment Generator)

### Purpose
Before particles can be accelerated or tracked, they require a background space weather environment to move through. This file generates the macroscopic fluid background of a moving Coronal Mass Ejection (CME) shock wave. It provides the localized values for solar wind speed ($V_{sw}$) and magnetic field intensity ($B$) that dynamically influence particle transport.

### Core Architecture & Logic
* **Rankine-Hugoniot Jump Modeling:** Instead of modeling a sudden, mathematically discontinuous step function (which causes numerical stability issues in partial differential equation solvers), it uses a smoothed hyperbolic tangent (`tanh`) profile. This simulates a sharp but continuous transition region representing the shock layer.
* **Velocity Decay & Magnetic Field Compression:** As space coordinates move from upstream (ahead of the shock) to downstream (behind the shock), the solar wind speed sharply decelerates relative to the shock frame, while the magnetic field compresses and grows stronger by the specified `compression_ratio`.
* **Adiabatic Divergence:** The method `compute_adiabatic_divergence` calculates the spatial derivative ($\partial V / \partial x$). In physics, compression zones ($\partial V / \partial x < 0$) compress the particle distribution, serving as the source term for shock acceleration.

---

## 2. core/transport_solver.py (Kinetic Particle Engine)

### Purpose
This file houses the core physics engine of the project. It integrates the 1D Focused Transport Equation (FTE) forward in time, tracing how the phase-space density $f(x, \mu, t)$ of Solar Energetic Particles (SEPs) changes due to streaming parallel to magnetic fields and scattering off magnetic turbulence.

### Core Architecture & Logic
* **Quasi-Linear Theory (QLT) Scattering:** The function `pitch_angle_diffusion_coefficient` implements the standard scattering operator $D_\mu(\mu) = D_0(1-\mu^2)|\mu|^{q-1}$. A small regularization constant (`+ 0.01`) is injected to prevent division-by-zero anomalies when particles cross a pitch-angle cosine of zero ($\mu=0$).
* **Advection Stabilized Upwind Discretization:** Standard central differences for advection terms cause artificial numerical oscillations. This solver implements an **Upwind Scheme**, shifting the spatial stencil derivative based on whether the particle is moving forward ($\mu > 0$) or backward ($\mu < 0$).
* **Boundary Safeguards:** It applies absorbing boundaries at both grid ends ($f = 0$), forcing particles to escape the system if they travel past the outer limits of the computational domain.

---

## 3. ml_gap_filling/data_degrader.py (Telemetry Anomaly Simulator)

### Purpose
Real spacecraft missions (e.g., Parker Solar Probe, Solar Orbiter) do not deliver perfect, gap-free matrices due to hardware limitations, instrument blind spots, or communication dropouts. To train and validate machine learning architectures for the **AIPAD project**, this module takes perfect simulation data and realistically corrupts it.

### Core Architecture & Logic
* **Patch Dropout Modeling (`gap_type='patch'`):** Mimics structural or viewing constraints of a real electrostatic particle detector sensor. It picks randomized pitch-angle bins ($\mu$-strips) and zeros them out across all spatial locations, simulating dead zones or obstructed fields of view.
* **Random Dropout Modeling (`gap_type='random'`):** Simulates standard communication packet loss or extreme measurement noise by masking separate individual pixels in the $(x, \mu)$ grid using a Bernoulli probability distribution.
* **Mask Generation:** Crucially, it returns both the corrupted data array and a boolean `observation_mask`. The mask keeps track of which data points are real (`True`) and which ones are hidden (`False`), which is vital for calculating the loss function during training.

---

## 4. ml_gap_filling/reconstructor.py (Deep Learning Engine)

### Purpose
This file provides the machine learning solution called for by the **AIPAD project**. It utilizes a deep neural network to learn the underlying smooth, continuous physical manifolds of particle behavior, filling in the artificial observation gaps introduced by the data degrader.

### Core Architecture & Logic
* **Symmetric Deep Autoencoder:** The `PADReconstructionNet` processes the data by compressing the angular channels into a lower-dimensional latent space (Encoder) to extract the broad physical features of the distribution. The Decoder stage then scales this latent state back to the original full dimensions.
* **Physics-Aligned Activation Functions:** It uses Hyperbolic Tangent (`Tanh`) activations to allow smooth gradient flows (ideal for reproducing wave and fluid profiles). The final output layer uses a Rectified Linear Unit (`ReLU`) to ensure that particle density results remain physically valid and non-negative ($f \ge 0$).
* **Masked MSE Loss Function:** Standard Mean Squared Error (MSE) would force the model to try and optimize over the entire dataset, ruining the intact telemetry. The custom loop explicitly applies the `~M.bool()` operation, forcing the optimizer to compute gradients and adjust neural weights **only over the data gaps**, leaving pristine data coordinates untouched.

---

## 5. notebooks/research_demo.py (Pipeline Orchestration)

### Purpose
This script serves as the main driver and execution track for the entire toolkit. It imports the individual physical and computational modules, feeds variables from one layer into the next, and prints out validation error metrics.

### Core Architecture & Logic
1. **Initializes Grid Planes:** Establishes coordinate definitions for space ($x$) and pitch angle ($\mu$).
2. **Generates Shock Fronts:** Calls `CMEShockGenerator` to create the background solar wind fields.
3. **Executes Physics Integrator:** Instantiates a particle beam distribution and steps it forward over 50 time increments using `FocusedTransportSolver`.
4. **Applies Instrument Degradation:** Blinds 35% of the data arrays using `SpacecraftDataDegrader` to build an un-imputed input grid.
5. **Executes Neural Optimization:** Trains the deep reconstruction autoencoder for 300 epochs.
6. **Validates Results:** Computes the final Root Mean Squared Error (RMSE) comparing the model's reconstructions directly against the known, hidden ground-truth values from the physical model.