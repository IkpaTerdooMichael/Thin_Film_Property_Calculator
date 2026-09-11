# app.py
# Run with: streamlit run app.py
# Install: pip install streamlit numpy

import streamlit as st
import numpy as np

st.set_page_config(page_title="Thin Film Property Calculator", page_icon="🧪")

st.title("🧪 Thin Film Property Calculator")
st.markdown("*Smart Surfaces & Functional Materials*")

# Controls
st.subheader("Controls")

wavelength = st.slider("Wavelength (nm)", min_value=380, max_value=780, value=550, step=1)
thickness = st.slider("Film Thickness (nm)", min_value=10, max_value=500, value=100, step=1)
n = st.slider("Film Refractive Index (n)", min_value=1.0, max_value=3.5, value=1.5, step=0.01)
ns = st.slider("Substrate Refractive Index (n_s)", min_value=1.0, max_value=4.0, value=1.52, step=0.01)


def calculate_thin_film(wavelength_nm, thickness_nm, n_film, n_sub, n_ambient=1.0):
    """Calculate reflectance and transmittance for a thin film at normal incidence."""
    # Phase thickness (radians)
    delta = 2 * np.pi * n_film * thickness_nm / wavelength_nm

    # Fresnel reflection coefficients at each interface (normal incidence)
    r01 = (n_ambient - n_film) / (n_ambient + n_film)
    r12 = (n_film - n_sub) / (n_film + n_sub)

    # Total reflection coefficient (Airy summation)
    numerator = r01 + r12 * np.exp(-2j * delta)
    denominator = 1 + r01 * r12 * np.exp(-2j * delta)
    r_total = numerator / denominator

    R = np.abs(r_total) ** 2
    T = 1.0 - R  # non-absorbing film
    return R, T


R, T = calculate_thin_film(wavelength, thickness, n, ns)

# Results
st.subheader("Results")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Reflectance (R)", f"{R * 100:.2f} %")
with col2:
    st.metric("Transmittance (T)", f"{T * 100:.2f} %")

# Interference classification
optical_path = n * thickness
qwot = optical_path / (wavelength / 4)  # quarter-wave optical thickness

if abs(qwot - round(qwot)) < 0.05 and round(qwot) % 2 == 1:
    interference = "Destructive (quarter-wave)"
elif abs(qwot - round(qwot)) < 0.05 and round(qwot) % 2 == 0:
    interference = "Constructive (half-wave)"
else:
    interference = "Partial"

with col3:
    st.metric("Interference", interference)

st.warning("⚠️ Assumes normal incidence, non-absorbing film, and air as ambient (n₀ = 1.0).")
