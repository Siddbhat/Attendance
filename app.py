import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
import mysql.connector
import pandas as pd
import dash_core_components as dcc
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
dummy_trigger = html.Div(id='dummy-trigger', style={'display': 'none'})
# Create a MySQL database connection
db_config = {
    "host": 'localhost',
    "user": 'root',
    "password": 'root',
    "database": 'vector',
}
 
 
# Styling for the admin page
admin_page_style = {
    'background-color': '#f4f4f4',
    'border-radius': '10px',
    'border': '1px solid #ccc',
    'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'padding': '20px',
    'color': 'green',
    'margin-bottom':"10px",
}
 
search_input_style = {
    'background-color': 'white',
    'border-radius': '5px',
    'border': '1px solid #ccc',
    'box-shadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
    'padding': '10px',
    'margin-bottom':"10px",
    'margin-top':"10px"
}
 
search_button_style = {
    'background-color': 'green',
    'color': 'white',
    'border': 'none',
    'border-radius': '5px',
    'padding': '10px',
    'cursor': 'pointer',
    'margin-right': '10px',
    'fontWeight': '500',
    'fontSize': '14px',
    'margin-left':'10px',
    'margin-bottom':'10px'
}
 
search_button_style1 = {
    'width':'100px',
    'background-color': 'green',
    'color': 'white',
    'border': 'none',
    'border-radius': '5px',
    'padding': '10px',
    'cursor': 'pointer',
    'margin-right': '10px',
    'fontWeight': '500',
    'fontSize': '17px',
    'margin-left':'50px'
}
 
employee_info_style = {
    'margin-top': '20px',
    'font-weight': 'bold',
}
 
timesheet_table_style = {
    'margin-top': '20px',
}
 
signin_layout = html.Div([
    html.Div([
        html.Button('Employee Login', id='admin-button', n_clicks=0, className='button',style=search_button_style),
        html.Button('Admin Login', id='user-button', n_clicks=0, className='button',style=search_button_style),
    ], className='container'),
 
    html.Div(id='button-output')
],style=admin_page_style)
 
admin_login_layout = html.Div(
    dbc.Container(
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Admin Login", style={'color': 'green', "margin-left": "70px"}),
                        dbc.Input(type="text", id="username-input", placeholder="Admin Username",
                                  style={'margin-bottom': '10px'}),
                        dbc.Input(type="password", id="password-input", placeholder="Password",
                                  style={'margin-bottom': '20px'}),
                        dbc.Row([dbc.Button("Login", id="login-button",className='button',style=search_button_style1), ],
                                style={'width': '250px', "display": "flex", "margin-left": "40px"})
                    ],
                    className="p-5",
                    style=admin_page_style  # Apply the admin page style to the login box
                ),
                width={"size": 4, "offset": 4},
                className="mt-5",
            )
        ),
    )
)
 
 
change_admin_password_layout = dbc.Container(
    [
        html.H2("Change Admin Password", style=admin_page_style),
        dbc.Input(id="admin-username-input", type="text", placeholder="Admin Username", style=search_input_style),
        dbc.Input(id="admin-old-password-input", type="password", placeholder="Old Password", style=search_input_style),
        dbc.Input(id="admin-new-password-input", type="password", placeholder="New Password", style=search_input_style),
        dbc.Button("Change Admin Password", id="change-admin-password-submit-button", color="success", className="mt-3",style=search_button_style),
        dbc.Button("Back", id="back-button-password", color="success", className="mt-3",style=search_button_style),
        html.Div(id="admin-password-change-info", style=employee_info_style)
    ],
    style=admin_page_style,
    className="p-5",
)
 
download_excel_button = dbc.Button(
    "DOWNLOAD",
    id="download-excel-button",
    color="primary",
    className="mt-3",
    style=search_button_style
)
 
# def fetch_employee_ids():
#     # Replace with your MySQL connection parameters
   
#     connection = mysql.connector.connect(**db_config)
#     cursor = connection.cursor()
 
#     try:
#         # Execute the SQL query to fetch employee IDs
#         cursor.execute("SELECT emp_id FROM users ORDER BY emp_id ASC")
 
#         # Fetch all the rows and extract employee IDs into a list
#         employee_ids = [row[0] for row in cursor.fetchall()]
 
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
 
#     finally:
#         cursor.close()
#         connection.close()
 
#     return employee_ids
 
# employee_ids = fetch_employee_ids()
 
checklist = html.Div([
    
    html.Div([
        dcc.Checklist(
            id="search-input",
            options=[],
            value=[],
            labelStyle={'display': 'block', 'fontSize': '20px', 'margin': '10px'},
            style={'maxHeight': '100px', 'overflowY': 'auto', 'display': 'flex', 'flexWrap': 'wrap',
                   'fontSize': '17px', 'background-color': 'white', 'border-radius': '5px',
                   'border': '1px solid #ccc', 'box-shadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
                   'padding': '10px', 'margin': '5px'}
        ), dcc.Interval(id='interval-component', interval=180*1000, n_intervals=0),
    ]),
    dcc.Input(id='search-input1', type='text', placeholder='Search Employee ID',style=search_input_style),
    html.Button('Select', id='select-button',style=search_button_style),
    html.Button('Deselect', id='deselect-button', style=search_button_style),
])
 
@app.callback(Output('search-input', 'options'), Input('interval-component', 'n_intervals'))
def update_employee_ids(n):
    # Replace with your MySQL connection parameters
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
 
    try:
        # Execute the SQL query to fetch employee IDs
        cursor.execute("SELECT emp_id FROM users ORDER BY emp_id ASC")
 
        # Fetch all the rows and extract employee IDs into a list
        employee_ids = [row[0] for row in cursor.fetchall()]
 
    except mysql.connector.Error as err:
        print(f"Error: {err}")
 
    finally:
        cursor.close()
        connection.close()
    
    # Return the updated options for the checklist
    return [{'label': emp_id, 'value': emp_id} for emp_id in employee_ids]




admin_layout = dbc.Container(
    [  
        html.H2("Admin Page", style=admin_page_style),
    html.Div([
    checklist,
    dcc.DatePickerRange(
        id="date-range-input",
        start_date=None,
        end_date=None,
        display_format="YYYY-MM-DD",
    ),
    dbc.Button("SEARCH", id="search-button", color="primary", className="mt-3", style=search_button_style),
    dbc.Button("ADD EMP", id="add-emp-button", color="success", className="mt-3", style=search_button_style),
    dbc.Button("REMOVE EMP", id="remove-emp-button", color="danger", className="mt-3", style=search_button_style),
    dbc.Button("GIVE ACCESS", id="give-access-button", color="info", className="mt-3", style=search_button_style),
    dbc.Button("Leave history", id="leave-history-button", color="primary", className="mt-3", style=search_button_style),
    dbc.Button("CHANGE PASSWORD", id="change-admin-password-button", color="success", className="mt-3", style=search_button_style),
    download_excel_button,
    dbc.Button("Consolidate Download", id="consolidate-download-button", color="primary", className="mt-3", style=search_button_style),
],style=admin_page_style),
        html.Div(id="employee-info", style=employee_info_style),
        dash_table.DataTable(
            id="timesheet-table",
            columns=[
                {"name": "EmpID", "id": "EmpID"},
                {"name": "From Date", "id": "From Date"},
                {"name": "To Date", "id": "To Date"},
                {"name": "Total Hours", "id": "Total Hours"},
            ],
            style_table={'height': '400px', 'overflowY': 'auto'},
            data=[],
            style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#F7F7F7'},
            {'if': {'row_index': 'even', 'column_id': 'EmpID'}, 'backgroundColor': '#E2E2E2', 'cursor': 'pointer'}
        ],
        style_header={'backgroundColor': 'green', 'color': '#FFFFFF', 'fontWeight': 'bold'},
        style_cell={'padding': '10px', 'fontSize': '17px', 'textAlign': 'center'},
        style_data={'transition': 'background-color 0.3s'},
       
        )
    ],
    style=admin_page_style,
    className="p-5",
)

button_style2 = {
    'background-color': 'green',
    'color': '#FFFFFF',
    'border': 'none',
    'border-radius': '5px',
    'padding': '10px 20px',
    'cursor': 'pointer',
}
button_style3 = {
    'background-color': 'red',
    'color': '#FFFFFF',
    'border': 'none',
    'border-radius': '5px',
    'padding': '10px 20px',
    'cursor': 'pointer',
}
input_style = {
    'width': '100%',
    'padding': '10px',
    'margin-bottom': '10px',
    'border': '1px solid #D1D1D1',
    'border-radius': '5px',
}

label_style = {
    'font-weight': 'bold',
    'color': 'green',
}

header_style = {
    'background-color': 'green',
    'color': '#FFFFFF',
    'font-size': '20px',
    'text-align': 'center',
}

date_picker_style = {
    'width': '100%',
    'padding': '10px',
    'margin-bottom': '10px',
    'border': '1px solid #D1D1D1',
    'border-radius': '5px',
}

checklist_container_style = {
    'display': 'flex',
    'flex-direction': 'column',  # Display options in a column
    'align-items': 'flex-start',  # Align options to the left
}
checklist_container_style1 = {
    "width":"100%",
    'display': 'flex',
    'flex-direction': 'column',  # Display options in a column
    'align-items': 'flex-start',  # Align options to the left
}

# Define styles for checklist labels
checklist_label_style = { 
    "font-family":"sans-serif",
     'display': 'block', 
     'fontSize': '18px', 
     'margin': '10px' # Add some spacing between options
}

popup = dbc.Modal([
    dbc.ModalHeader("Consolidate Download",style=header_style),
    dbc.ModalBody([
        html.Div([
            html.Label("Employee ID",style=label_style),
            dcc.Input(id="emp-id-input", type="text", placeholder="Enter Employee ID",style=input_style),
        ]),
        html.Div([
            html.Label("Start Date",style=label_style),
            dcc.DatePickerSingle(id="start-date-input", display_format="YYYY-MM-DD",style=date_picker_style),
        ],style=checklist_container_style1),
        html.Div([
            html.Label("End Date",style=label_style),
            dcc.DatePickerSingle(id="end-date-input", display_format="YYYY-MM-DD",style=date_picker_style),
        ],style=checklist_container_style1),
        html.Div([
            dcc.Checklist(
                options=[
                    {"label": "Attendance Report", "value": "attendance"},
                    {"label": "Approved Leaves Report", "value": "approved_leaves"},
                    {"label": "Rejected Leaves Report", "value": "rejected_leaves"},
                ],
                id="report-checkboxes",
                style=checklist_container_style,  # Apply the container style
                inline=True,  # Maintain inline style for individual options
                labelStyle=checklist_label_style, 
            ),
        ]),
    ]),
    dbc.ModalFooter([
        dbc.Button("Download", id="download-consolidated-button", color="primary",style=button_style2),
        dbc.Button("Close", id="close-popup-button", color="red",style=button_style3),
    ]),
], id="popup",style=admin_page_style)

@app.callback(
    Output("popup", "is_open"),
    [Input("consolidate-download-button", "n_clicks"),
     Input("close-popup-button", "n_clicks")],
    State("popup", "is_open")
)
def toggle_popup(consolidate_clicks, close_clicks, is_open):
    if consolidate_clicks or close_clicks:
        return not is_open
    return is_open

import pandas as pd

# Function to generate and download reports
def generate_reports(employee_id, start_date, end_date, selected_reports):
    # Your database connection code
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    reports = []

    if 'attendance' in selected_reports:
        # Generate the attendance report and append it to the list
        cursor.execute(
            "SELECT * FROM employee_timesheet WHERE emp_id = %s AND date >= %s AND date <= %s",
            (employee_id, start_date, end_date)
        )
        attendance_data = cursor.fetchall()
        if attendance_data:
            df = pd.DataFrame(attendance_data, columns=[col[0] for col in cursor.description])
            df.to_excel('attendance_report.xlsx', index=False)
            reports.append(('attendance_report.xlsx', df))

    if 'approved_leaves' in selected_reports:
        # Generate the approved leaves report and append it to the list
        cursor.execute(
            "SELECT * FROM leavesapproved WHERE emp_id = %s AND from_date >= %s AND to_date <= %s",
            (employee_id, start_date, end_date)
        )
        approved_leaves_data = cursor.fetchall()
        if approved_leaves_data:
            df = pd.DataFrame(approved_leaves_data, columns=[col[0] for col in cursor.description])
            df.to_excel('approved_leaves_report.xlsx', index=False)
            reports.append(('approved_leaves_report.xlsx', df))

    if 'rejected_leaves' in selected_reports:
        # Generate the rejected leaves report and append it to the list
        cursor.execute(
            "SELECT * FROM pendingLeaves WHERE emp_id = %s AND from_date >= %s AND to_date <= %s",
            (employee_id, start_date, end_date)
        )
        rejected_leaves_data = cursor.fetchall()
        if rejected_leaves_data:
            df = pd.DataFrame(rejected_leaves_data, columns=[col[0] for col in cursor.description])
            df.to_excel('rejected_leaves_report.xlsx', index=False)
            reports.append(('rejected_leaves_report.xlsx', df))

    cursor.close()
    connection.close()

    # Return the list of reports
    return reports

Consolidated=dcc.Download(id="download-reports")
import tempfile
import zipfile
import os

@app.callback(
    Output("download-reports", "data"),
    [Input("download-consolidated-button", "n_clicks")],
    [
        State("emp-id-input", "value"),
        State("start-date-input", "date"),
        State("end-date-input", "date"),
        State("report-checkboxes", "value"),
    ],
)
def download_reports(n_clicks, emp_id, start_date, end_date, selected_reports):
    if n_clicks:
        reports = []

        if not emp_id and not start_date and not end_date:
            # No specific emp_id, start date, or end date provided, fetch data for all employees
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            if "attendance" in selected_reports:
                cursor.execute("SELECT * FROM employee_timesheet")
                attendance_data = cursor.fetchall()
                if attendance_data:
                    df = pd.DataFrame(attendance_data, columns=[col[0] for col in cursor.description])
                    df.to_excel('attendance_report.xlsx', index=False)
                    reports.append(('attendance_report.xlsx', df))

            if "approved_leaves" in selected_reports:
                cursor.execute("SELECT * FROM leavesapproved")
                approved_leaves_data = cursor.fetchall()
                if approved_leaves_data:
                    df = pd.DataFrame(approved_leaves_data, columns=[col[0] for col in cursor.description])
                    df.to_excel('approved_leaves_report.xlsx', index=False)
                    reports.append(('approved_leaves_report.xlsx', df))

            if "rejected_leaves" in selected_reports:
                cursor.execute("SELECT * FROM pendingLeaves")
                rejected_leaves_data = cursor.fetchall()
                if rejected_leaves_data:
                    df = pd.DataFrame(rejected_leaves_data, columns=[col[0] for col in cursor.description])
                    df.to_excel('rejected_leaves_report.xlsx', index=False)
                    reports.append(('rejected_leaves_report.xlsx', df))

            cursor.close()
            connection.close()
        elif not emp_id and start_date and end_date:
    # No specific emp_id, but start date and end date are provided, fetch data for all employees within the date range
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                if "attendance" in selected_reports:
                    cursor.execute("SELECT * FROM employee_timesheet WHERE date >= %s AND date <= %s", (start_date, end_date))
                    attendance_data = cursor.fetchall()
                    if attendance_data:
                        df = pd.DataFrame(attendance_data, columns=[col[0] for col in cursor.description])
                        df.to_excel('attendance_report.xlsx', index=False)
                        reports.append(('attendance_report.xlsx', df))

                if "approved_leaves" in selected_reports:
                    cursor.execute("SELECT * FROM leavesapproved WHERE from_date >= %s AND to_date <= %s", (start_date, end_date))
                    approved_leaves_data = cursor.fetchall()
                    if approved_leaves_data:
                        df = pd.DataFrame(approved_leaves_data, columns=[col[0] for col in cursor.description])
                        df.to_excel('approved_leaves_report.xlsx', index=False)
                        reports.append(('approved_leaves_report.xlsx', df))

                if "rejected_leaves" in selected_reports:
                    cursor.execute("SELECT * FROM pendingLeaves WHERE from_date >= %s AND to_date <= %s", (start_date, end_date))
                    rejected_leaves_data = cursor.fetchall()
                    if rejected_leaves_data:
                        df = pd.DataFrame(rejected_leaves_data, columns=[col[0] for col in cursor.description])
                        df.to_excel('rejected_leaves_report.xlsx', index=False)
                        reports.append(('rejected_leaves_report.xlsx', df))

                cursor.close()
                connection.close()
                
        else:
            # Emp_id, start date, and end date are provided, fetch data for the specified employee
            reports = generate_reports(emp_id, start_date, end_date, selected_reports)

        # Package the reports in a zip file and serve it for download
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as archive:
                for filename, data in reports:
                    # Write each report file to the zip archive
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as report_file:
                        data.to_excel(report_file, index=False)
                        # Append emp_id to the filename if available
                        if emp_id:
                            filename = f"{emp_id}_{filename}"
                        archive.write(report_file.name, arcname=filename)
        # Return the zip file data
        zip_file_name = "consolidated_report.zip"
        return dcc.send_file(tmp.name, zip_file_name)



def fetch_leave_records_data():
    # Replace with your own logic to fetch data from the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT emp_id, from_date, to_date, reason, description FROM leaverecords")
    data_from_database = cursor.fetchall()
    data = [{"emp_id": emp_id, "from_date": from_date, "to_date": to_date, "reason": reason, "description": description,"approve_button":"Approve","reject_button":"Reject"} for
            (emp_id, from_date, to_date, reason, description) in data_from_database]
    return data
 
# Fetch the data from the SQL table

def fetch_leaves_approved_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()    
 
    try:
        cursor.execute("SELECT emp_id, from_date, to_date, reason, description FROM leavesapproved")
        leaves_approved_data_from_db = cursor.fetchall()
 
        leaves_approved_data = []
        for row in leaves_approved_data_from_db:
            leaves_approved_data.append({
                "emp_id": row[0],
                "from_date": row[1],
                "to_date": row[2],
                "reason": row[3],
                "description": row[4],
            })
 
        return leaves_approved_data
 
    except mysql.connector.Error as err:
        print(f"Error: {err}")
 
    finally:
        cursor.close()
        connection.close()

def fetch_pending_leaves_data():
    try:
        connection = mysql.connector.connect(**db_config)  # Replace db_config with your database configuration
        cursor = connection.cursor(dictionary=True)

        # Define your SQL query to fetch data from the "pendingleaves" table
        query = "SELECT emp_id, from_date, to_date, reason, description FROM pendingleaves"

        cursor.execute(query)
        data = cursor.fetchall()

        return data
    except Exception as e:
        print(f"Error fetching pending leaves data: {e}")
    finally:
        cursor.close()
        connection.close()

import datetime
import calendar
current_year1 = datetime.datetime.now().year
options1 = [{'label': calendar.month_name[month], 'value': f'{current_year1}-{month:02}'} for month in range(1, 13)]
# Define your DataTable with the "Approve/Disapprove" column as a dropdown
leave_records_table = html.Div([dcc.Interval(
    id='table-update-interval',
    interval=10*1000,  # 10 seconds in milliseconds
    n_intervals=0
)
,      dcc.Interval(
        id="update-leaves-approved-interval",
        interval=30* 1000,  # Refresh "leaves-approved-table" every 2 seconds
        n_intervals=1   
    ),dcc.Interval(
        id="update-leaves-pending-interval",
        interval=30* 1000,  
        n_intervals=1   
    ),dbc.Button("Back", id="back-button-give-access", color="success", className="mt-3", style=search_button_style),
    html.Div([html.H2("Leaves Pending For Approval", style=admin_page_style),
    dbc.Button("Approve Leave", id="approve-leave", color="success", className="mt-3", style=search_button_style),
    dbc.Button("Reject Leave", id="reject-leave", color="success", className="mt-3", style=search_button_style),
    dash_table.DataTable(
        id="leave-records-table",
        columns=[
            {"name": "Employee ID", "id": "emp_id", "editable": False},
            {"name": "From Date", "id": "from_date", "editable": False},
            {"name": "To Date", "id": "to_date", "editable": False},
            {"name": "Reason", "id": "reason", "editable": False},
            {"name": "Description", "id": "description", "editable": False},
        ],
        data=fetch_leave_records_data(),
        row_selectable='single',
        editable=True,  # Set to editable to allow dropdowns
        style_table={'height': '400px', 'overflowY': 'auto', 'margin-bottom': '20px'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#F7F7F7'},
            {'if': {'row_index': 'even', 'column_id': 'emp_id'}, 'backgroundColor': '#E2E2E2', 'cursor': 'pointer'}
        ],
        style_header={'backgroundColor': 'green', 'color': '#FFFFFF', 'fontWeight': 'bold'},
        style_cell={'padding': '10px', 'fontSize': '17px', 'textAlign': 'center'},
        style_data={'transition': 'background-color 0.3s'},
    ),
    html.Div(id='output'),
],style=admin_page_style)
,html.Div([ html.H2("Leaves Approved", style=admin_page_style),html.Div([
    dcc.Input(id="search-emp-id", type="text", placeholder="Search by Employee ID",style=search_input_style)
])
,dbc.Button("Download Leave Report", id="download-excel-button1", n_clicks=0, style=search_button_style),dcc.Dropdown(
    id="select-month",
    options=options1,
    placeholder="Select a Month",style=search_input_style
)
,html.Div([
        dash_table.DataTable(
            id="leaves-approved-table",
            columns=[
                {"name": "Employee ID", "id": "emp_id"},
                {"name": "From Date", "id": "from_date"},
                {"name": "To Date", "id": "to_date"},
                {"name": "Reason", "id": "reason"},
                {"name": "Description", "id": "description"},
            ],
            data=fetch_leaves_approved_data(),
            editable=False,
            style_table={'height': '400px', 'overflowY': 'auto', 'margin-bottom': '20px'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#F7F7F7'},
                {'if': {'row_index': 'even', 'column_id': 'emp_id'}, 'backgroundColor': '#E2E2E2', 'cursor': 'pointer'}
            ],
            style_header={'backgroundColor': 'green', 'color': '#FFFFFF', 'fontWeight': 'bold'},
            style_cell={'padding': '10px', 'fontSize': '17px', 'textAlign': 'center'},
            style_data={'transition': 'background-color 0.3s'},
        ),
    ])],style=admin_page_style), html.Div([html.H2("Leaves Rejected", style=admin_page_style),
    dash_table.DataTable(
        id="pending-leaves-table",
        columns=[
            {"name": "Employee ID", "id": "emp_id"},
            {"name": "From Date", "id": "from_date"},
            {"name": "To Date", "id": "to_date"},
            {"name": "Reason", "id": "reason"},
            {"name": "Description", "id": "description"},
        ],
        data=fetch_pending_leaves_data(),  # Implement the function to fetch pendingleaves data
        editable=False,
        style_table={'height': '400px', 'overflowY': 'auto', 'margin-bottom': '20px'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#F7F7F7'},
            {'if': {'row_index': 'even', 'column_id': 'emp_id'}, 'backgroundColor': '#E2E2E2', 'cursor': 'pointer'}
        ],
        style_header={'backgroundColor': 'green', 'color': '#FFFFFF', 'fontWeight': 'bold'},
        style_cell={'padding': '10px', 'fontSize': '17px', 'textAlign': 'center'},
        style_data={'transition': 'background-color 0.3s'},
    )],style=admin_page_style),],style=admin_page_style),
 
 
download_component1 = dcc.Download(id="download-excel1")
 
import io
import pandas as pd
from dash.dash import no_update
import os
 
@app.callback(
    Output("download-excel1", "data"),
    Input("download-excel-button1", "n_clicks"),
    State("leaves-approved-table", "data")
)
def download_data_to_excel(n_clicks, table_data):
    if n_clicks:
        if table_data:
            df = pd.DataFrame(table_data)
 
            default_file_name = "Delta_employee_Leave_report.xlsx"
            file_name = default_file_name
            path_to_folder = "C:/Users/aksha/Desktop/DELTA_ATTENDANCE_REPORT"
 
            # Check if the folder exists, create it if not
            if not os.path.exists(path_to_folder):
                os.makedirs(path_to_folder)
 
            file_path = os.path.join(path_to_folder, file_name)
            df.to_excel(file_path, index=False)
            return dcc.send_file(file_path)
        else:
            raise PreventUpdate  # No data to download
    else:
        raise PreventUpdate  # Button has not been clicked
 
 
           
 
@app.callback(
    Output("pending-leaves-table", "data"),
    Input("update-leaves-pending-interval", "n_intervals")
)
def update_pending_leaves_table(n_intervals):
    if n_intervals:
        new_pending_leaves_data = fetch_pending_leaves_data()

        if new_pending_leaves_data:
            return new_pending_leaves_data

    # If no new data or not an interval update, return the current data
    return dash.callback_context.outputs[0].data



@app.callback(
    Output("leaves-approved-table", "data"),
    [Input("search-emp-id", "value"),
     Input("select-month", "value"),
     Input("update-leaves-approved-interval", "n_intervals")],
    State("leaves-approved-table", "data")
)
def update_leaves_approved_table(search_value, selected_month, n_intervals, current_data):
    leaves_approved_data = fetch_leaves_approved_data()  # Assuming you have defined this function

    if search_value:
        # Filter the data based on the search input
        leaves_approved_data = [record for record in leaves_approved_data if search_value in str(record["emp_id"])]

    if selected_month:
        # Filter the data based on the selected month
        leaves_approved_data = [record for record in leaves_approved_data if record["from_date"].startswith(selected_month)]

    if n_intervals:
        new_leaves_approved_data = fetch_leaves_approved_data()  # Assuming you have defined this function
        if not current_data:
            # If the table is empty, return the new data directly
            return new_leaves_approved_data
        else:
            # Append the new data to the existing data
            leaves_approved_data += new_leaves_approved_data

    return leaves_approved_data

 

@app.callback(
    Output('leave-records-table', 'data'),
    Input('table-update-interval', 'n_intervals')
)
def update_table_data(n_intervals):
    data = fetch_leave_records_data()  # Replace with your data retrieval function
    return data

@app.callback(
    Output('output', 'children'),
    Input('approve-leave', 'n_clicks'),
    Input('reject-leave', 'n_clicks'),
    State('leave-records-table', 'selected_rows'),
    State('leave-records-table', 'data')
)
def update_leave_status(approve_n_clicks, reject_n_clicks, selected_rows, data):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if selected_rows:
            selected_row = data[selected_rows[0]]
            emp_id = selected_row['emp_id']
            from_date = selected_row['from_date']
            to_date = selected_row['to_date']
            reason = selected_row['reason']
            description = selected_row['description']
            if button_id == 'approve-leave':
                # Move data to "leavesapproved" table
                insert_into_leavesapproved(emp_id, from_date, to_date, reason, description)
            elif button_id == 'reject-leave':
                # Move data to "pendingleaves" table
                insert_into_pendingleaves(emp_id, from_date, to_date, reason, description)
            # Remove the entry from the current table
            data.pop(selected_rows[0])
            return "Leave status updated successfully."
    return ""

# Your database insert functions
def insert_into_pendingleaves(emp_id, from_date, to_date, reason, description):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    insert_query = "INSERT INTO pendingleaves (emp_id, from_date, to_date, reason, description) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (emp_id, from_date, to_date, reason, description))
    delete_query = "DELETE FROM leaverecords WHERE emp_id = %s AND from_date = %s AND to_date = %s"
    cursor.execute(delete_query, (emp_id, from_date, to_date))
    connection.commit()
    connection.close()

def insert_into_leavesapproved(emp_id, from_date, to_date, reason, description):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    insert_query = "INSERT INTO leavesapproved (emp_id, from_date, to_date, reason, description) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (emp_id, from_date, to_date, reason, description))
    delete_query = "DELETE FROM leaverecords WHERE emp_id = %s AND from_date = %s AND to_date = %s"
    cursor.execute(delete_query, (emp_id, from_date, to_date))
    connection.commit()
    connection.close()



@app.callback(
    Output('search-input', 'value'),
    Input('select-button', 'n_clicks'),
    Input('deselect-button', 'n_clicks'),  # Add a Deselect button input
    State('search-input1', 'value'),
    State('search-input', 'value')
)
def select_or_deselect_employee(select_button_clicks, deselect_button_clicks, search_input1, selected_checkboxes):
    ctx = dash.callback_context  # Get the callback context to identify the triggered input
   
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]
       
        if prop_id == 'select-button' and search_input1:
            entered_emp_id = search_input1
            selected_checkboxes.append(entered_emp_id)
        elif prop_id == 'deselect-button':
            if search_input1:  # Deselect a specific employee if an ID is entered
                entered_emp_id = search_input1
                if entered_emp_id in selected_checkboxes:
                    selected_checkboxes.remove(entered_emp_id)
            else:  # Deselect all employees if no ID is entered
                selected_checkboxes = []
 
    return selected_checkboxes
  

import os 
@app.callback(
    Output("download-excel", "data"),
    Input("download-excel-button", "n_clicks"),
    Input("timesheet-table", "data"),
    State("search-input", "value"),
   
)
def download_excel_report(n_clicks, table_data, emp_id):
    if n_clicks:
        timesheet_df = pd.DataFrame(table_data)
        if emp_id is None:
            default_file_name = "Delta_employee_attendance.xlsx"
            file_name = default_file_name
        else:
            file_name = f"{emp_id}_attendance_report.xlsx"
 
        path_to_folder = "C:/Users/aksha/Desktop/DELTA_ATTENDANCE_REPORT"
        file_path = os.path.join(path_to_folder, file_name)
 
        timesheet_df.to_excel(file_path, index=False)
 
        return dcc.send_file(file_path)
    else:
        raise PreventUpdate
 
 
registration_layout = dbc.Container(
    [
        html.H2("Register Employee", style=admin_page_style),
        dbc.Input(id="emp-id-input", type="text", placeholder="Employee ID", style=search_input_style),
        dbc.Input(id="emp-name-input", type="text", placeholder="Employee Name", style=search_input_style),
        dbc.Input(id="emp-password-input", type="password", placeholder="Employee Password", style=search_input_style),
        dbc.Button("Register", id="register-button", color="success", className="mt-3", style=search_button_style),
        dbc.Button("Back", id="back-button-registration", color="success", className="mt-3",style=search_button_style),
        html.Div(id="registration-info", style=employee_info_style)
    ],
    style=admin_page_style,
    className="p-5",
)
 
# Create a new layout for the "Give Access" feature
 
 
give_access_layout = dbc.Container(
    [
        html.H2("Give Access", style=admin_page_style),
        dbc.Input(id="give-access-emp-id", type="text", placeholder="Employee ID", style=search_input_style),
        dcc.DatePickerRange(
            id="give-access-date-range",
            start_date=None,
            end_date=None,
            display_format="YYYY-MM-DD",
            style=search_input_style
        ),
        dbc.Button("Submit", id="submit-give-access-button", color="info", className="mt-3", style=search_button_style),
        dbc.Button("Back", id="back-button-give-access", color="success", className="mt-3", style=search_button_style),
        html.Div(id="give-access-info", style=employee_info_style)
    ],
    style=admin_page_style,
    className="p-5",
)
 
 
# Callback to handle changing the admin login details
@app.callback(
    Output("admin-password-change-info", "children"),
    Input("change-admin-password-submit-button", "n_clicks"),
    State("admin-username-input", "value"),
    State("admin-old-password-input", "value"),
    State("admin-new-password-input", "value"),
   
)
def change_admin_password(change_password_clicks, admin_username, old_password, new_password):
    if change_password_clicks and admin_username and old_password and new_password:
        # Check if the old password matches
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM admin WHERE admin_id = %s", (admin_username,))
        stored_password = cursor.fetchone()
 
        if not stored_password:
            return "Admin username not found."
 
        stored_password = stored_password[0]
 
        if old_password == stored_password:
            # Update the password in the database
            cursor.execute("UPDATE admin SET password = %s WHERE admin_id = %s", (new_password, admin_username))
            connection.commit()
            connection.close()
            return "Admin password changed successfully."
        else:
            return "Old password is incorrect. Admin password not changed."
 
    return ""
 
 
 
 
# Create a callback to handle admin login, showing the admin page, and registration
@app.callback(
    Output("signin-layout", "style"),
    Output("login-layout", "style"),
    Output("page1-layout","style"),
    Output("admin-layout", "style"),
    Output("registration-layout", "style"),
    Output("change-admin-password-layout", "style"),
    Output("give-access-layout", "style"),
    Output('leave-history-layout','style'),
    Input("admin-button", "n_clicks"),
    Input("user-button", "n_clicks"),
    Input("login-button", "n_clicks"),
    Input("add-emp-button", "n_clicks"),
    Input("register-button", "n_clicks"),
    Input("change-admin-password-button", "n_clicks"),
    Input("give-access-button", "n_clicks"),
    Input('leave-history-button','n_clicks'),
    Input("back-button-registration", "n_clicks"),
    Input("back-button-password", "n_clicks"),
    Input("back-button-give-access", "n_clicks"),
    State("username-input", "value"),
    State("password-input", "value"),
    State("emp-name-input", "value"),
    State("emp-id-input", "value"),
    State("emp-password-input", "value"),
 
)
def handle_login_and_registration(leave_history_clicks,admin_clicks, user_clicks,
        login_clicks, add_emp_clicks, register_clicks, change_password_clicks, give_access_clicks,
        back_registration_clicks, back_password_clicks, back_give_access_clicks,
        username, password, emp_name, emp_id, emp_password):
    page1_style={"display":"none"}
    signin_style = {"display": "block"}
    login_style = {"display": "none"}
    admin_style = {"display": "none"}
    registration_style = {"display": "none"}
    change_admin_password_style = {"display": "none"}
    give_access_style = {"display": "none"}
    leave_history_style={'display':'none'}
 
    ctx = dash.callback_context
 
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
 
        if trigger_id == "login-button":
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            query = "SELECT admin_id FROM admin WHERE admin_id=%s AND password=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result:
                login_style = {"display": "none"}
                admin_style = {"display": "block"}
 
        if trigger_id == "add-emp-button":
            admin_style = {"display": "none"}
            login_style = {"display": "none"}
            registration_style = {"display": "block"}
 
        if trigger_id == "register-button":
            if emp_id and emp_password:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
                query="SELECT emp_id FROM users WHERE emp_id = %s"
                cursor.execute(query, (emp_id,))
                existing_emp = cursor.fetchone()
 
                if existing_emp:
                    registration_style = {"display": "none"}
                    login_style = {"display": "block"}
                else:
                    connection = mysql.connector.connect(**db_config)
                    cursor = connection.cursor()
                    insert_user_query = "INSERT INTO users (emp_id,  password) VALUES (%s, %s)"
                    cursor.execute(insert_user_query, (emp_id, emp_password))
                    connection.commit()
 
        if trigger_id == "change-admin-password-button":
            admin_style = {"display": "none"}
            login_style = {"display": "none"}
            change_admin_password_style = {"display": "block"}
 
        if trigger_id == "give-access-button":
            admin_style = {"display": "none"}
            login_style = {"display": "none"}
            give_access_style = {"display": "block"}
 
        if trigger_id in ["back-button-registration", "back-button-password", "back-button-give-access"]:
            admin_style = {"display": "block"}
            login_style = {"display": "none"}
            registration_style = {"display": "none"}
            change_admin_password_style = {"display": "none"}
        if trigger_id== "admin-button":
        # Check if the provided username and password are correct for admin (you should implement your own validation logic here)
                login_style = {"display": "block"}
        if trigger_id=="user-button":
            page1_style={"display":"block"}
        if trigger_id=='leave-history-button':
            leave_history_style={'display':'block'}
 
 
 
 
    return signin_style,page1_style,login_style, admin_style, registration_style, change_admin_password_style, give_access_style,leave_history_style
 
# Callback to handle giving access with CustomDate
from dash.exceptions import PreventUpdate
from datetime import timedelta, date
 
@app.callback(
    Output("give-access-info", "children"),
    Input("submit-give-access-button", "n_clicks"),
    State("give-access-emp-id", "value"),
    State("give-access-date-range", "start_date"),
    State("give-access-date-range", "end_date"),
)
def give_access(submit_clicks, emp_id, start_date, end_date):
    if not emp_id or not start_date or not end_date:
        raise PreventUpdate  # Prevent callback execution if any of the required fields are empty
 
    start_date = date.fromisoformat(start_date.split(' ')[0])  # Extract date and convert to date object
    end_date = date.fromisoformat(end_date.split(' ')[0])
 
    delta = timedelta(days=1)  # Create a timedelta object to increment the date
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    # Check if the emp_id exists in the EmployeeAccess table
    cursor.execute("SELECT emp_id FROM EmployeeAccess1 WHERE emp_id = %s", (emp_id,))
    result = cursor.fetchone()
 
    if result:
        # Update the existing entry with the new CustomDates
        while start_date <= end_date:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            insert_query = "INSERT INTO EmployeeAccess1 (emp_id, CustomFromDate, CustomToDate) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (emp_id, start_date, start_date))
            start_date += delta  # Increment to the next date
        connection.commit()
    else:
        # Insert a new entry for giving access with the CustomDates
        while start_date <= end_date:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            insert_query = "INSERT INTO EmployeeAccess1 (emp_id, CustomFromDate, CustomToDate) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (emp_id, start_date, start_date))
            start_date += delta  # Increment to the next date
        connection.commit()
 
    return f"Access granted for Employee ID: {emp_id} from {start_date} to {end_date}"
 
 
 
 
# Callback to handle removing an employee
@app.callback(
    Output("employee-info", "children"),
    Input("remove-emp-button", "n_clicks"),
    State("search-input", "value"),
    prevent_initial_call=True
)
def remove_employees(n_clicks, selected_emp_ids):
    if n_clicks and selected_emp_ids:
        for emp_id in selected_emp_ids:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            delete_timesheet_query = "DELETE FROM employee_timesheet WHERE emp_id = %s"
            cursor.execute(delete_timesheet_query, (emp_id,))
            connection.commit()
 
            delete_user_query = "DELETE FROM users WHERE emp_id = %s"
            cursor.execute(delete_user_query, (emp_id,))
            connection.commit()
 
        return f"Employees with EmpIDs {', '.join(selected_emp_ids)} have been removed."
    else:
        return "No action taken."
 
from datetime import datetime
from dateutil.parser import parse
 
from datetime import datetime
 
# ...
 
@app.callback(
    Output("timesheet-table", "data"),
    Input("dummy-trigger", "children"),
    Input("search-button", "n_clicks"),
    State("search-input", "value"),
    State("date-range-input", "start_date"),
    State("date-range-input", "end_date"),
)
def update_timesheet_entries(_, search_clicks, selected_employee_ids, start_date, end_date):
    if search_clicks:
        query = "SELECT emp_id, date, hours_worked FROM employee_timesheet WHERE emp_id IS NOT NULL"
   
        params = []
   
        if selected_employee_ids:
            # Create a comma-separated placeholder string for the IN clause
            placeholder = ",".join(["%s" for _ in selected_employee_ids])
            query += f" AND emp_id IN ({placeholder})"
            params.extend(selected_employee_ids)
   
        if start_date:
            start_date = parse(start_date).date()
            query += " AND date >= %s"
            params.append(start_date)
   
        if end_date:
            end_date = parse(end_date).date()
            query += " AND date <= %s"
            params.append(end_date)
   
        query += " ORDER BY emp_id, date"
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query, params)
        timesheet_records = cursor.fetchall()
   
        # Process the records to get a single entry for each emp_id
        unique_emp_ids = set(record[0] for record in timesheet_records)
        single_entry_records = []
        for emp_id in unique_emp_ids:
            emp_records = [record for record in timesheet_records if record[0] == emp_id]
            from_date = emp_records[0][1]  # First entry's date
            to_date = emp_records[-1][1]  # Last entry's date
            total_hours = sum(record[2] for record in emp_records if record[2] is not None)
            single_entry_records.append((emp_id, from_date, to_date, total_hours))
   
        timesheet_df = pd.DataFrame(single_entry_records, columns=["EmpID", "From Date", "To Date", "Total Hours"])
        return timesheet_df.to_dict('records')
 
dummy_trigger = html.Div(id='dummy-trigger', style={'display': 'none'})
download_component = dcc.Download(id="download-excel")
 
####################################################################################
db_config = {
    "host": 'localhost',
    "user": 'root',
    "password": 'root',
    "database": 'vector',
}
 
# Create a session dictionary to store user-specific information
session = {}
 
# Define styles
login_box_style = {
    'background-color': '#f4f4f4',
    'border-radius': '10px',
    'border': '1px solid #ccc',
    'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'padding': '20px',
}
 
timesheet_style = {
    'background-color': '#f4f4f4',
    'border-radius': '10px',
    'border': '1px solid #ccc',
    'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'padding': '20px',
    'color': 'green',
    'width': '800px',
    'margin':'Auto'
   
}
placeholder={
    'margin-top':'10px',
    'width':'350px',
    'margin-bottom':'10px',
}
import datetime
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
def get_custom_dates(emp_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
 
        # Query to fetch custom dates from the "employeeaccess1" table for the specific emp_id
        query = "SELECT customFromDate FROM employeeaccess1 WHERE emp_id = %s"
        cursor.execute(query, (emp_id,))
       
        custom_dates = [row[0] for row in cursor.fetchall()]
       
        connection.close()
 
        return custom_dates
    except mysql.connector.Error as err:
        print("MySQL Error: {}".format(err))
        return []
 
# Usage in the populate_custom_dates_dropdown callback
 
 
# Define login layout
login_layout = html.Div(
    dbc.Container(
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Employee Login", style={'color': 'green', "margin-left": "70px"}),
                        dbc.Input(type="text", id="emp-id-input1", placeholder="Emp ID", style={'margin-bottom': '10px'}),
                        dbc.Input(type="password", id="password-input1", placeholder="Password", style={'margin-bottom': '20px'}),
                        dbc.Row([dbc.Button("Login", id="login-button1", className='button',style=search_button_style1),
                                ],
                                style={'width': '250px', "margin-left": "40px"})
                    ],
                    className="p-5",
                    style=login_box_style
                ),
                width={"size": 4, "offset": 4},
                className="mt-5",
            )
        ),
    )
)
@app.callback(
    Output("custom-attendance-date", "options"),
    Input("emp-id-input1", "value"),
)
def populate_custom_dates_dropdown(emp_id):
    emp_id = session.get('emp_id')
    if emp_id:
        custom_dates = get_custom_dates(emp_id)
        options = [{"label": date, "value": date} for date in custom_dates]
    else:
        options = []
 
    return options
 
 
# Sample currently logged-in employee (you can replace this with your actual logic)
message_box = html.Div([
    dbc.Button("Leaves Applied By Employee", id="view-leaves-button", color="success",style=search_button_style),
    dbc.Button("leaves Approved By HR", id="approve-leaves-button", color="success",style=search_button_style),
    html.H2("Leaves Applied By Employee", id="leaves-table-heading", style={'text-align': 'center', 'font-size': '20px'}),
    dash_table.DataTable(
        id="leaves-table",
        style_table={'height': '400px', 'overflowY': 'auto', 'margin-bottom': '20px'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#F7F7F7'},
            {'if': {'row_index': 'even', 'column_id': 'emp_id'}, 'backgroundColor': '#E2E2E2', 'cursor': 'pointer'}
        ],
        style_header={'backgroundColor': 'green', 'color': '#FFFFFF', 'fontWeight': 'bold'},
        style_cell={'padding': '10px', 'fontSize': '17px', 'textAlign': 'center'},
        style_data={'transition': 'background-color 0.3s'},
    )
])
 
# Define an HTML element to display the employee's leaves
leaves_display = html.Div(id="leaves-display")
 
 
post_login_layout = dbc.Tabs(
    [
        dbc.Tab(label="Current Date Attendance", children=[
            html.H2("Current Date Attendance"),
            dbc.Input(id="attendance-date", type="text", placeholder="Date", value=current_date, disabled=True, style=placeholder),
            dbc.Input(id="total-hours-worked", type="number", min=0, max=9, step=1, placeholder="Total Hours Worked", style=placeholder),
            dbc.Button("Submit", id="submit-attendance-button", color="success", className="mt-3", style=search_button_style),
            html.Div(id="current-date-status", style={"margin-top": "10px"})
        ], style=timesheet_style),
 
        dbc.Tab(label="Custom Date Attendance", children=[
            html.H2("Custom Date Attendance"),
            dcc.Dropdown(
                id="custom-attendance-date",
                options=[],
                placeholder="Select Custom Date",
                style=placeholder
            ),
            dbc.Input(id="custom-total-hours-worked", type="number", min=0, max=9, step=1, placeholder="Total Hours Worked", style=placeholder),
            dbc.Button("Submit", id="custom-attendance-button", color="success", className="mt-3", style=search_button_style),
            html.Div(id="custom-date-status", style={"margin-top": "10px"})
        ], style=timesheet_style),
 
        dbc.Tab(label="Change Password", children=[
            html.H2("Change Password"),
            dbc.Input(id="old-password", type="password", placeholder="Old Password", style=placeholder),
            dbc.Input(id="new-password", type="password", placeholder="New Password", style=placeholder),
            dbc.Input(id="confirm-new-password", type="password", placeholder="Confirm New Password", style=placeholder),
            dbc.Input(id="emp-id-input1", type="text", style={'display': 'none'}),  # Hidden input
            dbc.Button("Change Password", id="change-password-button", color="success", className="mt-3", style=search_button_style),
            html.Div(id="password-change-status", style={"margin-top": "10px"})
        ], style=timesheet_style),
 
        dbc.Tab(label="Apply Leave", children=[
            html.H2("Apply Leave"),
            dcc.DatePickerRange(
                id="leave-date-range",
                start_date_placeholder_text="Start Date",
                end_date_placeholder_text="End Date",
                display_format="YYYY-MM-DD",
            ),
            dbc.Input(id="leave-reason", type="text", placeholder="Reason", style=placeholder),
            dbc.Textarea(id="leave-description", placeholder="Leave Description", style=placeholder),
            dbc.Button("Apply Leave", id="apply-leave-button", color="success", className="mt-3", style=search_button_style),
            html.Div(id="apply-leave-status", style={"margin-top": "10px"})
        ], style=timesheet_style),
        dbc.Tab(label="Leaves Details", children=[
            html.H2("Manage Leaves"),
            message_box,
            leaves_display,
        ], style=timesheet_style),
    ],
    style=timesheet_style,
)
 
@app.callback(
    Output("leave-date-range", "end_date"),
    Input("leave-date-range", "start_date")
)
def update_end_date(start_date):
    if start_date:
        # If the start date is provided, set the end date to be the same as the start date
        return start_date
    # If no start date is provided, return None for the end date
    return None
 
 
style_table = {
    'height': '400px',
    'overflowY': 'auto',
    'transition': 'background-color 0.3s',
    "border":'2px solid green'
}
style_data_conditional = [
    {'if': {'row_index': 'odd'}, 'backgroundColor': '#F7F7F7'},
    {'if': {'row_index': 'even', 'column_id': 'EmpID'}, 'backgroundColor': '#E2E2E2', 'cursor': 'pointer'}
]
 
style_header = {'backgroundColor': 'green', 'color': '#FFFFFF', 'fontWeight': 'bold',"border":'2px solid green'}
style_cell = {
    'padding': '10px',
    'fontSize': '17px',
    'textAlign': 'center',
    'transition': 'background-color 0.3s' ,
     "border":'2px solid green' # Add a transition effect
}
 
 
@app.callback(
    Output("leaves-table", "data"),
    Output("leaves-table", "columns"),
    Output("leaves-table-heading", "children"),
    Input("view-leaves-button", "n_clicks"),
    Input("approve-leaves-button", "n_clicks"),
    State("view-leaves-button", "n_clicks"),
    State("approve-leaves-button", "n_clicks"),
)
def display_leaves(view_clicks, approve_clicks, view_n_clicks, approve_n_clicks):
    ctx = dash.callback_context
    data = []
    columns = []
    heading_text = "Leaves Applied By Employee"
 
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
       
        if button_id == "view-leaves-button" and view_clicks:
            # Reset "Approved Leaves" button clicks
            approve_n_clicks = 0
        elif button_id == "approve-leaves-button" and approve_clicks:
            # Reset "View Leaves" button clicks
            view_n_clicks = 0
            heading_text = "Leaves Approved By HR"
 
        emp_id = session.get('emp_id')
        if emp_id:
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
               
                if view_n_clicks:
                    # Query to fetch leaves of the specific emp_id from "LeaveRecords" table
                    query = """
                        SELECT emp_id, from_date, to_date, reason, description, 'leaverecords' as source
                        FROM leaverecords
                        WHERE emp_id = %s
                        UNION
                        SELECT emp_id, from_date, to_date, reason, description, 'leavesapproved' as source
                        FROM leavesapproved
                        WHERE emp_id = %s
                        UNION
                        SELECT emp_id, from_date, to_date, reason, description, 'pendingleaves' as source
                        FROM pendingleaves
                        WHERE emp_id = %s
                    """
                    cursor.execute(query, (emp_id, emp_id, emp_id))
                elif approve_n_clicks:
                    # Query to fetch leaves of the specific emp_id from "LeavesApproved" table
                    query = "SELECT * FROM LeavesApproved WHERE emp_id = %s"
               
                    cursor.execute(query, (emp_id,))
                leaves = cursor.fetchall()
                connection.close()
               
                if leaves:
                    # Define the columns for the table
                    columns = [{"name": "From Date", "id": "from_date"},
                               {"name": "To Date", "id": "to_date"},
                               {"name": "Reason", "id": "reason"}]
 
                    # Create the data for the table
                    data = [{"from_date": leave[2], "to_date": leave[3], "reason": leave[4]} for leave in leaves]
                else:
                    if view_n_clicks:
                        data = [{"from_date": "No leaves applied", "to_date": "", "reason": ""}]
                    elif approve_n_clicks:
                        data = [{"from_date": "No leaves approved", "to_date": "", "reason": ""}]
            except mysql.connector.Error as err:
                print("MySQL Error: {}".format(err))
                data = [{"from_date": "Error fetching leaves", "to_date": "", "reason": ""}]
 
    return data, columns, heading_text
 
 
@app.callback(
    Output('apply-leave-status', 'children'),
    Input('apply-leave-button', 'n_clicks'),
    State('emp-id-input1', 'value'),
    State('leave-date-range', 'start_date'),
    State('leave-date-range', 'end_date'),
    State('leave-reason', 'value'),
    State('leave-description', 'value')
)
def apply_leave(n_clicks, emp_id, from_date, to_date, reason, description):
    if n_clicks:
        emp_id = session.get('emp_id')
 
        if not (from_date and reason and description):
            return "Please fill in all the required fields."
 
        if from_date == to_date and not (reason and description):
            return "Please provide a reason and description for one-day leave."
 
        try:
            # Create a MySQL database connection
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
 
            # Prepare the SQL insert statement
            insert_query = "INSERT INTO LeaveRecords (emp_id, from_date, to_date, reason, description) " \
                           "VALUES (%s, %s, %s, %s, %s)"
 
            # Execute the insert statement with the provided data
            cursor.execute(insert_query, (emp_id, from_date, to_date, reason, description))
 
            # Commit the transaction and close the cursor and connection
            conn.commit()
            cursor.close()
            conn.close()
 
            return "Leave applied successfully"
        except Exception as e:
            return f"Error: {str(e)}"
 
    return None
 
 
 
@app.callback(
    Output("page1-layout", "children"),
    Input("login-button1", "n_clicks"),
    State("emp-id-input1", "value"),
    State("password-input1", "value"),
)
def handle_login(n_clicks, emp_id, password):
    if n_clicks is not None:
        # Connect to the MySQL database and verify credentials
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
 
            query = "SELECT * FROM users WHERE emp_id = %s AND password = %s"
            cursor.execute(query, (emp_id, password))
            user = cursor.fetchone()
 
            if user:
                # Store the emp_id in the session
                session['emp_id'] = emp_id
                # Successful login, switch to post-login page
                return post_login_layout
            else:
                # Failed login
                return html.Div("Login failed. Please check your credentials.")
 
        except mysql.connector.Error as err:
            print("MySQL Error: {}".format(err))
            return html.Div("Error connecting to the database.")
 
    # Return the login layout by default
    return login_layout
 
@app.callback(
    Output("password-change-status", "children"),
    Input("change-password-button", "n_clicks"),
    State("old-password", "value"),
    State("new-password", "value"),
    State("confirm-new-password", "value"),
    State("emp-id-input1", "value"),
)
def handle_password_change(n_clicks, old_password, new_password, confirm_new_password, emp_id_input):
    if n_clicks:
        # Connect to the MySQL database and verify old password
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            emp_id = session.get('emp_id')  # Retrieve the emp_id from the session
            print(emp_id)
            # Check if the old password matches the current password in the database
            query = "SELECT password FROM users WHERE emp_id = %s"
            cursor.execute(query, (emp_id,))
            current_password = cursor.fetchone()
 
            if not current_password:
                return html.Div("User not found. Password change failed.")
 
            if old_password != current_password[0]:
                return html.Div("Old password does not match. Password change failed.")
 
            # Check if the new password and confirm new password match
            if new_password != confirm_new_password:
                return html.Div("New password and confirm new password do not match. Password change failed.")
 
            # Update the password in the database
            update_query = "UPDATE users SET password = %s WHERE emp_id = %s"
            cursor.execute(update_query, (new_password, emp_id))
 
            # Commit the changes to the database
            connection.commit()
            connection.close()
 
            return html.Div("Password changed successfully.")
 
        except mysql.connector.Error as err:
            print("MySQL Error: {}".format(err))
            return html.Div("Error changing the password.")
 
    return html.Div("")
@app.callback(
    Output("custom-date-status", "children"),
    Input("custom-attendance-button", "n_clicks"),
    State("custom-attendance-date", "value"),
    State("custom-total-hours-worked", "value"),
)
def handle_submit_custom_attendance(n_clicks, custom_date, custom_total_hours_worked):
    if n_clicks:
        if not custom_date:
            return "Please select a custom date before submitting."
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            emp_id = session.get('emp_id')
            if custom_total_hours_worked is None or custom_total_hours_worked == 0:
                return "Please enter a valid total hours worked before submitting."
            # Check if attendance for the given date already exists
            query = "SELECT * FROM employee_timesheet WHERE date = %s AND emp_id = %s"
            cursor.execute(query, (custom_date, emp_id))
            existing_attendance = cursor.fetchone()
 
            if existing_attendance:
                return "Attendance for this date has already been marked."
 
            # Insert the custom date attendance into the employee_timesheet table
            insert_query = "INSERT INTO employee_timesheet (date, hours_worked, emp_id) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (custom_date, custom_total_hours_worked, emp_id))
 
            # Delete the selected date from the employeeaccess1 table
            delete_query = "DELETE FROM employeeaccess1 WHERE customFromDate = %s"
            cursor.execute(delete_query, (custom_date,))
 
            # Commit the changes to the database
            connection.commit()
            connection.close()
 
            return "Attendance has been marked and the date has been removed by admin"
 
        except mysql.connector.Error as err:
            print("MySQL Error: {}".format(err))
            return html.Div("Error submitting data to the database: {}".format(err))
 
    return ''
@app.callback(
    Output("current-date-status", "children"),
    Input("submit-attendance-button", "n_clicks"),
    State("attendance-date", "value"),
    State("total-hours-worked", "value"),
)
def handle_submit_attendance(n_clicks, attendance_date, total_hours_worked):
    if n_clicks:
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            emp_id = session.get('emp_id')
            if total_hours_worked is None or total_hours_worked == 0:
                return "Please enter a valid total hours worked before submitting."
 
            query = "SELECT * FROM employee_timesheet WHERE date = %s AND emp_id = %s"
            cursor.execute(query, (attendance_date, emp_id))
            existing_attendance = cursor.fetchone()
 
            if existing_attendance:
                return "Attendance for this date has already been marked."
           
            # Insert the current date attendance record into the employee_timesheet table
            insert_query = "INSERT INTO employee_timesheet (date, hours_worked, emp_id) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (attendance_date, total_hours_worked, emp_id))
 
            # Commit the changes to the database
            connection.commit()
            connection.close()
 
            print("Data inserted successfully.")
            return "Attendance has been marked."
 
        except mysql.connector.Error as err:
            print("MySQL Error: {}".format(err))
            return html.Div("Error submitting data to the database: {}".format(err))
 
    return ''
# Define the overall layout
app.layout = html.Div([
    html.Div(id="signin-layout",children=signin_layout,style={"display":"block"}),
    html.Div(id="login-layout", children=admin_login_layout, style={"display": "none"}),
    html.Div(id="admin-layout", children=admin_layout, style={"display": "none"}),
    html.Div(id="registration-layout", children=registration_layout, style={"display": "none"}),
    html.Div(id="change-admin-password-layout", children=change_admin_password_layout, style={"display": "none"}),
    html.Div(id="give-access-layout", children=give_access_layout, style={"display": "none"}),
    html.Div(id="leave-history-layout", children=leave_records_table, style={"display": "none"}),
    dummy_trigger,
    download_component,
    download_component1,
    Consolidated,
    popup,
    html.Div(id="page1-layout", children=login_layout,style={"display":"none"})
])
 
if __name__ == "__main__":
    app.run_server(host='192.168.29.111', port=8080,debug=True)