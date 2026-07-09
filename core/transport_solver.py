import numpy as np

class FocusedTransportSolver:
    """
    Solves the 1D Focused Transport Equation for Solar Energetic Particles (SEPs)
    df/dt + mu * v * df/dx = d/d_mu ( D_mu (df/d_mu) )
    """
    def __init__(self, x_grid, mu_grid, v, D0, q=1.5):
        self.x = x_grid
        self.mu = mu_grid  # Pitch-angle cosine (-1 to 1)
        self.v = v          # Particle velocity
        self.D0 = D0        # Scattering coefficient
        self.q = q          # Turbulence spectral index
        
        self.dx = x_grid[1] - x_grid[0]
        self.dmu = mu_grid[1] - mu_grid[0]
        
    def pitch_angle_diffusion_coefficient(self, mu):
        """Standard quasi-linear theory formulation for D_mu"""
        Ur = np.abs(mu)**(self.q - 1.0)
        return self.D0 * (1.0 - mu**2) * (Ur + 0.01)

    def step(self, f_current, dt):
        """Advances the particle distribution function by one time-step delta t"""
        f_next = np.copy(f_current)
        Nx, Nmu = f_current.shape
        
        # 1. Advection term (Upwind scheme based on pitch angle sign)
        for i in range(1, Nx - 1):
            for j in range(Nmu):
                mu = self.mu[j]
                if mu > 0:
                    advection = mu * self.v * (f_current[i, j] - f_current[i-1, j]) / self.dx
                else:
                    advection = mu * self.v * (f_current[i+1, j] - f_current[i, j]) / self.dx
                f_next[i, j] -= dt * advection
                
        # 2. Pitch-Angle Diffusion term (Centered difference scheme)
        for i in range(1, Nx - 1):
            for j in range(1, Nmu - 1):
                mu_p = 0.5 * (self.mu[j] + self.mu[j+1])
                mu_m = 0.5 * (self.mu[j] + self.mu[j-1])
                
                D_p = self.pitch_angle_diffusion_coefficient(mu_p)
                D_m = self.pitch_angle_diffusion_coefficient(mu_m)
                
                diffusion = (D_p * (f_current[i, j+1] - f_current[i, j]) - 
                             D_m * (f_current[i, j] - f_current[i, j-1])) / (self.dmu**2)
                f_next[i, j] += dt * diffusion
                
        # Enforce boundary conditions (absorbing at boundaries)
        f_next[0, :] = 0.0
        f_next[-1, :] = 0.0
        return f_next