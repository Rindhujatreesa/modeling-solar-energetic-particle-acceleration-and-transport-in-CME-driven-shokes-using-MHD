import numpy as np

class SpacecraftDataDegrader:
    """Simulates multi-mission spacecraft instrument blindspots and orbital telemetry dropouts"""
    def __init__(self, random_state=42):
        self.rng = np.random.default_rng(random_state)
        
    def inject_pitch_angle_gaps(self, clean_distribution, mask_fraction=0.3, gap_type='patch'):
        """Injects artificial dropouts into Pitch-Angle Distribution matrix"""
        degraded = np.copy(clean_distribution)
        mask = np.ones_like(clean_distribution, dtype=bool)
        
        if gap_type == 'patch':
            # Simulates an instrument sensor dead-zone blocking specific angular fields over time
            Nx, Nmu = clean_distribution.shape
            num_gaps = int(Nmu * mask_fraction)
            gap_indices = self.rng.choice(Nmu, size=num_gaps, replace=False)
            degraded[:, gap_indices] = 0.0
            mask[:, gap_indices] = False
            
        elif gap_type == 'random':
            # Simulates telemetry packet loss
            mask = self.rng.random(clean_distribution.shape) > mask_fraction
            degraded[~mask] = 0.0
            
        return degraded, mask