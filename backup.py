import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [4, 5, 6],
    'D': [4, 5, 6],
    'E': [4, 5, 6],
    'F': [4, 5, 6],
    'G': [4, 5, 6]
})

# Freeze the first column (0th index) using CSS styling
css_style = """
            <style>
                table td:first-child {
                    position: sticky;
                    left: 0;
                    background-color: white;
                }
            </style>
        """

st.write(css_style, unsafe_allow_html=True)
st.table(df)