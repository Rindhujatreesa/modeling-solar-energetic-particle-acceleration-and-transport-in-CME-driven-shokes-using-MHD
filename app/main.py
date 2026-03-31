import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.simulation import run_simulation
from src.utils import compute_energy, pitch_angle_cosine

st.set_page_config(page_title="SEP Simulation", layout="wide")

st.title("🌞 Solar Energetic Particle Simulation")

# Sidebar controls
st.sidebar.header("Simulation Parameters")

num_particles = st.sidebar.slider("Number of Particles", 100, 2000, 500)
steps = st.sidebar.slider("Time Steps", 100, 2000, 500)

run = st.sidebar.button("Run Simulation")

if run:
    with st.spinner("Running simulation..."):
        traj, final_vel = run_simulation(N=num_particles, steps=steps)

    st.success("Simulation Complete")

    # Plot trajectories
    st.subheader("Particle Trajectories")

    fig, ax = plt.subplots()

    for i in range(min(50, num_particles)):
        ax.plot(traj[:, i, 0], traj[:, i, 1], alpha=0.5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Trajectories")

    st.pyplot(fig)

    # Energy distribution
    st.subheader("Energy Distribution")

    energy = compute_energy(final_vel)

    fig2, ax2 = plt.subplots()
    ax2.hist(energy, bins=50)
    ax2.set_title("Energy Spectrum")

    st.pyplot(fig2)

    # Pitch angle
    st.subheader("Pitch Angle Distribution")

    mu = pitch_angle_cosine(final_vel)

    fig3, ax3 = plt.subplots()
    ax3.hist(mu, bins=50)
    ax3.set_title("Pitch Angle Cosine Distribution")

    st.pyplot(fig3)