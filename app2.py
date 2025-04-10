import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set wide mode and page title
st.set_page_config(layout="wide", page_title="Advanced Streamlit App")

# Custom CSS for overall styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        color: #333;
        background-color: #f8f8f8;
    }
    .header {
        background-color: #f0f0f5;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .section {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stTextInput > div > div > input {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px;
    }
    .styled-table {
        border-collapse: collapse;
        width: 100%;
        
    }
    .styled-table th, .styled-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .styled-table th {
        background-color: #1aa11a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header section
st.markdown("<div class='header'>", unsafe_allow_html=True)
st.title("Advanced Streamlit App")
st.subheader("Random Data Exploration and Visualization")
st.markdown("</div>", unsafe_allow_html=True)

# Create random DataFrame
np.random.seed(42)  # For reproducibility
data = {
    'A': np.random.randint(0, 100, 100),
    'B': np.random.rand(100),
    'C': np.random.choice(['X', 'Y', 'Z'], 100),
    'D': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), 100))
}
df = pd.DataFrame(data)

# Section 1: Data Filtering
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header("Data Filtering")

# Filter columns
selected_columns = st.multiselect("Select Columns", df.columns)
filtered_df = df[selected_columns] if selected_columns else df

# Display filtered data with styling
st.markdown("<table class='styled-table'>", unsafe_allow_html=True)
st.write(filtered_df.to_html(index=False, classes="styled-table"), unsafe_allow_html=True)
st.markdown("</table>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Section 2: Data Visualization
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header("Data Visualization")

# Visualization options
chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"])

if chart_type == "Line Chart":
    x_column = st.selectbox("Select X-axis Column", filtered_df.columns)
    y_column = st.selectbox("Select Y-axis Column", filtered_df.columns)
    fig = px.line(filtered_df, x=x_column, y=y_column)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Bar Chart":
    x_column = st.selectbox("Select X-axis Column", filtered_df.columns)
    y_column = st.selectbox("Select Y-axis Column", filtered_df.columns)
    fig = px.bar(filtered_df, x=x_column, y=y_column)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Scatter Plot":
    x_column = st.selectbox("Select X-axis Column", filtered_df.columns)
    y_column = st.selectbox("Select Y-axis Column", filtered_df.columns)
    color_column = st.selectbox("Select Color Column (Optional)", [None] + list(filtered_df.columns))
    fig = px.scatter(filtered_df, x=x_column, y=y_column, color=color_column)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Histogram":
    column = st.selectbox("Select Column for Histogram", filtered_df.columns)
    fig = px.histogram(filtered_df, x=column)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Section 3: Data Summary
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header("Data Summary")

# Display summary statistics with styling
st.markdown("<table class='styled-table'>", unsafe_allow_html=True)
st.write(df.describe().to_html(classes="styled-table"), unsafe_allow_html=True)
st.markdown("</table>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)