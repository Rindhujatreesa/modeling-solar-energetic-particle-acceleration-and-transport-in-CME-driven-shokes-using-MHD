**Literature Review**

## Plasma: The fourth state of matter [[1]](#1-ff-chen-introduction-to-plasma-physics-and-controlled-fusion-doi-101007978-3-319-22309-4_1)

Plasma is the state of matter at high temperature in vacuum, when the atom ionizes to a positive ion and electron(s), with atleast one positive charge.
- This makes plasma a charged medium with rampant electric field.
- The colliion of particles in a plasma medium corresponds to interaction of electric fields between the ions, rather than physical interactions.
- Plasma usually exists only in vacuum, as air tends to cool down the ions resulting in combining of ions and electrons to form neutral atoms.


The Saha's equation provides the ratio of ionization to be expected in a gas in thermal equilibrium.

$$
\frac{n_i}{n_n}\approx 2.4\times 10^{21} \frac{T^{3/2}}{n_i}e^{-U_i/KT}
$$

Where, $n_i$ and $n_n$ are the density (number per $m^3$) of ionized atoms and neutral atoms respectively.

$T$ is the gas temperature in Kelvin, $K$ is the Boltzmann's constant, and $U_i$ is the ionization energy of the gas - number of Joules required to remove the outermost electron from an atom.

At room temperature ($T=300K$), $n_n\approx 3\times 10^{25} m^{-3}$, and $U_i=14.5eV$ for nitrogen. The ratio is very low - 

$$
\frac{n_i}{n_n}\approx 10^{-122}
$$

**Definition of Plasma**: A plasma is a *quasineutral* gas of charged and neutral particles which exhibits *collective behavior*.

#### What is collective behavior?

Plasma, due to its ions and electrons, exhibits a behavior that is not influenced by external factors like sound waves. This is because the plasma particles do not undergo "direct" collisions for a wave propagation due to its innate electromagnetic forces, which are much larger than local forces. The long-range Coulombic forces is the reason for motion of particles in plasma, and this "collisionless" characteristics due to electromagnetic forces is the *"collective behavior"* of plasma.

#### Debye Shielding and Quasineutrailty

Debye Length is a measure of the shielding distance or thickness of the sheath (charge cloud) formed when the plasma is exosed to an external electric field. It is given by - 

$$
\lambda_D \equiv (\frac{\epsilon_0KT_e}{ne^2})^{1/2}
$$

where, $n=n_{\infty}$ is the ion density.

- Without an infinite thermal agitation ($KT_e$), the charge cloud would collapse into a thin layer.
- As the ion density increases, the Debye length decreases

If the dimension $L$ of the plasma system is much larger thean the Debye length $\lambda_D$, any external potentials introduced to the system are shielded out, leaving the bulk of plasma free of electric potentials or fields. This makes the plasma *quasineutral*, i.e., neutral enough so that $n_i\simeq n_e \simeq n$, where n is the plasma density, but there is still some electromagnetic force in some area.

- **1. An ionized gas is considered plasma only when the density is enough to satisfy the condition: $\lambda_D \ll L$** 
- **2. For the Debye Shielding to be valid, the number of particles in a Debye Sphere should satisfy the collective behavior condition: $N_D \ggg 1$**
        where, 
        $$
        N_D = \frac43n\pi\lambda_D^3 = 1.38 \times 10^6\times \frac{T^{3/2}}{n^{1/2}}
        $$
- **3. If $\omega$ is the frequency of typical plasma oscillations and $\tau$ is the mean time between collisions with neutral atoms, the ionized gas is considered plasma only if $\omega \tau > 1$

## Plasma in Space

## Single Particle Theory

## Adiabatic Invariants

## Plasma as Fluid

## Maxwell's Equations and Plasma

## MagnetoHydroDynamics (MHD)



## Citations

#### [1] F.F. Chen, Introduction to Plasma Physics and Controlled Fusion, doi 10.1007/978-3-319-22309-4_1