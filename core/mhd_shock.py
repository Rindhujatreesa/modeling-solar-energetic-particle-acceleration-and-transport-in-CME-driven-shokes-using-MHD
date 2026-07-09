import numpy as np

class CMEShockGenerator:
    """
    Models the MHD macro-properties of a Coronal Mass Ejection (CME) driven shock.
    Uses continuous hyperbolic tangent profiles to simulate the sharp transitions
    (Rankine-Hugoniot jumps) in plasma speed and magnetic field intensity.
    """
    def __init__(self, shock_position=0.0, shock_width=0.05, compression_ratio=3.5):
        self.x_s = shock_position         # Position of the shock front in the grid
        self.w = shock_width              # Spatial thickness of the shock transition layer
        self.s = compression_ratio        # Magnetic field compression ratio (B_downstream / B_upstream)

    def compute_plasma_speed_profile(self, x_grid, V_upstream=400.0, V_downstream=1200.0):
        """
        Generates the solar wind velocity profile V_sw(x) across the shock boundary.
        Units: km/s
        """
        # Smooth step transition modeling the deceleration of plasma relative to the shock front
        return V_upstream + 0.5 * (V_downstream - V_upstream) * (1.0 - np.tanh((x_grid - self.x_s) / self.w))

    def compute_magnetic_field_profile(self, x_grid, B_upstream=5.0):
        """
        Generates the compressed magnetic field profile B(x) across the shock boundary.
        Units: nT (nanotesla)
        """
        B_downstream = B_upstream * self.s
        return B_upstream + 0.5 * (B_downstream - B_upstream) * (1.0 - np.tanh((x_grid - self.x_s) / self.w))

    def compute_adiabatic_divergence(self, x_grid, V_profile):
        """
        Calculates the spatial derivative dV/dx used to determine adiabatic energy 
        losses or shock acceleration rates in advanced particle tracking.
        """
        # Centered finite difference calculation for spatial gradient
        dv_dx = np.zeros_like(V_profile)
        dx = x_grid[1] - x_grid[0]
        dv_dx[1:-1] = (V_profile[2:] - V_profile[:-2]) / (2.0 * dx)
        # Handle boundaries with one-sided differences
        dv_dx[0] = (V_profile[1] - V_profile[0]) / dx
        dv_dx[-1] = (V_profile[-1] - V_profile[-2]) / dx
        return dv_dx