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



# if st.session_state.df is not None:

#     st.subheader("Original Dataset")

#     st.write(st.session_state.df.dtypes)



tab1,tab2=st.tabs(["Filter & Update","Update"])



with tab1:

    st.subheader("Original Dataset Sample")

    st.write(st.session_state.df.head())

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

    

    # tab1,tab2=st.tabs(["Confirm","Update"])

    # with tab1:

    #     with st.container(border=True):

    #         if 'MATERIAL' in st.session_state.df.columns:

    #             material_options = st.session_state.df['MATERIAL'].unique().tolist()

    #             selected_material = st.selectbox("Select Material:", options=material_options, key='tab1_material_select')

    #             # Rest of your code...

    #             if selected_material:

    #                 selected_row = st.session_state.df[st.session_state.df['MATERIAL'] == selected_material]

    #                 if not selected_row.empty:

    #                     rn = selected_row.index[0] # Get the index of the selected row.

    #                     updated_df = st.write(selected_row.copy()) #use copy to avoid slice issue.

    

    #                     if st.button("Confirm Changes"):

    #                         st.success("Comfirmed!")

    #                 else:

    #                     st.write("No matching material found.")

    # with tab2:

    with st.container(border=True):

        if 'MATERIAL' in st.session_state.df.columns:

            material_options = st.session_state.df['MATERIAL'].unique().tolist()

            selected_material_to_update = st.selectbox("Select Material:", options=material_options, key='tab2_material_select')

    

            if selected_material_to_update:

                selected_row = st.session_state.df[st.session_state.df['MATERIAL'] == selected_material_to_update]

                if not selected_row.empty:

                    rn = selected_row.index[0] # Get the index of the selected row.

                    updated_df = st.data_editor(selected_row.copy()) #use copy to avoid slice issue.

    

                    if st.button("Update Changes"):

                        updated_row_dict = pd.DataFrame(updated_st.df).iloc[0].to_dict()

                        updated_row_dict['UPDATED_BY'] = st.session_state.user_name

                        updated_row_dict['UPDATED_DATED'] = datetime.datetime.now(pytz.timezone('Asia/Singapore')).isoformat()

                        updated_row_dizt['ACTIVE FLAG'] = False

                       # Update st.session_state.df using 'MATERIAL' as the key

                        st.session_state.df.loc[st.session_state.df['MATERIAL'] == selected_material_to_update] = updated_row_dict

                        st.success("Updated successfully!")

                else:

                    st.write("No matching material found.")





with tab2:

    material1_options = st.session_state.df['STANDARD_LEVEL_1_MATERIAL'].unique().tolist()

    selected_material1 = st.selectbox("Select Material 1:", options=material1_options)



    filtered_df_material2 = st.session_state.df[st.session_state.df['STANDARD_LEVEL_1_MATERIAL'] == selected_material1]

    material2_options = filtered_df_material2['STANDARD_LEVEL_2_MATERIAL'].unique().tolist()

    selected_material2 = st.selectbox("Select Material 2:", options=material2_options)



    filtered_df_material3 = filtered_df_material2[filtered_df_material2['STANDARD_LEVEL_2_MATERIAL'] == selected_material2]

    material3_options = filtered_df_material3['STANDARD_LEVEL_3_MATERIAL'].unique().tolist()

    selected_material3 = st.selectbox("Select Material 3:", options=material3_options)



    filtered_df_material4 = filtered_df_material3[filtered_df_material3['STANDARD_LEVEL_3_MATERIAL'] == selected_material3]

    material4_options = filtered_df_material4['STANDARD_LEVEL_4_MATERIAL'].unique().tolist()

    selected_material4 = st.selectbox("Select Material 4:", options=material4_options)



    final_df = filtered_df_material4[filtered_df_material4['STANDARD_LEVEL_4_MATERIAL'] == selected_material4]





    if not final_df.empty:

        edited_df = st.data_editor(final_df, key='hierarchical_material_editor')

        if st.button("Confirm Changes"):

            for index, row in edited_df.iterrows():

                original_row = final_df.loc[final_df['MATERIAL'] == row['MATERIAL']].iloc[0]

                if not row.equals(original_row):

                    # Handle NaT values and format timestamp:

                    updated_dated = row['UPDATED_DATED']

                    if pd.isna(updated_dated):

                        updated_dated = datetime.datetime.now(pytz.timezone('Asia/Singapore')).isoformat() # default to current time.

                    else:

                        updated_dated = pd.to_datetime(updated_dated).tz_localize('Asia/Singapore').isoformat()

    

                    # Construct the UPDATE query:

                    update_query = f"""

                        UPDATE DB_DW_DEV.RPT_STREAMLIT.STANDARD_LEVEL_MATERIAL_CLONE

                        SET {', '.join([f"{col} = '{row[col]}'" if not pd.isna(row[col]) else f"{col} = NULL" for col in row.index if col not in ['MATERIAL', 'UPDATED_BY', 'UPDATED_DATED']])},

                        UPDATED_BY = '{st.session_state.user_name}',

                        UPDATED_DATED = '{updated_dated}'

                        WHERE MATERIAL = '{row['MATERIAL']}'

                    """

                    try:

                        session.sql(update_query).collect()

                        st.success(f"Row with MATERIAL '{row['MATERIAL']}' updated.")

                    except Exception as e:

                        st.error(f"Error updating row with MATERIAL '{row['MATERIAL']}': {e}")

            st.session_state.df = load_data()

            st.rerun()



it updated in main table, but showing in tab1, tab2 dfs and data editors in both tabs why, not changed