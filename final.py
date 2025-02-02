# app.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. App Configuration

st.set_page_config(
    page_title="COVID Bayes & Data Analysis",
    page_icon="📊",
    layout="centered"
)

# 2. Multi-page Setup
page = st.sidebar.radio("Navigate to", ["COVID Bayes Calculator", "Data Analysis"])

# COVID Bayes Calculator Page
if page == "COVID Bayes Calculator":
    st.title("🦠 COVID-19 Testing: Bayes' Theorem Calculator")
    
    # Bayes-specific sidebar
    with st.sidebar:
        st.header("COVID Test Parameters")
        prior = st.slider("Prior Probability (P(COVID))", 0.01, 0.5, 0.05, 0.01)
        sensitivity = st.slider("Sensitivity (P(Test+ | COVID))", 0.5, 1.0, 0.9, 0.01)
        specificity = st.slider("Specificity (P(Test- | No COVID))", 0.5, 1.0, 0.95, 0.01)

    # Bayes theorem calculation
    def bayes_theorem(prior, sensitivity, specificity):
        false_positive = (1 - specificity) * (1 - prior)
        posterior = (sensitivity * prior) / ((sensitivity * prior) + false_positive)
        return posterior

    posterior = bayes_theorem(prior, sensitivity, specificity)

    # Results columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Prior Probability", f"{prior*100:.2f}%")
    with col2:
        st.metric("Posterior Probability", f"{posterior*100:.2f}%")
    with col3:
        st.metric("Test Accuracy", f"{(sensitivity + specificity)/2*100:.1f}%")

    # Contour plot
    sensitivity_grid, specificity_grid = np.meshgrid(np.linspace(0.5, 1, 50), np.linspace(0.5, 1, 50))
    posterior_grid = bayes_theorem(prior, sensitivity_grid, specificity_grid)

    fig = go.Figure(go.Contour(
        x=sensitivity_grid[0],
        y=specificity_grid[:,0],
        z=posterior_grid,
        colorscale='Viridis',
        contours=dict(showlabels=True)))
    fig.update_layout(
        title="Posterior Probability Landscape",
        xaxis_title="Sensitivity",
        yaxis_title="Specificity",
        height=600)
    st.plotly_chart(fig, use_container_width=True)

# Data Analysis Page
else:
    st.title("📈 Data Analysis Dashboard")
    
    # Data-specific sidebar
    with st.sidebar:
        st.header("Data Controls")
        uploaded_file = st.file_uploader("Upload Dataset (CSV)", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Dataset loaded successfully!")
            
            # Data preview
            with st.expander("View Raw Data"):
                st.dataframe(df.head())

            # Analysis section
            st.subheader("Data Exploration")
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis Variable", df.columns)
            with col2:
                y_col = st.selectbox("Y-axis Variable", df.columns)

            # Plot selection
            plot_type = st.radio("Visualization Type", ["Scatter Plot", "Histogram", "Box Plot"])
            if plot_type == "Scatter Plot":
                fig = px.scatter(df, x=x_col, y=y_col)
            elif plot_type == "Histogram":
                fig = px.histogram(df, x=x_col)
            else:
                fig = px.box(df, x=x_col, y=y_col if y_col != x_col else None)
            st.plotly_chart(fig)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    else:
        st.warning("⚠️ Please upload a CSV file to begin analysis")