# v3_columns.py
import streamlit as st


def bayes_theorem(prior, sensitivity, specificity):
    posterior = (sensitivity * prior) / ((sensitivity * prior) + (1 - specificity) * (1 - prior))
    return posterior

st.title("🦠 COVID-19 Bayes Calculator")

with st.sidebar:
    prior = st.slider("Prior Probability (P(COVID))", 0.01, 0.5, 0.05)
    sensitivity = st.slider("Sensitivity", 0.5, 1.0, 0.9)
    specificity = st.slider("Specificity", 0.5, 1.0, 0.95)

posterior = bayes_theorem(prior, sensitivity, specificity)

col1, col2 = st.columns(2)
with col1:
    st.metric("Prior", f"{prior*100:.2f}%")
with col2:
    st.metric("Posterior", f"{posterior*100:.2f}%")