import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from snowflake.snowpark.context import get_active_session

# Get active Snowflake session
session = get_active_session()
#st.set_page_config(layout="wide")
st.set_page_config(
    page_title="My Awesome App",
    page_icon="🚀",
    layout="wide", # or "centered"
    #layout="centered",
    initial_sidebar_state="collapsed", # or "expanded"
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Revised Color Palette (Purple and Lavender focused)
colors = {
    "dark_purple": "#0D0221",      # Dark Purple - Primary text, borders
    "medium_purple": "#4B0082",    # Medium Purple - Header backgrounds, accents
    "lavender": "#E6E6FA",        # Lavender -  Light backgrounds, containers
    "light_lavender": "#F0F0FF",   # Very Light Lavender -  Even lighter backgrounds
    "pale_lavender": "#F8F8FF",    # Pale Lavender -  Subtle backgrounds
    "accent_color": "#6A5ACD",     # Slate Blue - Button accents, highlights
    "text_on_light": "#333333",    # Dark Gray - Text on light backgrounds
    "text_on_dark": "#FFFFFF",  # White - Text on dark backgrounds
    "light_pink": "#FCE4EC",       # Light Pink - Very light background
    "pale_pink": "#F9A8D4",        # Pale Pink - Light background, containers
    "medium_pink": "#F48FB1",       # Medium Pink - Accents, headers
    "deep_pink": "#EC407A",         # Deep Pink - Buttons, interactive elements
    "dark_pink": "#C2185B",          # Dark Pink - Strong accents, borders
    "off_white": "#F8F8FF",         # Off-White -  Alternative light background
    "text_on_light": "#333333",     # Dark Gray - Text on light backgrounds
    "text_on_dark": "#FFFFFF",
    'light_pink_1': '#FFE4E1',  # Light Rose
    'light_pink_2': '#FFECF0',  # Very Light Pink
    'peach_pink': '#FFE5B4',   # Peach Pink (subtle warm tone)
    'off_white': '#F8F8FF'     # Almost White# White - Text on dark backgrounds
}


def set_fun_pink_gradient_background():
    gradient = f"""
        linear-gradient(135deg, {colors['light_pink_1']}, {colors['light_pink_2']}, {colors['peach_pink']}, {colors['off_white']})
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: {gradient};
            background-attachment: fixed;
            color: #333333; /* Default text color */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply the fun pink gradient background
set_fun_pink_gradient_background()

#print("Appled gradient background")
print("Appled gradient background")

# Updated Theme CSS for Streamlit elements - Revised Selectors and Color Scheme
streamlit_theme = f"""
<style>
/* General body text */
body {{
    color: {colors['text_on_light']};
    font-family: sans-serif; /* Example: Use sans-serif for general text */
}}

/* Headers: Using medium purple for prominence */
h1, h2, h3, h4, h5, h6 {{
    color: {colors['medium_purple']};
    font-weight: bold;
    margin-bottom: 0.5em;
}}

/* Containers: Light lavender background with border */
.stApp .stContainer {{
    background-color: {colors['lavender']};
    border: 1px solid {colors['medium_purple']};
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.05); /* Subtle shadow */
}}

/* Buttons - Slate blue with light text */
div.stButton > button:first-child {{
    background-color: {colors['accent_color']};
    color: {colors['text_on_dark']};
    border: 1px solid {colors['medium_purple']};
    border-radius: 25px; /* Rounded buttons */
    padding: 10px 25px;
    font-weight: bold;
}}

div.stButton > button:hover {{
    background-color: {colors['medium_purple']};
    color: white;
    border-color: {colors['dark_purple']};
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] > div {{
    background-color: {colors['medium_purple']}; /* Darker tab header */
    border-bottom: 2px solid {colors['dark_purple']};
    padding: 0 10px;
    border-radius: 8px 8px 0 0;
}}

.stTabs [data-baseweb="tab-list"] button {{
    color: {colors['text_on_dark']}; /* Light text on tab headers */
    background-color: {colors['medium_purple']};
    padding: 10px 15px;
    border-radius: 8px 8px 0 0;
    margin-right: 2px;
    font-weight: bold;
}}

.stTabs [data-baseweb="tab-list"] button:hover {{
    background-color: {colors['accent_color']};
    color: {colors['text_on_dark']};
}}

.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
    background-color: {colors['lavender']}; /* Selected tab content background */
    color: {colors['text_on_light']}; /* Dark text on selected tab */
    font-weight: bold;
    border-bottom: none; /* Remove bottom border of selected tab */
}}

.stTabs [data-baseweb="tab-content"] {{
    background-color: {colors['lavender']}; /* Tab content area */
    padding: 20px;
    border-radius: 0 8px 8px 8px; /* Rounded corners for content area */
    border: 1px solid {colors['medium_purple']};
}}


/* Text Input and Text Area */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {{ /* Added NumberInput */
    background-color: {colors['light_lavender']};
    color: {colors['text_on_light']};
    border: 1px solid {colors['medium_purple']};
    border-radius: 5px;
    padding: 8px;
}}

/* Selectbox */
/* Selectbox */
.stSelectbox > div > div > div {{
    background-color: {colors['light_lavender']};
    color: {colors['text_on_light']};
    border: 1px solid {colors['medium_purple']};
    border-radius: 5px;
    padding: 8px;
}}
.stSelectbox > div > div > div:focus,
.stSelectbox > div > div > div:active {{
    border-color: {colors['accent_color']};
    box-shadow: 0 0 0 0.2rem rgba(106, 90, 205, 0.25); /* Accent color shadow */
}}


/* Dataframe */
.ag-theme-streamlit {{
    background-color: {colors['lavender']};
    color: {colors['text_on_light']};
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid {colors['medium_purple']};
}}

.ag-theme-streamlit .ag-header {{
    background-color: {colors['medium_purple']};
    color: {colors['text_on_dark']};
    border-bottom: 2px solid {colors['dark_purple']};
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}

.ag-theme-streamlit .ag-header-cell-text {{
    color: {colors['text_on_dark']} !important;
    font-weight: bold;
}}

.ag-theme-streamlit .ag-row-odd,
.ag-theme-streamlit .ag-row-even {{
    color: {colors['text_on_light']};
}}

.ag-theme-streamlit .ag-root-wrapper {{
    border-radius: 0 0 8px 8px;
    overflow: hidden;
}}

</style>
"""

st.markdown(streamlit_theme, unsafe_allow_html=True)

st.title("Dataset Upload and Filter App")
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.selected_db=None
    st.session_state.selected_schema=None
    st.session_state.selected_table=None
    st.session_state.filters = []
    st.session_state.filter_cols = []
    st.session_state.new_file_uploaded = False
    st.session_state.uploaded_file_name = None  # Initialize to None
    st.session_state.editor=None
    st.session_state.filtered_df=pd.DataFrame()
    st.session_state.update_query=None
    
# Retrieve list of databases
resultdb = session.sql("show DATABASEs").collect()
databases = [row["name"] for row in resultdb]

# Select database
selected_db = st.selectbox("Select a database", databases)

if selected_db:
    # Retrieve list of schemas
    resultschema = session.sql(f"show SCHEMAS in database {selected_db}").collect()
    schemas = [row["name"] for row in resultschema]

    # Select schema
    selected_schema = st.selectbox("Select a schema", schemas)

    if selected_schema:
        # Retrieve list of tables and views
        resulttable = session.sql(f"SELECT table_name FROM {selected_db}.information_schema.tables WHERE table_schema='{selected_schema}'").collect()
        resulttable
        tables_and_views = [row["TABLE_NAME"] for row in resulttable]
        selected = st.selectbox("Select the table or view",options=tables_and_views)
        if selected:
            uploaded_file_name=f"{selected_db}+{selected_schema}+{selected}"
            df = session.sql(f"select * from {selected_db}.{selected_schema}.{selected}").to_pandas()
            if st.session_state.uploaded_file_name != uploaded_file_name:
                st.session_state.selected_db=selected_db;
                st.session_state.selected_schema=selected_schema;
                st.session_state.selected_table=selected;
                st.session_state.df = df
                st.session_state.editor=None
                st.session_state.filtered_df=pd.DataFrame()
                st.session_state.filter_cols = list(df.columns)
                st.session_state.new_file_uploaded = True
                st.session_state.uploaded_file_name = uploaded_file_name
                st.session_state.filters = []  # Reset filters here.
            else:
                st.session_state.new_file_uploaded = False

# Function to update filtered_df (call this after df changes)
def update_filtered_df():
    unique_column = st.session_state.df.columns[0]
    if st.session_state.df is not None and not st.session_state.df.empty:
        # st.session_state.filtered_df = st.session_state.df[st.session_state.df[unique_column].isin(st.session_state.filtered_df[unique_column])].copy()
        # Apply filtering logic here based on st.session_state.filters
        # For this example, let's assume no filtering is applied
        st.session_state.filtered_df = st.session_state.df.copy()
    else:
        st.session_state.filtered_df = pd.DataFrame()


def create_html_table_with_frozen_columns(df):
    html = """
    <style>
    .table-container {
        width: 100%;
        overflow-x: auto;
        max-height: 500px;
        overflow-y: auto;
    }
    table {
        border-collapse: collapse;
        width: max-content;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        white-space: nowrap;
    }
    th {
        background-color: #C2A1CE;
        color: black;
        font-weight: bold;
        position: sticky;
        top: 0;
    }
    .first-col {
        position: sticky;
        left: 0;
        z-index: 10;
        min-width: 0;
    }
    .second-col {
        position: sticky;
        left: 0;
        z-index: 9;
        min-width: 0;
    }
    th.first-col {
        z-index: 12;
    }
    th.second-col {
        z-index: 11;
    }
    tbody .first-col {
        background-color: white;
    }
    tbody .second-col {
        background-color: white;
    }
    </style>
    <div class="table-container">
        <table id="dataTable">
            <thead>
                <tr>
    """
    for i, col in enumerate(df.columns):
        if i == 0:
            html += f'<th class="first-col">{col}</th>'
        elif i == 1:
            html += f'<th class="second-col">{col}</th>'
        else:
            html += f'<th>{col}</th>'
    html += """
                </tr>
            </thead>
            <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        for i, col in enumerate(df.columns):
            if i == 0:
                html += f'<td class="first-col">{row[col]}</td>'
            elif i == 1:
                html += f'<td class="second-col">{row[col]}</td>'
            else:
                html += f'<td>{row[col]}</td>'
        html += "</tr>"
    html += """
            </tbody>
        </table>
    </div>
    <script>
    function updateColumnWidths() {
        const firstCols = document.querySelectorAll('.first-col');
        const secondCols = document.querySelectorAll('.second-col');

        let maxFirstWidth = 0;
        firstCols.forEach(cell => {
            maxFirstWidth = Math.max(maxFirstWidth, cell.offsetWidth);
        });

        let maxSecondWidth = 0;
        secondCols.forEach(cell => {
            maxSecondWidth = Math.max(maxSecondWidth, cell.offsetWidth);
        });

        firstCols.forEach(cell => {
            cell.style.minWidth = maxFirstWidth + 'px';
        });

        secondCols.forEach(cell => {
            cell.style.minWidth = maxSecondWidth + 'px';
            cell.style.left = (maxFirstWidth + 14) + 'px'; // Add a 1px buffer
        });
    }

    window.addEventListener('load', updateColumnWidths);
    window.addEventListener('resize', updateColumnWidths);
    </script>
    """
    return html


tab1, tab2, tab3 = st.tabs(["Filter", "Update", "Alter"])
with tab1:
    if st.session_state.df is not None:
        st.subheader("Original Dataset")
        st.write(df.dtypes)
        if 'RAW' not in st.session_state.df.columns:    
            html_table = create_html_table_with_frozen_columns(st.session_state.df)
            components.html(html_table, height=500)
            #st.markdown(html_table, unsafe_allow_html=True)
            #st.write(st.session_state.df)
            # st.write("");
            # st.write("");
            if st.button("Add Filter"):
                st.session_state.filters.append({"column": "", "value": "", "operator": ""})
            with st.container(border=True):
                for i, filter in enumerate(st.session_state.filters):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        filter['column'] = st.selectbox(f"Select Column {i+1}", options=st.session_state.filter_cols, key=f"select_col_{i}")
                    with col2:
                        column_name = filter['column']  # Get column name from the filter dictionary
            
                        if column_name and column_name in st.session_state.df.columns: #check to avoid errors if column_name is empty or not in df.
                          column_series = st.session_state.df[column_name]  # Access the column data (Pandas Series)
                          if pd.api.types.is_integer_dtype(column_series):
                              filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
                          elif pd.api.types.is_float_dtype(column_series):
                              filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
                          elif pd.api.types.is_object_dtype(column_series):
                              filter['operator'] = st.selectbox(f"Operator {i+1}", options=["contains", "starts with", "ends with", "equals"], key=f"operator_{i}")
                          elif pd.api.types.is_datetime64_any_dtype(pd.to_datetime(column_series, errors='coerce')):
                              filter['operator'] = st.selectbox(f"Operator {i+1}", options=["start date", "end date"], key=f"operator_{i}")
                          else:
                              filter['operator'] = st.selectbox(f"Operator {i+1}", options=["==", "!=", ">", "<", ">=", "<="], key=f"operator_{i}")
                    with col3:
                        filter['value'] = st.text_input(f"Enter value to filter by for column {filter['column']}", key=f"filter_value_{i}")
                        if i<len(st.session_state.filters)-1:
                            st.divider()
                        
    if st.session_state.filters != [] and st.button("Apply Filters"):
        if isinstance(st.session_state.df, pd.DataFrame):
            filtered_df = st.session_state.df.copy()
        else:
            st.write("Error: st.session_state.df is not a DataFrame.")
        
        
        for i,filter in enumerate(st.session_state.filters):
            column = filter['column']
            operator = filter['operator']
            value = filter['value']
    
            if column and value:
                if pd.api.types.is_integer_dtype(filtered_df[column]):
                    try:
                        value = int(value)
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
                    except ValueError:
                        st.error(f"Invalid integer value for column {column}")
    
                elif pd.api.types.is_float_dtype(filtered_df[column]):
                    try:
                        value = float(value)
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
                    except ValueError:
                        st.error(f"Invalid float value for column {column}")
                
                elif pd.api.types.is_datetime64_any_dtype(filtered_df[column]):
                    try:
                        st.write(pd.api.types.is_datetime64_any_dtype(filtered_df[column]))
                        if operator in ["start date", "end date", "between dates"]:
                            if operator == "between dates":
                                start_date, end_date = value.split(',')
                                start_date = pd.to_datetime(start_date.strip())
                                end_date = pd.to_datetime(end_date.strip())
                                filtered_df = filtered_df[(filtered_df[column] >= start_date) & (filtered_df[column] <= end_date)]
                            elif operator == "start date":
                                value = pd.to_datetime(value)
                                filtered_df = filtered_df[filtered_df[column] >= value]
                            elif operator == "end date":
                                value = pd.to_datetime(value)
                                filtered_df = filtered_df[filtered_df[column] <= value]
                        else:
                            value = pd.to_datetime(value)
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
    
                    except ValueError:
                        st.error(f"Invalid date value for column {column}")
    
                elif pd.api.types.is_object_dtype(filtered_df[column]):
                    if operator == "contains":
                        filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False, na=False)]
                    elif operator == "starts with":
                        filtered_df = filtered_df[filtered_df[column].str.startswith(value, na=False)]
                    elif operator == "ends with":
                        filtered_df = filtered_df[filtered_df[column].str.endswith(value, na=False)]
                    elif operator == "equals":
                        filtered_df = filtered_df[filtered_df[column] == value]
                    elif operator == "==":
                        filtered_df = filtered_df[filtered_df[column] == value]
                    elif operator == "!=":
                        filtered_df = filtered_df[filtered_df[column] != value]
            
        st.divider()
        st.subheader("Filtered Dataset")
        st.write(filtered_df)
        st.session_state.filtered_df=filtered_df
        downloaded_file = filtered_df.to_csv(index=False).encode()  # Convert to CSV and encode to bytes
        # Create the download button
        st.download_button(
            label="Download",
            data=downloaded_file,
            file_name='my_data.csv',
            mime='text/csv'
        )

@st.dialog("Are you make these changes in Final Table?")
def main_table_update(update_column,unique_column,row_index,value):
    st.session_state.update_query = f"""
                UPDATE {st.session_state.selected_db}.{st.session_state.selected_schema}.{st.session_state.selected_table}
                SET {update_column} = '{value}'
                WHERE {unique_column} = '{row_index}'
            """
    st.code(st.session_state.update_query, language="sql")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Yes"):
            try:
                # **Execute the UPDATE query in Snowflake**
                # Replace this with your actual Snowflake execution code
                session.sql(st.session_state.update_query).collect()
                st.success("Snowflake table updated!")
            except Exception as e:
                st.error(f"Error updating Snowflake: {e}")
            finally:  
                st.rerun()  # Rerun to clear the dialog

    with col2:
        if st.button("No"):  
            st.rerun()  # Rerun to clear the dialog
        
        
        
with tab2:
    flag=0
    if st.session_state.filtered_df is not None and not st.session_state.filtered_df.empty:
        copy_df=st.session_state.filtered_df.copy()
        flag=1
    else:
        copy_df=st.session_state.df.copy()
    st.write(copy_df)
    unique_column = copy_df.columns[0]
    row_index = st.selectbox("Select a row:", copy_df[unique_column])
    selected_row = copy_df[copy_df[unique_column] == row_index]

    # Display the selected row
    st.write(selected_row)

    if row_index is not None:
        with st.container(border=True):  # Assuming you have a way to style the container
            st.subheader("Update Values")
            # Display values as read-only text inputs
            # for col in st.session_state.df.columns:
            st.text_input(f"Data:", value=str(selected_row[unique_column].values[0]),
                         disabled=True)

            # Determine the column to update
            update_column = st.selectbox("Select column to update", st.session_state.df.columns)

            value = st.text_input("New Value:")

            if st.button('Update'):
                try:
                    # Update the DataFrame in session state
                    st.session_state.df.loc[st.session_state.df[unique_column] == row_index, update_column] = value
                    # if st.session_state.filtered_df is not None and not st.session_state.filtered_df.empty:
                    #     st.session_state.filtered_df.loc[st.session_state.df[unique_column] == row_index, update_column] = value
                    if flag==1:
                        update_filtered_df()  # Update filtered_df after df changes
                    st.success("DataFrame updated!")
                    # Display the updated dataframe.
                    st.subheader("Updated Dataframe")
                    main_table_update(update_column,unique_column,row_index,value)
                    st.write(st.session_state.df)
                    downloaded_file = filtered_df.to_csv(index=False).encode()  # Convert to CSV and encode to bytes
                    # Create the download button
                    st.download_button(
                        label="Download",
                        data=downloaded_file,
                        file_name='my_data.csv',
                        mime='text/csv'
                    )
                except Exception as e:
                    st.error(f"An error occurred during update: {e}")
    else:
        st.write(st.session_state.df)

with tab3:
    @st.dialog("Are you sure to update this Table")
    def update():
        if st.button("Submit"):
            st.session_state.df=st.session_state.editor  # Update filtered_df after df changes
            st.rerun()
        
    if st.session_state.df is not None and not st.session_state.df.empty:
        # DataFrame is not None and not empty 
        st.session_state.editor = st.data_editor(st.session_state.df)  # Use df here
        if st.button("Confirm"):
            update()
    else:
        st.write(st.session_state.df)