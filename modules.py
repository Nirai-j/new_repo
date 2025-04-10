import streamlit as st

def initialize_session():
    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.filters = []

def get_filters():
    if 'filters' in st.session_state:
        return st.session_state.filters
    return []

def add_filter(column, value, operator):
    st.session_state.filters.append({"column": column, "value": value, "operator": operator})

def apply_filters(df, filters):
    filtered_df = df.copy()
    for filter in filters:
        column = filter['column']
        operator = filter['operator']
        value = filter['value']
        if column and value:
            if df[column].dtype == 'int64':
                value = int(value)
            elif df[column].dtype == 'float64':
                value = float(value)
            query_str = f"`{column}` {operator} @value"
            filtered_df = filtered_df.query(query_str)
    return filtered_df
