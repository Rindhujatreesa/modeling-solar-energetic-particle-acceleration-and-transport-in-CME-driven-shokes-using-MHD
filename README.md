# Solar Energetic Particle Acceleration and Transportation in Coronal Mass Ejections Shocks using Magnetohydrodynamics

### Physics-Informed Numerical Simulation and Machine Learning Imputation Framework for Solar Energetic Particle (SEP) Transport across CME-Driven Shocks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Core](https://img.shields.io/badge/Physics-Focused%20Transport-blue)](#theoretical-formulation)

## Overview
This repository contains a research-grade computational framework engineered to model **Solar Energetic Particle (SEP)** acceleration and spatial-temporal evolution within Coronal Mass Ejection (CME) shock boundary environments. 

A central challenge in space climate forecasting and interplanetary mission protection is resolving observational data gaps within multi-mission satellite telemetry. Spacecraft instruments tracking particle **Pitch-Angle Distributions (PADs)** frequently suffer from sensor dead-zones, telemetry dropouts, and geometric shielding limitations. 

This toolkit tackles this challenge by combining **explicit finite-difference numerical solvers** (modeling physical transport laws) with **deep autoencoder neural networks** to impute missing PAD parameters under high uncertainty.

---

## Theoretical Formulation

The baseline particle distribution function $f(x, \mu, t)$ is modeled via the 1D Focused Transport Equation (FTE):

$$\frac{\partial f}{\partial t} + \mu v \frac{\partial f}{\partial x} = \frac{\partial}{\partial \mu} \left( D_\mu(\mu) \frac{\partial f}{\partial \mu} \right) + S(x, \mu, t)$$

Where:
* $x$: Heliocentric spatial coordinate parallel to the magnetic field line.
* $\mu = \cos(\theta)$: Pitch-angle cosine matching the local ambient field.
* $v$: Relativistic/non-relativistic particle velocity matrix.
* $D_\mu(\mu)$: Pitch-angle diffusion coefficient based on quasi-linear magnetic turbulence theory:

$$D_\mu(\mu) = D_0 (1 - \mu^2)|\mu|^{q-1}$$

---

## Architecture Blueprint

The framework bridges physical transport mechanics with deep learning imputation:

```text
+----------------------------------------------------------------------------+
|                          1. PHYSICS ENGINE (FTE)                           |
|  Solves continuous particle distribution f(x, μ, t) via numerical methods.  |
+----------------------------------------------------------------------------+
                                      |
                                      v
+----------------------------------------------------------------------------+
|                         2. OBSERVATION DEGRADER                            |
|    Injects artificial patch/matrix dropouts to simulate spacecraft gaps.   |
+----------------------------------------------------------------------------+
                                      |
                                      v
+----------------------------------------------------------------------------+
|                   3. MACHINE LEARNING ENCODER-DECODER                      |
| Evaluates Masked-MSE Loss to reconstruct fluid-continuous distributions.   |
+----------------------------------------------------------------------------+
```

---

## Plasma and Solar Wind

*Plasma is a quasineutral gas of charged and neutral particles which exhibits a collective behavior.*
A plasma is an ionized gas consisting of charged particles (electrons and ions) whose collective behavior is governed by electromagnetic forces rather than binary collisions. This enables long-range interactions and collective phenomena such as waves and instabilities [[1]](#1-ff-chen-introduction-to-plasma-physics-and-controlled-fusion-doi-101007978-3-319-22309-4_1)

The solar wind is a continuous, supersonic outflow of magnetized plasma from the solar corona into interplanetary space. It carries both mass and magnetic field outward, forming the heliosphere [[2]](#2-en-parker-dynamics-of-the-interplanetary-gas-and-magnetic-fields-doi-101086146579).The plasma escapes due to the high coronal temperature, which expands into the space with magnetic field.

### Mass Conservation Equation

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{u}) = 0
$$

**Variables:**
- $\rho$ : Plasma mass density (kg/m³)  
- $t$ : Time (s)  
- $\mathbf{u}$ : Plasma velocity vector (m/s)  
- $\nabla \cdot$ : Divergence operator  


This equation expresses conservation of mass. Any change in plasma density at a point is balanced by the flow of plasma into or out of that region [[2]](#2-en-parker-dynamics-of-the-interplanetary-gas-and-magnetic-fields-doi-101086146579).


The partial derivative ($\frac{\partial\rho}{\partial t}$) defines the rate of change of density at a fixed point.

The divergence term $\nabla \cdot (\rho \vec{u})$ defines the direction of mass flux ($\rho \vec{u}$).

- If divergence > 0 -> plasma is leaving -> density decreases
- If divergence < 0 -> plasma is entering -> density increases

### Momentum Equation (MHD Form)

$$
\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} \right)
= -\nabla p + \mathbf{J} \times \mathbf{B}
$$

**Variables:**
- $\rho$ : Plasma density  
- $\mathbf{u}$ : Velocity field  
- $p$ : Plasma pressure  
- $\mathbf{J}$ : Electric current density (A/m²)  
- $\mathbf{B}$ : Magnetic field (Tesla)  
- $\nabla p$ : Pressure gradient  


This equation represents conservation of momentum. Plasma motion is driven by pressure gradients and electromagnetic forces, particularly the Lorentz force $\mathbf{J} \times \mathbf{B}$ [[2]](#2-en-parker-dynamics-of-the-interplanetary-gas-and-magnetic-fields-doi-101086146579).


The LHS deals with the changing acceleration due to the following - 
1. The change in velocity at a fixed point (solar wind speeding up)
2. The change in velocity due to plasma entering solar wind of different velocity.

The RHS term explains the pressure forces and magnetic Lorentz forces respectively. These forces are responsible for the bending of the solar wind and the generation of Coronal Mass Ejections and shock in the space.



### Parker Spiral Magnetic Field

$$
B_r \propto \frac{1}{r^2}, \quad
B_\phi \propto -\frac{\Omega r}{V_{sw}} B_r
$$

**Variables:**
- $B_r$ : Radial magnetic field component  
- $B_\phi$ : Azimuthal magnetic field component  
- $r$ : Radial distance from the Sun  
- $\Omega$ : Angular rotation rate of the Sun  
- $V_{sw}$ : Solar wind speed  


Due to solar rotation and outward plasma flow, magnetic field lines are twisted into a spiral structure. This geometry governs how energetic particles propagate through the heliosphere [[2]](#2-en-parker-dynamics-of-the-interplanetary-gas-and-magnetic-fields-doi-101086146579).



## 2. Coronal Mass Ejections (CMEs)

### Definition

A coronal mass ejection (CME) is a large-scale eruption of magnetized plasma from the solar corona into interplanetary space [[3]](#3-n-gopalswamy-coronal-mass-ejections-and-solar-energetic-particles-doi-101007s11214-006-9102-1).



### Alfvén Speed and Shock Formation

$$
V_A = \frac{B}{\sqrt{\mu_0 \rho}}
$$

**Variables:**
- $V_A$ : Alfvén speed (m/s)  
- $B$ : Magnetic field strength (Tesla)  
- $\mu_0$ : Magnetic permeability of free space  
- $\rho$ : Plasma density  

**Shock Condition:**
$$
V_{CME} > V_A
$$


A shock forms when a CME travels faster than the characteristic speed at which disturbances propagate in the plasma. This produces a discontinuity in plasma properties [[4]](#4-ti-gombosi-physics-of-the-space-environment).



## 3. Shock Waves in Space Plasmas

### Definition

A shock wave is a discontinuity across which plasma properties such as density, velocity, and magnetic field change abruptly [[5]](#5-tidman-krall-shock-waves-in-collisionless-plasmas).



### Conservation Across Shock

$$
\rho_1 u_1 = \rho_2 u_2
$$

**Variables:**
- $\rho_1, \rho_2$ : Upstream and downstream densities  
- $u_1, u_2$ : Upstream and downstream velocities  



### Compression Ratio

$$
r = \frac{\rho_2}{\rho_1}
$$

**Variables:**
- $r$ : Compression ratio  


The compression ratio determines how efficiently particles are accelerated at the shock. Higher compression leads to stronger acceleration [[5]](#5-tidman-krall-shock-waves-in-collisionless-plasmas).



## 4. Solar Energetic Particle (SEP) Acceleration

### Definition

Solar energetic particles (SEPs) are high-energy charged particles accelerated during solar eruptions, particularly at CME-driven shocks [[6]](#6-dv-reames-particle-acceleration-at-the-sun-and-in-the-heliosphere-doi-101023a1005105831781).



### Diffusive Shock Acceleration (DSA)

Particles gain energy by repeatedly crossing the shock front due to scattering by magnetic turbulence. This process leads to systematic energy gain over multiple crossings [[7]](#7-ar-bell-the-acceleration-of-cosmic-rays-in-shock-fronts-doi-101093mnras1822147), [[8]](#8-lo-drury-introduction-to-diffusive-shock-acceleration-doi-1010880034-4885468002).



### Energy Spectrum

$$
f(E) \propto E^{-\gamma}
$$

$$
\gamma = \frac{r+2}{r-1}
$$

**Variables:**
- $f(E)$ : Particle energy distribution  
- $E$ : Particle energy  
- $\gamma$ : Spectral index  
- $r$ : Shock compression ratio  


Diffusive shock acceleration naturally produces a power-law energy spectrum, consistent with observations of solar energetic particles [[7]](#7-ar-bell-the-acceleration-of-cosmic-rays-in-shock-fronts-doi-101093mnras1822147).



## 5. Particle Transport in the Heliosphere

### Focused Transport Equation

$$
\frac{\partial f}{\partial t} + \mu v \frac{\partial f}{\partial z} + \frac{1-\mu^2}{2L}
v \frac{\partial f}{\partial \mu} = \frac{\partial}{\partial \mu} \left( D_{\mu\mu} \frac{\partial f}{\partial \mu} \right)
$$


### Variables

- $f(z, \mu, t)$ : Particle distribution function  
- $t$ : Time  
- $z$ : Distance along magnetic field line  
- $\mu = \cos(\theta)$ : Pitch-angle cosine  
- $v$ : Particle speed  
- $L$ : Focusing length  
- $D_{\mu\mu}$ : Pitch-angle diffusion coefficient  



1. **Time Evolution Term**: Represents how the particle distribution changes over time.

$$
\frac{\partial f}{\partial t}
$$


2. **Streaming Term**: Describes particle motion along magnetic field lines.

$$
\mu v \frac{\partial f}{\partial z}
$$



3. **Focusing Term**: Represents how spatial variations in magnetic field strength alter particle directions.

$$
\frac{1-\mu^2}{2L} \, v \frac{\partial f}{\partial \mu}
$$


4. **Diffusion Term**: Describes scattering of particles due to magnetic turbulence, which randomizes their directions [[9]](#9-ec-roelof-propagation-of-solar-cosmic-rays-1969), [[10]](#10-j-skilling-cosmic-ray-streaming-doi-101093mnras1534499).

$$
\frac{\partial}{\partial \mu} \left( D_{\mu\mu} \frac{\partial f}{\partial \mu} \right)
$$



### Focusing Length

$$
L = - \left( \frac{1}{B} \frac{dB}{dz} \right)^{-1}
$$

The focusing length quantifies how rapidly the magnetic field changes along a field line, determining how strongly particles are focused or defocused.



## 6. Particle Motion: Lorentz Force

$$
\frac{d\mathbf{p}}{dt} = q (\mathbf{E} + \mathbf{v} \times \mathbf{B})
$$

**Variables:**
- $\mathbf{p}$ : Particle momentum  
- $q$ : Particle charge  
- $\mathbf{E}$ : Electric field  
- $\mathbf{v}$ : Particle velocity  
- $\mathbf{B}$ : Magnetic field  

This equation governs the motion of charged particles in electromagnetic fields. In the heliosphere, particle trajectories are primarily controlled by magnetic fields [[11]](#11-jd-jackson-classical-electrodynamics).



## 7. Magnetohydrodynamics (MHD)

Magnetohydrodynamics (MHD) is the theoretical framework used to describe the behavior of electrically conducting fluids (such as plasma) in the presence of electromagnetic fields. It combines the principles of fluid dynamics with Maxwell’s equations of electromagnetism.

MHD is essential for modeling:
- Solar wind dynamics  
- CME evolution  
- Shock formation  
- Large-scale heliospheric structure  

[[4]](#4-ti-gombosi-physics-of-the-space-environment), [[12]](#12-h-alfven-existence-of-mhd-waves-doi-101038150405d0)



## 7.1 Foundations of MHD

MHD is derived by coupling:

1. **Fluid equations (mass, momentum, energy)**
2. **Maxwell’s equations (electromagnetism)**



### Maxwell’s Equations (Simplified MHD Form)

$$
\nabla \cdot \mathbf{E} = \frac{\rho_e}{\varepsilon_0}
$$

$$
\nabla \cdot \mathbf{B} = 0
$$

$$
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}
$$

$$
\nabla \times \mathbf{B} = \mu_0 \mathbf{J}
$$

**Variables:**
- $\mathbf{E}$ : Electric field  
- $\mathbf{B}$ : Magnetic field  
- $\mathbf{J}$ : Current density  
- $\rho_e$ : Charge density  
- $\varepsilon_0$ : Permittivity of free space  
- $\mu_0$ : Permeability of free space  


In MHD, we assume quasi-neutrality ($\rho_e \approx 0$) and neglect displacement current, simplifying Maxwell’s equations for plasma conditions.



### Ohm’s Law in a Moving Plasma

$$
\mathbf{E} + \mathbf{u} \times \mathbf{B} = \eta \mathbf{J}
$$

**Variables:**
- $\mathbf{u}$ : Plasma velocity  
- $\eta$ : Electrical resistivity  



### Ideal MHD Approximation

In highly conducting plasmas (like the solar wind), resistivity is negligible:

$$
\mathbf{E} + \mathbf{u} \times \mathbf{B} = 0
$$

This is known as the **ideal MHD condition**.



## 7.2 Induction Equation

Using Faraday’s law and Ohm’s law, we obtain:

$$
\frac{\partial \mathbf{B}}{\partial t}
= \nabla \times (\mathbf{u} \times \mathbf{B})
$$

**Variables:**
- $\mathbf{B}$ : Magnetic field  
- $\mathbf{u}$ : Plasma velocity  



### Physical Meaning

This equation describes how magnetic fields evolve in time due to plasma motion.



## 7.3 Frozen-in Condition

From ideal MHD:

$$
\mathbf{E} + \mathbf{u} \times \mathbf{B} = 0
$$



### Interpretation

Magnetic field lines are “frozen” into the plasma and move with it.



### Physical Consequence

- Plasma carries magnetic field outward (solar wind)  
- CME structures retain magnetic topology  
- Field lines stretch and twist with flow  



## 7.4 Full Set of Ideal MHD Equations

The complete MHD system consists of:



### Mass Conservation

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{u}) = 0
$$



### Momentum Equation

$$
\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} \right)
= -\nabla p + \mathbf{J} \times \mathbf{B}
$$



### Induction Equation

$$
\frac{\partial \mathbf{B}}{\partial t}
= \nabla \times (\mathbf{u} \times \mathbf{B})
$$



### Equation of State (Closure)

$$
p \propto \rho^\gamma
$$

**Variables:**
- $p$ : Pressure  
- $\rho$ : Density  
- $\gamma$ : Adiabatic index (typically 5/3)  



## 7.5 Magnetic Pressure and Tension

Magnetic fields exert forces that can be interpreted as:



### Magnetic Pressure

$$
P_B = \frac{B^2}{2\mu_0}
$$



### Magnetic Tension

Force along field lines due to curvature.



### Physical Meaning

- Magnetic pressure pushes plasma outward  
- Magnetic tension pulls along field lines  



## 7.6 Alfvén Waves

Alfvén waves are transverse waves in which magnetic field lines oscillate while plasma moves with them.



### Alfvén Speed

$$
V_A = \frac{B}{\sqrt{\mu_0 \rho}}
$$



### Interpretation

- Sets the speed of information propagation in plasma  
- Determines shock formation conditions  



[[12]](#12-h-alfven-existence-of-mhd-waves-doi-101038150405d0)



## 7.7 MHD Waves

There are three fundamental MHD wave modes:

1. **Alfvén waves** (transverse)  
2. **Slow magnetosonic waves**  
3. **Fast magnetosonic waves**



### Importance

These waves:
- Transport energy  
- Scatter particles  
- Contribute to turbulence  



## 7.8 MHD Shocks

When plasma flow exceeds characteristic wave speeds, shocks form.


### Types of MHD Shocks

- Fast shocks  
- Slow shocks  
- Intermediate shocks  



### Physical Role

In CME-driven shocks:
- Plasma is compressed  
- Magnetic fields are amplified  
- Particles are accelerated (DSA)  



## 7.9 Why MHD is Critical for SEP Modeling

MHD provides:

- Large-scale plasma structure  
- Magnetic field geometry  
- Shock properties  

These directly determine:
- Where particles are accelerated  
- How they propagate  


### Final Insight

MHD describes the **macroscopic plasma environment**, while kinetic equations describe **particle behavior within that environment**.

Together, they form the foundation of modern space weather modeling.

## References

#### [1] F.F. Chen, *Introduction to Plasma Physics and Controlled Fusion*, doi: 10.1007/978-3-319-22309-4_1  
<a id="1-ff-chen-introduction-to-plasma-physics-and-controlled-fusion-doi-101007978-3-319-22309-4_1"></a>

#### [2] E.N. Parker, "Dynamics of the Interplanetary Gas and Magnetic Fields", *The Astrophysical Journal*, 1958, doi: 10.1086/146579  
<a id="2-en-parker-dynamics-of-the-interplanetary-gas-and-magnetic-fields-doi-101086146579"></a>

#### [3] N. Gopalswamy, "Coronal Mass Ejections and Solar Energetic Particles", *Space Science Reviews*, 2006, doi: 10.1007/s11214-006-9102-1  
<a id="3-n-gopalswamy-coronal-mass-ejections-and-solar-energetic-particles-doi-101007s11214-006-9102-1"></a>

#### [4] T.I. Gombosi, *Physics of the Space Environment*, Cambridge University Press, 2015  
<a id="4-ti-gombosi-physics-of-the-space-environment"></a>

#### [5] Tidman & Krall, *Shock Waves in Collisionless Plasmas*, 1971  
<a id="5-tidman-krall-shock-waves-in-collisionless-plasmas"></a>

#### [6] D.V. Reames, "Particle Acceleration at the Sun and in the Heliosphere", *Space Science Reviews*, 1999, doi: 10.1023/A:1005105831781  
<a id="6-dv-reames-particle-acceleration-at-the-sun-and-in-the-heliosphere-doi-101023a1005105831781"></a>

#### [7] A.R. Bell, "The Acceleration of Cosmic Rays in Shock Fronts", *MNRAS*, 1978, doi: 10.1093/mnras/182.2.147  
<a id="7-ar-bell-the-acceleration-of-cosmic-rays-in-shock-fronts-doi-101093mnras1822147"></a>

#### [8] L.O. Drury, "An Introduction to the Theory of Diffusive Shock Acceleration", *Reports on Progress in Physics*, 1983, doi: 10.1088/0034-4885/46/8/002  
<a id="8-lo-drury-introduction-to-diffusive-shock-acceleration-doi-1010880034-4885468002"></a>

#### [9] E.C. Roelof, "Propagation of Solar Cosmic Rays in the Interplanetary Magnetic Field", 1969  
<a id="9-ec-roelof-propagation-of-solar-cosmic-rays-1969"></a>

#### [10] J. Skilling, "Cosmic Ray Streaming I", *MNRAS*, 1971, doi: 10.1093/mnras/153.4.499  
<a id="10-j-skilling-cosmic-ray-streaming-doi-101093mnras1534499"></a>

#### [11] J.D. Jackson, *Classical Electrodynamics*, Wiley, 3rd Edition, 1998  
<a id="11-jd-jackson-classical-electrodynamics"></a>

#### [12] H. Alfvén, "Existence of Electromagnetic-Hydrodynamic Waves", *Nature*, 1942, doi: 10.1038/150405d0  
<a id="12-h-alfven-existence-of-mhd-waves-doi-101038150405d0"></a>
