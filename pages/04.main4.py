import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Streamlit

# Set page title
st.title("Virtual Solar System: Star Radial Velocity and Orbital Animation")

# Define star and planet properties
star = {"name": "Star X", "mass": 1.0, "type": "G-type Main Sequence"}
planets = {
    "Planet A": {"mass": 1.0, "period": 10.0, "semi_major_axis": 0.1, "color": "red"},    # Jupiter-like
    "Planet B": {"mass": 0.3, "period": 4.0, "semi_major_axis": 0.05, "color": "blue"},   # Neptune-like
    "Planet C": {"mass": 0.01, "period": 1.0, "semi_major_axis": 0.02, "color": "green"}  # Earth-like
}

# Display star and planet information
st.header("Star and Planet Information")
st.write(f"**{star['name']}**:")
st.write(f"- Mass: {star['mass']} solar masses")
st.write(f"- Type: {star['type']}")
st.write("**Planets**:")
for name, props in planets.items():
    st.write(f"{name}:")
    st.write(f"- Mass: {props['mass']} Jupiter masses")
    st.write(f"- Orbital Period: {props['period']} days")
    st.write(f"- Semi-major Axis: {props['semi_major_axis']} AU")

# User input: select planets for radial velocity
selected_planets = st.multiselect(
    "Select planets for radial velocity plot:",
    list(planets.keys()),
    default=["Planet A"]
)

# Function to calculate radial velocity for a single planet
def radial_velocity(t, mass, period, semi_major_axis, star_mass=1.0):
    K = (28.4329 / np.sqrt(1 - 0.0**2)) * (mass / star_mass) * (2 * np.pi * 6.67430e-11 * star_mass / (period * 86400))**0.3333
    return K * np.sin(2 * np.pi * t / period)

# Radial velocity plot
st.header("Radial Velocity Plot")
t = np.linspace(0, 20, 1000)
vr_total = np.zeros_like(t)
for planet in selected_planets:
    vr = radial_velocity(
        t,
        planets[planet]["mass"],
        planets[planet]["period"],
        planets[planet]["semi_major_axis"]
    )
    vr_total += vr

fig_rv, ax_rv = plt.subplots()
ax_rv.plot(t, vr_total, label="Total Radial Velocity", color="blue")
ax_rv.set_xlabel("Time (days)")
ax_rv.set_ylabel("Radial Velocity (m/s)")
ax_rv.set_title("Star's Radial Velocity Due to Selected Planets")
ax_rv.grid(True)
ax_rv.legend()
st.pyplot(fig_rv)

# Animation of planets orbiting the star
st.header("Planetary Orbits Animation")
fig_anim, ax_anim = plt.subplots()
ax_anim.set_xlim(-0.15, 0.15)
ax_anim.set_ylim(-0.15, 0.15)
ax_anim.set_xlabel("X (AU)")
ax_anim.set_ylabel("Y (AU)")
ax_anim.set_title("Orbit of Planets around Star X")
ax_anim.grid(True)

# Plot star at center
star_plot, = ax_anim.plot(0, 0, 'o', color="yellow", markersize=15, label="Star X")

# Initialize planet plots
planet_plots = {}
for name in planets:
    planet_plots[name], = ax_anim.plot([], [], 'o', color=planets[name]["color"], markersize=8, label=name)

ax_anim.legend()

# Animation functions
def init():
    for name in planets:
        planet_plots[name].set_data([], [])
    return [star_plot] + list(planet_plots.values())

def update(frame):
    for name, props in planets.items():
        t = frame * 0.05  # Scale time for animation
        x = props["semi_major_axis"] * np.cos(2 * np.pi * t / props["period"])
        y = props["semi_major_axis"] * np.sin(2 * np.pi * t / props["period"])
        planet_plots[name].set_data([x], [y])
    return [star_plot] + list(planet_plots.values())

# Create animation
ani = FuncAnimation(fig_anim, update, init_func=init, frames=200, interval=50, blit=True)

# Save animation to temporary file and display in Streamlit
import io
import base64
buf = io.BytesIO()
ani.save(buf, format="gif", writer="pillow", fps=20)
buf.seek(0)
data = base64.b64encode(buf.read()).decode("ascii")
st.image(f"data:image/gif;base64,{data}")

# Display selected planets for radial velocity
st.write(f"Selected planets for radial velocity: {', '.join(selected_planets) if selected_planets else 'None'}")
