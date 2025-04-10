def create_html_table_with_frozen_column(df):
    html = """
    <style>
    .table-container {
        width: 100%; /* Or a specific width if you want to limit horizontal size as well */
        overflow-x: auto; /* Enable horizontal scrolling if needed */
        max-height: 500px; /* Limit the vertical size of the table */
        overflow-y: auto; /* Enable vertical scrolling */
    }
    table {
        width: max-content;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
        white-space: nowrap;
    }
    .frozen {
        position: sticky;
        left: 0;
        background-color: rgba(0,0,0,0.5);
        z-index: 1; /* Ensure the frozen column is on top */
    }
    .frozen-cell {
    border-left: 2px solid rgba(0,0,0,3);
    border-right: 2px solid rgba(0,0,0,3) !important; /* Increased thickness and made it red */
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    }
    th, td { /* Style for all cells to make borders more visible */
        border: 1px solid black;
    }
    </style>
    <div class="table-container">
    <table>
        <thead>
            <tr>
    """
    for col in df.columns:
        if col == df.columns[0]:
            html += f"<th class='frozen'>{col}</th>"
        else:
            html += f"<th>{col}</th>"
    html += """
            </tr>
        </thead>
        <tbody>
    """
    for index, row in df.iterrows():
        html += "<tr>"
        for i, col in enumerate(df.columns):
            if col == df.columns[0]:
                html += f"<td class='frozen frozen-cell'>{row[col]}</td>"
            else:
                html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += """
        </tbody>
    </table>
    </div>
    """
    return html