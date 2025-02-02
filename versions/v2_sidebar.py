# v2_sidebar.py
import streamlit as st

st.title("🦠 COVID-19 Bayes Calculator")

with st.sidebar:
    prior = st.slider("Prior Probability (P(COVID))", 0.01, 0.5, 0.05)
    sensitivity = st.slider("Sensitivity (P(Test+ | COVID))", 0.5, 1.0, 0.9)
    specificity = st.slider("Specificity (P(Test- | No COVID))", 0.5, 1.0, 0.95)

st.write(f"Prior: {prior}, Sensitivity: {sensitivity}, Specificity: {specificity}")