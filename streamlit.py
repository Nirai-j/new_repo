import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import numpy as np

def create_dataframe(rows, cols):
    data = np.random.randn(rows, cols)
    columns = [f"Column {i}" for i in range(cols)]
    return pd.DataFrame(data, columns=columns)

df = create_dataframe(200, 20)
st.write(df.head())

if df is not None:
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("Column 0", pinned="left")
    gb.configure_column("Column 1", pinned="left")
    gb.configure_default_column(resizable=True, movable=True)
    gridOptions = gb.build()
    st.header("Ag-Grid with Frozen Columns")
    AgGrid(df, gridOptions=gridOptions, fit_columns_on_grid_load=False, allow_unsafe_jscode=True) #Ensure this is True
    st.write("Scroll horizontally to observe the pinned columns.")
    st.subheader("AgGrid feature overview")
    st.write("AgGrid has many features, such as column resizing, reordering, filtering, and sorting.")