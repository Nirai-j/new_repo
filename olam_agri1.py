import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from snowflake.snowpark.context import get_active_session
# from datetime import datetime
# import numpy as np
# from logo_generator import render_image
from streamlit_extras.stylable_container import stylable_container
# URL = """wood_test/Olam Agri Logo.png"""
# add_logo(URL, height=60)
# --S_8348SF8V7PN08X (stage name)
# render_image('Olam Agri Logo.png')
# with stylable_container(
#     key="footer_container",
#     css_styles="""
#     {
#         padding-top: 50px;
#         box-sizing: border-box;

#         .element-container {
#             height: 100px;
#             display: flex;
#             color: #ffffff;
#             text-align: center;
#             align-items: center;
#             background-color: #0054a3;

#             a {
#                 color: #ffffff;
#             }
#         }
#     }
#         """,
# ):
#     st.write("For more information, visit www.snowflake.com")
st.set_page_config(layout="wide")

def set_background():
    gradient=f"""linear-gradient(225deg, #FFFFFFff, #FFFBF8ff, #FFF8F0ff, #FFF4E9ff, #FFF0E2ff, #FFEDDAff, #FFE9D3ff)"""
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

# Apply the fun pink gradient background
set_background()
st.markdown(
    """
    <style>
    .stApp {
        background-image: {gradient};
        background-attachment: fixed;
        padding-left: 700px;
        padding-right: 700px;
        max-width: 1500px;
        margin: 0 auto;
    }
    div.stDownloadButton > button:first-child {
        background-color: #FF9900; /* Deeper orange color */
        color: #333; /* Dark gray text for better contrast */
        border: 1px solid #FFC107; /* Slightly darker orange border */
        border-radius: 25px; /* Rounded buttons */
        padding: 10px 25px;
        font-weight: bold;
        # background-color: #FFA07A; /* A vibrant orange color */
        # border: none;
        # padding: 10px 20px;
        # font-size: 16px;
        # font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }
    div.stDownloadButton > button:hover {
        background-color: #FF8C00; /* Even deeper orange hover color */
        color: white;
        border-color: #FF6F47;
        #background-color: #FFC107; /* A slightly darker orange color on hover */
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.4);
        transform: translateY(-2px);
    }

    .stSelectbox > div > div > div {
        outline: none;
        background-color: white; /* Orange background */
        color: #333; /* Dark text color */
        border: 2.2px solid #FF9900; /* Orange border */
        border-radius: 5px;
        padding: 8px;
    }
    
    .stSelectbox select:focus,
    .stSelectbox select:active {
        outline: none;
        border-color: #FFA07A; /* Darker orange border on focus */
        box-shadow: 0 0 0 0.2rem rgba(255, 153, 7, 0.25); /* Orange accent color shadow */
    }
    
    .stFileUploader {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #fff;
    }
      
      .stFileUploader label {
        font-size: 16px;
        color: #666;
    }
    .stselectbox div > li.st-e1:hover {
      background-color: #f7f7f7; /* Change this to your desired hover color */
    }
    .stFileUploader button[kind="secondary"] {
      border-radius: 10px;
      width: 120px;
      background-color: #000; /* Black background */
      color: #FF8C00; /* Orange text */
      border-color: #333;
      box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.4);
      transform: translateY(-2px);
      
    }

    .stFileUploader button[kind="secondary"]:hover {
      background-color: #FF8C00; /* Vibrant orange on hover */
      color: #ffffff; /* Black text on hover */ 
      box-shadow: 0px 5px 15px rgba(0,0,0, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        background-color: white;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        white-space: nowrap;
    }
    th {
        background-color: #FF8F5C;
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
    
# def create_html_table_with_frozen_columns(df):
#     html = """
#     <style>
#     .table-container {
#         width: 100%;
#         overflow-x: auto;
#         max-height: 300px;
#         overflow-y: auto;
#     }
#     table {
#         width: max-content;
#         border-collapse: collapse;
#         background-color: white;
#     }
#     th, td {
#         border: 1px solid black;
#         padding: 8px;
#         text-align: left;
#         white-space: nowrap;
#     }
#     thead {
#         background-color: #FF8F5C;
#         color: black;
#         font-weight: bold;
#     }
#     .first-col {
#         position: sticky;
#         left: 0;
#         z-index: 10;
#         min-width: 0;
#     }
#     .second-col {
#         position: sticky;
#         left: 0;
#         z-index: 9;
#         min-width: 0;
#     }
#     th.first-col {
#         z-index: 12;
#         background-color: #FF8F5C;
#     }
#     th.second-col {
#         z-index: 11;
#         background-color: #FF8F5C;
#     }
#     th:hover {
#         background-color: rgba(0,0,0,0.1);
#     }
#     td:hover{
#         background-color: rgba(0,0,0,0.1);
#     }
#     .frozen-cell {
#         border-left: 2px solid rgba(0,0,0,3);
#         border-right: 2px solid rgba(0,0,0,3) !important;
#         box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
#     }
#     th, td {
#         border: 1px solid black;
#     }
#     </style>
#     <div class="table-container">
#         <table id="dataTable">
#             <thead>
#                 <tr>
#     """
#     for i, col in enumerate(df.columns):
#         if i == 0:
#             html += f'<th class="first-col">{col}</th>'
#         elif i == 1:
#             html += f'<th class="second-col">{col}</th>'
#         else:
#             html += f'<th>{col}</th>'
#     html += """
#                 </tr>
#             </thead>
#             <tbody>
#     """
#     for _, row in df.iterrows():
#         html += "<tr>"
#         for i, col in enumerate(df.columns):
#             if i == 0:
#                 html += f'<td class="first-col">{row[col]}</td>'
#             elif i == 1:
#                 html += f'<td class="second-col">{row[col]}</td>'
#             else:
#                 html += f'<td>{row[col]}</td>'
#         html += "</tr>"
#     html += """
#             </tbody>
#         </table>
#     </div>
#     <script>
#     function updateColumnWidths() {
#         const firstCols = document.querySelectorAll('.first-col');
#         const secondCols = document.querySelectorAll('.second-col');

#         let maxFirstWidth = 0;
#         firstCols.forEach(cell => {
#             maxFirstWidth = Math.max(maxFirstWidth, cell.offsetWidth);
#         });

#         let maxSecondWidth = 0;
#         secondCols.forEach(cell => {
#             maxSecondWidth = Math.max(maxSecondWidth, cell.offsetWidth);
#         });

#         firstCols.forEach(cell => {
#             cell.style.minWidth = maxFirstWidth + 'px';
#         });

#         secondCols.forEach(cell => {
#             cell.style.minWidth = maxSecondWidth + 'px';
#             cell.style.left = (maxFirstWidth + 1) + 'px';
#         });
#     }

#     window.addEventListener('load', updateColumnWidths);
#     window.addEventListener('resize', updateColumnWidths);
#     </script>
#     """
#     return html

card_style = """
    {
        border: 1px groove #52546a;
        border-radius: 20px;
        background-color: white;
        padding-left: 25px;
        padding-top: 10px;
        padding-bottom: 10px;
        box-shadow: -6px 8px 20px 1px #00000052;
        height: 200px; /* fixed height */
        min-height: 125px; /* ensure minimum height is applied */
        max-height: 200px; 
        overflow: hidden; /* hide any overflowing content */
    }
"""
with stylable_container("Header",css_styles=
    """
      {
        border: 2.2px groove #52546a;
        border-radius: 6px;
        box-shadow: -6px 8px 20px 1px #00000052;
        background-color: white;
        .element-container {
            height: 156px;
            #height: 150px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom:0px;
            margin-top: -5.2em;
            margin-bottom: -5.8px;
            # margin-top: -4em;
            # margin-bottom: 0px;
            overflow: hidden;
       }
    """
        ):
    st.markdown(f"""
        <img src="https://i.imgur.com/Siru7FE.png" style="width:99.82%;height:100%;object-fit:contain">  
# """, unsafe_allow_html=True)


# with stylable_container("Header",css_styles=
#     """
#       { 
#         border: 1px groove #52546a;
#         border-radius: 20px;
#         box-shadow: -6px 8px 20px 1px #00000052;
#         background-color: white;
#         .element-container {
#             height: 100px;
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#             padding-left: 20px;
#             padding-right: 20px;
#             padding-botton:8px;
#             margin-top: -3.2em;
#             overflow: hidden;
#        }
#     """
#         ):
#     logo_container,info_container = st.columns([4, 2])
#     with logo_container:
#         st.image('https://lagosfoodbank.org/wp-content/uploads/2022/10/Olam-Agri-logo.png', width=150)
#     with info_container:
#         more_info_text = st.write("For more information, visit www.snowflake.com")
        
col1,col2=st.columns([1.2,1.2])

with col1:
    with stylable_container("Card1", css_styles=card_style):
        "**Card 1**"
        "This is an example of a short card."

with col2:
    with stylable_container("Card2", css_styles=
    card_style):
        st.metric("New York", "19.8M", "367K", help="Population growth")

# st.image('Olam Agri Logo.png',width= 200)

session = get_active_session()

st.title('Download/Upload')

# Define options
options = ["RPT_STREAMLIT.VAR_POSITION_TEMP", "RAW_WEBAPP.PRODUCT_MASTER_CP_FC"]

# Create a selectbox to choose an option
option = st.selectbox("Choose an option", options)

# Generate data based on the selected option
data = session.sql(f'select * from {option}').to_pandas()

# If data is not None, create a DataFrame and display it
if data is not None:
    df = data
    html_table = create_html_table_with_frozen_columns(df.head(5))
    components.html(html_table, height=500)
    #st.markdown(html_table, unsafe_allow_html=True)
    
    
    # Create a download button to download the DataFrame as a CSV file
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode("utf-8")

    csv = convert_df(df)
    st.write("")
    col1, col2 = st.columns([9.5, 1])
    with col2:
        st.download_button(
            label="Download Data",
            data=csv,
            file_name=f"{option}.csv",
            mime="text/csv"
        )


# Create an uploader to upload the updated CSV file
st.subheader("Upload Uploaded file")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file and update the data
    df_uploaded = pd.read_csv(uploaded_file)
    html_table = create_html_table_with_frozen_column(df_uploaded)
    st.markdown(html_table, unsafe_allow_html=True)
    #st.write(df_uploaded)
    #snowparkDf=session.write_pandas(df_uploaded,f"{option}",auto_create_table = True, overwrite=True)
    # st.write(snowparkDf)