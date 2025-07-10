import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page title
st.title("Virtual Solar System: Star Radial Velocity")

# Define planet properties
planets = {
    "Planet A": {"mass": 1.0, "period": 10.0, "semi_major_axis": 0.1},  # Jupiter-like
    "Planet B": {"mass": 0.3, "period": 4.0, "semi_major_axis": 0.05},  # Neptune-like
    "Planet C": {"mass": 0.01, "period": 1.0, "semi_major_axis": 0.02}   # Earth-like
}

# Function to calculate radial velocity for a single planet
def radial_velocity(t, mass, period, semi_major_axis, star_mass=1.0):
    # Velocity amplitude K (m/s), simplified for circular orbits
    K = (28.4329 / np.sqrt(1 - 0.0**2)) * (mass / star_mass) * (2 * np.pi * 6.67430e-11 * star_mass / (period * 86400))**0.3333
    # Radial velocity: K * sin(2πt / P)
    return K * np.sin(2 * np.pi * t / period)

# User input: select planets
selected_planets = st.multiselect(
    "Select planets to include in the radial velocity plot:",
    list(planets.keys()),
    default=["Planet A"]
)

# Time array for plotting (in days)
t = np.linspace(0, 20, 1000)

# Calculate combined radial velocity
vr_total = np.zeros_like(t)
for planet in selected_planets:
    vr = radial_velocity(
        t,
        planets[planet]["mass"],           # Planet mass in Jupiter masses
        planets[planet]["period"],         # Orbital period in days
        planets[planet]["semi_major_axis"] # Semi-major axis in AU
    )
    vr_total += vr

# Plot the radial velocity
fig, ax = plt.subplots()
ax.plot(t, vr_total, label="Total Radial Velocity", color="blue")
ax.set_xlabel("Time (days)")
ax.set_ylabel("Radial Velocity (m/s)")
ax.set_title("Star's Radial Velocity Due to Selected Planets")
ax.grid(True)
ax.legend()

# Display plot in Streamlit
st.pyplot(fig)

# Display selected planets
st.write(f"Selected planets: {', '.join(selected_planets) if selected_planets else 'None'}")
