import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="COVID Bayes & Data Analysis", layout="centered")
page = st.sidebar.radio("Navigate", ["COVID Calculator", "Data Analysis"])

if page == "COVID Calculator":
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

    sensitivity_grid = np.linspace(0.5, 1.0, 50)
    specificity_grid = np.linspace(0.5, 1.0, 50)
    posterior_grid = np.array([[bayes_theorem(prior, s, sp) for s in sensitivity_grid] 
                            for sp in specificity_grid])

    fig = go.Figure(go.Contour(
        x=sensitivity_grid,
        y=specificity_grid,
        z=posterior_grid,
        colorscale='Viridis'
    ))
    st.plotly_chart(fig)

else:  # Data Analysis Page
    st.title("📈 Data Analysis")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis", df.columns)
        fig = px.scatter(df, x=x_col, y=y_col)
        st.plotly_chart(fig)