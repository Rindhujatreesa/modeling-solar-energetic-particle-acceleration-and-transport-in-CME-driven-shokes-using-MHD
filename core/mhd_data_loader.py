import numpy as np
import h5py

class MHDDataLoader:
    """
    Loads 1D MHD simulation data from a local HDF5 file for use in the
    transport solver. Assumes the HDF5 file contains 1D datasets for
    radial coordinate 'r', radial velocity 'vr', and radial magnetic field 'br'.
    """
    def __init__(self):
        pass

    def load_1d_profile(self, h5_filepath):
        """
        Loads 1D radial profiles for r, Vr, and Br from a local HDF5 file.

        Args:
            h5_filepath (str): Path to the HDF5 data file.

        Returns:
            tuple: (r_coords, vr_profile, br_profile)
        """
        with h5py.File(h5_filepath, 'r') as f:
            # Assumes the HDF5 file has datasets named 'r', 'vr', and 'br'
            r_coords = f['r'][:]
            vr_profile = f['vr'][:]
            br_profile = f['br'][:]

