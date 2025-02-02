# final.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------
# 1. App Configuration
# ----------------------
st.set_page_config(
    page_title="Streamlit Demo App",
    page_icon="📊",
    layout="centered"
)

# ----------------------
# 2. Multi-page Setup
# ----------------------
page = st.sidebar.radio("Navigate", ["COVID Bayes Calculator", "Data Analysis Demo"])

# ----------------------
# COVID Bayes Calculator Page
# ----------------------
if page == "COVID Bayes Calculator":
    st.title("🦠 COVID-19 Testing: Bayes' Theorem Calculator")
    
    # Sidebar inputs
    with st.sidebar:
        st.header("Parameters")
        prior = st.slider("Prior Probability (P(COVID))", 0.01, 0.5, 0.05, 0.01)
        sensitivity = st.slider("Sensitivity (P(Test+ | COVID))", 0.5, 1.0, 0.9, 0.01)
        specificity = st.slider("Specificity (P(Test- | No COVID))", 0.5, 1.0, 0.95, 0.01)
        
        # Additional input types
        st.divider()
        uploaded_file = st.file_uploader("Upload prevalence data (CSV)")
        user_name = st.text_input("Your name")

    # Bayes theorem calculation
    def bayes_theorem(prior, sensitivity, specificity):
        false_positive = (1 - specificity) * (1 - prior)
        posterior = (sensitivity * prior) / ((sensitivity * prior) + false_positive)
        return posterior

    posterior = bayes_theorem(prior, sensitivity, specificity)

    # Display results in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Prior Probability", f"{prior*100:.2f}%")
    with col2:
        st.metric("Posterior Probability", f"{posterior*100:.2f}%")
    with col3:
        st.metric("Test Accuracy", f"{(sensitivity + specificity)/2*100:.1f}%")

    # Plotly contour plot
    sensitivity_grid, specificity_grid = np.meshgrid(np.linspace(0.5, 1, 50), np.linspace(0.5, 1, 50))
    posterior_grid = bayes_theorem(prior, sensitivity_grid, specificity_grid)

    fig = go.Figure(go.Contour(
        x=sensitivity_grid[0],
        y=specificity_grid[:,0],
        z=posterior_grid,
        colorscale='Viridis',
        contours=dict(showlabels=True)
    ))
    fig.update_layout(
        title="Posterior Probability Landscape",
        xaxis_title="Sensitivity",
        yaxis_title="Specificity",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Data Analysis Demo Page
# ----------------------
else:
    st.title("📈 Data Analysis Demo")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        
        # Show dataframe
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Interactive filters
        st.subheader("Data Exploration")
        col1, col2 = st.columns(2)
        
        with col1:
            x_col = st.selectbox("X-axis", df.columns)
        with col2:
            y_col = st.selectbox("Y-axis", df.columns)
            
        # Dynamic plot
        plot_type = st.radio("Plot type", ["Scatter", "Histogram"])
        
        if plot_type == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_col)
        else:
            fig = px.histogram(df, x=x_col)
            
        st.plotly_chart(fig)
        
    else:
        st.warning("⚠️ Please upload a CSV file to begin analysis")
