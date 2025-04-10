# Import python packages
import streamlit as st
import pandas as pd
import datetime
import pytz
from snowflake.snowpark.context import get_active_session


st.set_page_config(layout="wide")
# Get active Snowflake session
session = get_active_session()

st.title('BRD - Material Level Update Approval Process')

@st.cache_data()
def get_user_name():
    try:
        name = session.sql("SELECT CURRENT_USER();").collect()
        return name[0][0]
    except Exception as e:
        st.error(f"Error retrieving Snowflake username: {e}")
        return "Unknown User"

def set_background():
    gradient = "linear-gradient(225deg, #FFFFFFff, #FFFBF8ff, #FFF8F0ff, #FFF4E9ff, #FFF0E2ff, #FFEDDAff, #FFE9D3ff)"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: {gradient};
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <style>
    .stApp {
        # background-image: linear-gradient(225deg, #FFFFFFff, #FFFBF8ff, #FFF8F0ff, #FFF4E9ff, #FFF0E2ff, #FFEDDAff, #FFE9D3ff);
        background-attachment: fixed;
        padding-left: 500px;
        padding-right: 500px;
        max-width: 1500px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data(ttl=3600)
def load_data():
    return session.sql("select * from DB_DW_DEV.RPT_STREAMLIT.STANDARD_LEVEL_MATERIAL_CLONE").to_pandas()

user_name = get_user_name()
if 'user_name' not in st.session_state:
    st.session_state.user_name = user_name

if 'df' not in st.session_state:
    st.session_state.df = load_data()
    st.session_state.cols = list(st.session_state.df.columns)

if 'filters' not in st.session_state:
    st.session_state.filters = []
    st.session_state.filtered_df = pd.DataFrame()

if st.session_state.df is not None:
    st.subheader("Original Dataset")
    st.write(st.session_state.df.dtypes)

if st.button("Add Filter"):
    st.session_state.filters.append({"column": "", "value": "", "operator": ""})

with st.container(border=True):
    for i, filter in enumerate(st.session_state.filters):
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            filter['column'] = st.selectbox(f"Select Column {i+1}", options=st.session_state.cols, key=f"select_col_{i}")
        with col2:
            column_name = filter['column']
            if column_name and column_name in st.session_state.df.columns:
                column_series = st.session_state.df[column_name]
                if pd.api.types.is_integer_dtype(column_series) or pd.api.types.is_float_dtype(column_series):
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
                elif pd.api.types.is_object_dtype(column_series) and column_name == 'DATE_OF_FILE':
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["between", "==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
                elif pd.api.types.is_object_dtype(column_series) and column_name != 'DATE_OF_FILE':
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["contains", "starts with", "ends with", "equals"], key=f"operator_{i}")
                elif pd.api.types.is_datetime64_any_dtype(column_series):
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["between", "==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
                elif pd.api.types.is_object_dtype(column_series):
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["contains", "starts with", "ends with", "equals", "!="], key=f"operator_{i}")
                else:
                    filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")

        with col3:
            if filter['operator'] == "between":
                if pd.api.types.is_datetime64_any_dtype(st.session_state.df[column_name]) or filter['column'] == 'DATE_OF_FILE':
                    filter['value'] = st.date_input(f"Start and End Date {i+1}", value=(pd.to_datetime('today').date(), pd.to_datetime('today').date()), key=f"filter_value_{i}")
                else:
                    filter['value'] = st.text_input(f"Enter value to filter", key=f"filter_value_{i}")
            elif pd.api.types.is_datetime64_any_dtype(st.session_state.df[column_name]) or filter['column'] == 'DATE_OF_FILE':
                filter['value'] = st.date_input(f"Select Date {i+1}", value=pd.to_datetime('today').date(), key=f"filter_value_{i}")
            else:
                filter['value'] = st.text_input(f"Enter value to filter", key=f"filter_value_{i}")
        with col4:
            st.write("")
            st.write("")
            if st.button("❌", key=f"remove_filter_{i}", use_container_width=True):
                del st.session_state.filters[i]
                st.rerun()

        if i < len(st.session_state.filters) - 1:
            st.divider()

if st.session_state.filters and st.button("Apply Filters"):
    filtered_df = st.session_state.df.copy()
    for filter in st.session_state.filters:
        column = filter['column']
        operator = filter['operator']
        value = filter['value']

        if column and value:
            if pd.api.types.is_integer_dtype(filtered_df[column]):
                try:
                    value = int(value)
                    if operator == "==": filtered_df = filtered_df[filtered_df[column] == value]
                    elif operator == "!=": filtered_df = filtered_df[filtered_df[column] != value]
                    elif operator == ">": filtered_df = filtered_df[filtered_df[column] > value]
                    elif operator == "<": filtered_df = filtered_df[filtered_df[column] < value]
                    elif operator == ">=": filtered_df = filtered_df[filtered_df[column] >= value]
                    elif operator == "<=": filtered_df = filtered_df[filtered_df[column] <= value]
                except ValueError:
                    st.error(f"Invalid integer value for column {column}")
            elif pd.api.types.is_float_dtype(filtered_df[column]):
                try:
                    value = float(value)
                    if operator == "==": filtered_df = filtered_df[filtered_df[column] == value]
                    elif operator == "!=": filtered_df = filtered_df[filtered_df[column] != value]
                    elif operator == ">": filtered_df = filtered_df[filtered_df[column] > value]
                    elif operator == "<": filtered_df = filtered_df[filtered_df[column] < value]
                    elif operator == ">=": filtered_df = filtered_df[filtered_df[column] >= value]
                    elif operator == "<=": filtered_df = filtered_df[filtered_df[column] <= value]
                except ValueError:
                    st.error(f"Invalid float value for column {column}")
            elif pd.api.types.is_datetime64_any_dtype(filtered_df[column]):
                try:
                    if operator == "between":
                        start_date, end_date = value
                        start_date = pd.to_datetime(start_date).tz_localize('Asia/Singapore')
                        end_date = pd.to_datetime(end_date).tz_localize('Asia/Singapore')
                        filtered_df = filtered_df[(filtered_df[column] >= start_date) & (filtered_df[column] <= end_date)]
                    else:
                        value = pd.to_datetime(value).tz_localize('Asia/Singapore')
                        if operator == "==": filtered_df = filtered_df[filtered_df[column] == value]
                        elif operator == "!=": filtered_df = filtered_df[filtered_df[column] != value]
                        elif operator == ">": filtered_df = filtered_df[filtered_df[column] > value]
                        elif operator == "<": filtered_df = filtered_df[filtered_df[column] < value]
                        elif operator == ">=": filtered_df = filtered_df[filtered_df[column] >= value]
                        elif operator == "<=": filtered_df = filtered_df[filtered_df[column] <= value]
                except ValueError:
                    st.error(f"Invalid datetime value for column {column}")
            elif column == 'DATE_OF_FILE':
                try:
                    filtered_df['DATE_OF_FILE'] = pd.to_datetime(filtered_df['DATE_OF_FILE'])
                    if operator == "between":
                        start_date, end_date = value
                        start_date = pd.Timestamp(start_date)
                        end_date = pd.Timestamp(end_date)
                        filtered_df = filtered_df[(filtered_df[column] >= start_date) & (filtered_df[column] <= end_date)]
                    else:
                        value = pd.Timestamp(value)
                        if operator == "==": filtered_df = filtered_df[filtered_df[column] == value]
                        elif operator == "!=": filtered_df = filtered_df[filtered_df[column] != value]
                        elif operator == ">": filtered_df = filtered_df[filtered_df[column] > value]
                        elif operator == "<": filtered_df = filtered_df[filtered_df[column] < value]
                        elif operator == ">=": filtered_df = filtered_df[filtered_df[column] >= value]
                        elif operator == "<=": filtered_df = filtered_df[filtered_df[column] <= value]
                except ValueError:
                    st.error(f"Invalid date value for column {column}")
            elif pd.api.types.is_object_dtype(filtered_df[column]):
                try:
                    if operator == "contains": filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False, na=False)]
                    elif operator == "starts with": filtered_df = filtered_df[filtered_df[column].str.startswith(value, na=False)]
                    elif operator == "ends with": filtered_df = filtered_df[filtered_df[column].str.endswith(value, na=False)]
                    elif operator == "equals" or operator == "==": filtered_df = filtered_df[filtered_df[column] == value]
                    elif operator == "!=": filtered_df = filtered_df[filtered_df[column] != value]
                except ValueError:
                    st.error(f"Invalid string value for column {column}")
    st.divider()
    st.subheader("Filtered Dataset")
    try:
        st.write(filtered_df)
    except Exception as e:
        st.error(f"Unable to display DataFrame: {str(e)}")

st.divider()

tab1,tab2=st.tab("")
    with st.container(border=True):
            # Assuming you have a 'MATERIAL' column in your DataFrame
            if 'MATERIAL' in st.session_state.df.columns:
                material_options = st.session_state.df['MATERIAL'].unique().tolist()
                selected_material = st.selectbox("Select Material:", options=material_options)
    
                if selected_material:
                    selected_row = st.session_state.df[st.session_state.df['MATERIAL'] == selected_material]
                    if not selected_row.empty:
                        rn = selected_row.index[0] # Get the index of the selected row.
                        updated_df = st.data_editor(selected_row.copy()) #use copy to avoid slice issue.
    
                        if st.button("Confirm Changes"):
                            updated_row_dict = pd.DataFrame(updated_st.df).iloc[0].to_dict()
                            updated_row_dict['UPDATED_BY'] = st.session_state.user_name
                            updated_row_dict['UPDATED_DATED'] = datetime.datetime.now(pytz.timezone('Asia/Singapore')).isoformat()
                            st.session_state.df.iloc[rn] = updated_row_dict #update session state.
                            st.write("Changes confirmed!")
                    else:
                        st.write("No matching material found.")
            else:
                st.error("The 'MATERIAL' column does not exist in the DataFrame.")