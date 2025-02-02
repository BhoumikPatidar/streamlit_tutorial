# v1_basic.py
import streamlit as st

st.title("🦠 COVID-19 Bayes Calculator")
prior = st.slider("Prior Probability (P(COVID))", 0.01, 0.5, 0.05)
st.write(f"Prior: {prior}")