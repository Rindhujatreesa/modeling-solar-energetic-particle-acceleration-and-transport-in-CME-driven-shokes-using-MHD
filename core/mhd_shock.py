import numpy as np

class CMEShockGenerator:
    """
    Generates MHD macro-property profiles for the simulation grid.
    This can be based on either an idealized analytical model (tanh) or by
    interpolating data from an external MHD simulation.
    """
    def __init__(self):
        pass

    def get_analytical_profile(self, x_grid, V_upstream=400.0, V_downstream=1200.0, B_upstream=5.0,
                               shock_position=0.0, shock_width=0.05, compression_ratio=3.5):
        """
        Generates idealized solar wind velocity and magnetic field profiles
        using a hyperbolic tangent function to model a shock.
        """
        # Plasma speed
        v_profile = V_upstream + 0.5 * (V_downstream - V_upstream) * \
                    (1.0 - np.tanh((x_grid - shock_position) / shock_width))

        # Magnetic field
        B_downstream = B_upstream * compression_ratio
        b_profile = B_upstream + 0.5 * (B_downstream - B_upstream) * \
                    (1.0 - np.tanh((x_grid - shock_position) / shock_width))

        return v_profile, b_profile

    def get_profile_from_data(self, x_grid, mhd_r, mhd_vr, mhd_br):
        """
        Interpolates velocity and magnetic field profiles from MHD data
        onto the simulation's spatial grid `x_grid`.
        """
        # Ensure the MHD grid covers the simulation grid
        if x_grid.min() < mhd_r.min() or x_grid.max() > mhd_r.max():
            raise ValueError("The simulation grid 'x_grid' is outside the bounds of the MHD data grid 'mhd_r'.")

        # Linearly interpolate the MHD data onto our simulation grid
        v_profile = np.interp(x_grid, mhd_r, mhd_vr)
        b_profile = np.interp(x_grid, mhd_r, mhd_br)

        return v_profile, b_profile

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