import streamlit as st
import pandas as pd

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f0f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Dataset Upload and Filter App")
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.filters = []

uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="file_uploader")
if uploaded_file is not None:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    st.session_state.df = df
    st.write(df.dtypes)
    st.session_state.filter_cols = list(df.columns)

if st.session_state.df is not None:
    st.subheader("Original Dataset")
    st.write(st.session_state.df)

    if st.button("Add Filter"):
        st.session_state.filters.append({"column": "", "value": "", "operator": ""})
    
    for i, filter in enumerate(st.session_state.filters):
        col1, col2, col3 = st.columns(3)
        with col1:
            filter['column'] = st.selectbox(f"Select Column {i+1}", options=st.session_state.filter_cols, key=f"select_col_{i}")
        with col2:
            column = filter['column']
            if st.session_state.df[column].dtype == 'int64':
                filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
            elif st.session_state.df[column].dtype == 'float64':
                filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
            elif st.session_state.df[column].dtype == 'object':
                if pd.to_datetime(st.session_state.df[column], errors='coerce').notnull().all():
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["start date", "end date", "between dates"], key=f"operator_{i}")
                else:
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["contains", "starts with", "ends with", "equals"], key=f"operator_{i}")
            else:
                filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
        with col3:
            filter['value'] = st.text_input(f"Enter value to filter by for column {filter['column']}", key=f"filter_value_{i}")

if st.button("Apply Filters"):
    filtered_df = st.session_state.df.copy()
    
    for filter in st.session_state.filters:
        column = filter['column']
        operator = filter['operator']
        value = filter['value']
        if column and value:
            # Convert the value based on the column's dtype
            if filtered_df[column].dtype == 'int64':
                value = int(value)
            elif filtered_df[column].dtype == 'float64':
                value = float(value)
            elif filtered_df[column].dtype == 'object':
                if pd.to_datetime(filtered_df[column], errors='coerce').notnull().all():
                    if operator == "start date":
                        value = pd.to_datetime(value)
                        filtered_df = filtered_df[filtered_df[column] >= value]
                    elif operator == "end date":
                        value = pd.to_datetime(value)
                        filtered_df = filtered_df[filtered_df[column] <= value]
                    elif operator == "between dates":
                        start_date, end_date = value.split(',')
                        start_date = pd.to_datetime(start_date.strip())
                        end_date = pd.to_datetime(end_date.strip())
                        filtered_df = filtered_df[(filtered_df[column] >= start_date) & (filtered_df[column] <= end_date)]
                else:
                    if operator == "contains":
                        filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False)]
                    elif operator == "starts with":
                        filtered_df = filtered_df[filtered_df[column].str.startswith(value)]
                    elif operator == "ends with":
                        filtered_df = filtered_df[filtered_df[column].str.endswith(value)]
                    elif operator == "equals":
                        filtered_df = filtered_df[filtered_df[column] == value]
            # Apply the filter
            if operator in ["==", "!=", ">", "<", ">=", "<="]:
                if operator == "==":
                    filtered_df = filtered_df[filtered_df[column] == value]
                elif operator == "!=":
                    filtered_df = filtered_df[filtered_df[column] != value]
                elif operator == ">":
                    filtered_df = filtered_df[filtered_df[column] > value]
                elif operator == "<":
                    filtered_df = filtered_df[filtered_df[column] < value]
                elif operator == ">=":
                    filtered_df = filtered_df[filtered_df[column] >= value]
                elif operator == "<=":
                    filtered_df = filtered_df[filtered_df[column] <= value]
    
    st.subheader("Filtered Dataset")
    st.write(filtered_df)