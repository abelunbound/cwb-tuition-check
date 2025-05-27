import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc



# Register the page
dash.register_page(
    __name__, 
    path="/", 
    title="Profile | GoodFaith", 
    name="Profile"
)

# Callback to handle link clicks
@callback(
    Output('url', 'pathname'),
    Input({'type': 'view-link', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def handle_view_click(n_clicks):
    if any(click for click in n_clicks if click):
        return '/finhealth'
    return dash.no_update

# Page header component
def create_page_header():
    return html.Div(
        className="dashboard-header",
        children=[
            html.H1("Welcome!", className="dashboard-title"),
            html.P("""Here your university staff or agents can verify the 
                   financial capabilities of international
                    applicants for your BSc and MSc programs 
                   from over 30+ countries within minutes using our open banking capabilities. 
                   Our advanced machine learning capabilities
                   let you forecast risks of tuition payment default.""", 
                   className="dashboard-subtitle"
                   ),
        ]
    )

# First Row: Personal Information Card
def create_personal_info_card():
    return dbc.Card(
        dbc.CardBody([
            # Verified Badge in top right corner
            html.Div(
                "Verified", 
                className="position-absolute badge", 
                style={
                    "top": "10px", 
                    "right": "10px",
                    "backgroundColor": "rgba(46, 204, 113, 0.15)", 
                    "color": "#2ECC71"
                }
            ),
            dbc.Row([
                dbc.Col([
                    html.H4("Personal Information", className="card-title mb-4"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("First Name"),
                            dbc.Input(
                                type="text", 
                                placeholder="Enter first name", 
                                value="Abel",
                                className="mb-3"
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Last Name"),
                            dbc.Input(
                                type="text", 
                                placeholder="Enter last name", 
                                value="Johnson",
                                className="mb-3"
                            )
                        ], width=6),
                        
                        dbc.Col([
                            dbc.Label("Email Address"),
                            dbc.Input(
                                type="email", 
                                placeholder="Enter email", 
                                value="abel.johnson@example.com",
                                className="mb-3"
                            )
                        ], width=12),
                        
                        dbc.Col([
                            dbc.Label("Phone Number"),
                            dbc.InputGroup([
                                dbc.InputGroupText("+44"),
                                dbc.Input(
                                    type="tel", 
                                    placeholder="Phone number", 
                                    value="7700 900000"
                                )
                            ], className="mb-3")
                        ], width=12),
                        
                        dbc.Col([
                            dbc.Button("Update Profile", color="primary")
                        ], width=12)
                    ])
                ], width=12)
            ])
        ], className="position-relative")
    )

# Second Row: Timeline Cards
def create_timeline_cards():
    # Affordability Check Card
    affordability_card = dbc.Card(
        dbc.CardBody([
            html.Div(
                "Pending", 
                className="position-absolute badge", 
                style={
                    "top": "10px", 
                    "right": "10px",
                    "backgroundColor": "rgba(231, 76, 60, 0.15)", 
                    "color": "#E74C3C"
                }
            ),
            html.Div([
                html.I(className="bi bi-check2-circle mb-3", style={"fontSize": "36px", "color": "#5F2EEA"}),
                html.H5("Financial Requirements", className="mb-3"),
                html.P("Verify your income and expenses", className="text-muted mb-3"),
                dbc.Button("Create new", id="create-financial-req-btn", color="primary", outline=True)
            ], className="text-center")
        ]),
        className="h-100 position-relative"
    )

    # Credit Check Card
    credit_check_card = dbc.Card(
        dbc.CardBody([
            html.Div(
                "Pending", 
                className="position-absolute badge", 
                style={
                    "top": "10px", 
                    "right": "10px",
                    "backgroundColor": "rgba(231, 76, 60, 0.15)", 
                    "color": "#E74C3C"
                }
            ),
            html.Div([
                html.I(className="bi bi-person-bounding-box mb-3", style={"fontSize": "36px", "color": "#5F2EEA"}),
                html.H5("Single applicant check", className="mb-3"),
                html.P("Soft credit check for group trust", className="text-muted mb-3"),
                dbc.Button("Start check", href="https://goodfaith.vercel.app/risk-analysis?enterprise=1", target="_blank", color="primary", outline=True)
            ], className="text-center")
        ]),
        className="h-100 position-relative"
    )

    # Direct Debit Card
    direct_debit_card = dbc.Card(
        dbc.CardBody([
            html.Div(
                "Pending", 
                className="position-absolute badge", 
                style={
                    "top": "10px", 
                    "right": "10px",
                    "backgroundColor": "rgba(231, 76, 60, 0.15)", 
                    "color": "#E74C3C"
                }
            ),
            html.Div([
                html.I(className="bi bi-people-fill mb-3", style={"fontSize": "36px", "color": "#5F2EEA"}),
                html.H5("Batch applicant check", className="mb-3"),
                html.P("Configure automatic contributions", className="text-muted mb-3"),
                dbc.Button("Batch check", id="batch-check-btn", color="primary", outline=True)
            ], className="text-center")
        ]),
        className="h-100 position-relative"
    )

    return dbc.Row([
        dbc.Col(affordability_card, width=4),
        dbc.Col(credit_check_card, width=4),
        dbc.Col(direct_debit_card, width=4)
    ])

# Account Settings Card
def create_account_settings_card():
    # Fetch data from applicant_table
    try:
        from functions.database import retrieve_data_from_sql
        df = retrieve_data_from_sql('applicant_table')
        
        if df is not None and len(df) > 0:
            # Convert DataFrame to list of dictionaries for the table
            data = []
            for _, row in df.iterrows():
                # Format status with icons
                status = row['check_status']
                if status == 'pending':
                    status_display = '⚠️ Pending'
                elif status == 'completed':
                    status_display = '✅ Completed'
                elif status == 'expired':
                    status_display = '❌ Expired'
                else:
                    status_display = status
                
                data.append({
                    'applicant_id': row['applicant_id'],
                    'name': row['name'],
                    'email': row['email'],
                    'course': row['course'],
                    'country': row['country'],
                    'date_applied': str(row['application_date']) if row['application_date'] else '',
                    'status': status_display,
                    'actions': 'View'
                })
        else:
            # Fallback to empty data if no records found
            data = []
    except Exception as e:
        print(f"Error fetching applicant data: {e}")
        # Fallback to empty data on error
        data = []

    return dbc.Card(
        dbc.CardBody([
            html.H5("Applicants financial profiles", className="card-title mb-3"),
            html.Div([
                # Store for current applicant ID
                dcc.Store(id='current-applicant-id'),
                dash_table.DataTable(
                    id='applicants-table',
                    columns=[
                        {'name': 'ID', 'id': 'applicant_id'},
                        {'name': 'Name', 'id': 'name'},
                        {'name': 'Email', 'id': 'email'},
                        {'name': 'Course', 'id': 'course'},
                        {'name': 'Country', 'id': 'country'},
                        {'name': 'Date Applied', 'id': 'date_applied'},
                        {'name': 'Status', 'id': 'status'},
                        {
                            'name': 'Actions',
                            'id': 'actions',
                            'type': 'text'
                        }
                    ],
                    data=data,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '12px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '14px',
                        'border': '1px solid #e0e0e0'
                    },
                    style_header={
                        'backgroundColor': '#5F2EEA',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'border': '1px solid #5F2EEA',
                        'fontSize': '14px'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'white'
                        },
                        {
                            'if': {'row_index': 'even'},
                            'backgroundColor': 'white'
                        },
                        {
                            'if': {'column_id': 'actions'},
                            'cursor': 'pointer',
                            'color': '#5F2EEA',
                            'textDecoration': 'underline',
                            'fontWeight': '500'
                        },
                        {
                            'if': {'column_id': 'status'},
                            'textAlign': 'center',
                            'fontWeight': '500'
                        },
                        {
                            'if': {'state': 'active'},
                            'backgroundColor': '#e3d5ff',
                            'border': '1px solid #5F2EEA'
                        }
                    ],
                    page_size=10,
                    cell_selectable=True,
                    row_selectable=False,
                )
            ])
        ])
    )

# Callback to handle cell clicks
@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Output('url', 'refresh'),
    Input('applicants-table', 'active_cell'),
    State('applicants-table', 'data'),
    prevent_initial_call=True
)
def handle_cell_click(active_cell, data):
    if active_cell and active_cell['column_id'] == 'actions':
        return '/finhealth', True  # Force a refresh when navigating
    return dash.no_update, dash.no_update

# Security Card
def create_security_card():
    return dbc.Card(
        dbc.CardBody([
            html.H5("Security", className="card-title mb-3"),
            html.Div([
                html.Div(
                    className="mb-3",
                    children=[
                        html.Label("Change Password", className="mb-2"),
                        dbc.Input(
                            type="password", 
                            placeholder="Current Password", 
                            className="mb-2"
                        ),
                        dbc.Input(
                            type="password", 
                            placeholder="New Password", 
                            className="mb-2"
                        ),
                        dbc.Input(
                            type="password", 
                            placeholder="Confirm New Password", 
                            className="mb-3"
                        ),
                        dbc.Button("Update Password", color="primary", outline=True)
                    ]
                ),
                html.Div(
                    className="mb-3",
                    children=[
                        html.Label("Two-Factor Authentication", className="mb-2"),
                        dbc.Row([
                            dbc.Col([
                                html.P("Add an extra layer of security to your account", className="mb-2"),
                                dbc.Button(
                                    "Enable 2FA", 
                                    color="primary", 
                                    outline=True,
                                    className="me-2"
                                ),
                            ], width=8),
                            dbc.Col([
                                html.Div(
                                    className="text-muted small",
                                    children=[
                                        html.I(className="fas fa-info-circle me-2"),
                                        "Recommended for added security"
                                    ]
                                )
                            ], width=4),
                        ])
                    ]
                )
            ])
        ])
    )

# Create financial requirements modal
def create_financial_requirements_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("Create Financial Requirement"),
            dbc.ModalBody([
                # Success message (initially hidden)
                html.Div(
                    id="financial-req-success-message",
                    children=[
                        html.Div([
                            html.I(className="bi bi-check-circle-fill me-2", style={"fontSize": "24px", "color": "#28a745"}),
                            html.Span("✓ Financial requirement created successfully! Click 'Close' to exit.", 
                                     style={"color": "#28a745", "fontSize": "18px", "fontWeight": "500"})
                        ], className="text-center p-4")
                    ],
                    style={"display": "none"}
                ),
                # Form content (initially visible)
                html.Div(
                    id="financial-req-form-content",
                    children=[
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Course Name"),
                                    dbc.Input(
                                        type="text",
                                        id="course-name",
                                        placeholder="Enter course name",
                                        className="mb-3"
                                    ),
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Tuition Amount (£)"),
                                    dbc.Input(
                                        type="number",
                                        id="tuition-amount",
                                        placeholder="Enter tuition amount",
                                        className="mb-3"
                                    ),
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("Home Office Amount (£)"),
                                    dbc.Input(
                                        type="number",
                                        id="home-office-amount",
                                        placeholder="Enter home office amount",
                                        className="mb-3"
                                    ),
                                ], width=6),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Session Year"),
                                    dbc.Input(
                                        type="text",
                                        id="session-year",
                                        placeholder="e.g., 2024-2025",
                                        className="mb-3"
                                    ),
                                ]),
                            ]),
                            html.H6("Requirement Checkpoints", className="mt-3 mb-2"),
                            dbc.Checklist(
                                options=[
                                    {"label": "Home office living expense check", "value": "home_office_check"},
                                    {"label": "Tuition check", "value": "tuition_check"},
                                    {"label": "Exchange rate risks", "value": "exchange_rate_risks"},
                                    {"label": "Basic balance check", "value": "basic_balance_check"},
                                    {"label": "Probability of payment default forecast", "value": "payment_default_forecast"},
                                ],
                                id="requirement-checkpoints",
                                className="mb-3"
                            ),
                            html.Div(id="financial-req-error", className="text-danger mb-3"),
                        ]),
                    ]
                )
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Close",
                    id="financial-req-close",
                    className="ms-auto",
                    n_clicks=0
                ),
                dbc.Button(
                    "Create Requirement",
                    id="financial-req-submit",
                    color="primary",
                    className="ms-2",
                    n_clicks=0
                ),
            ]),
        ],
        id="financial-req-modal",
        is_open=False,
    )

# Financial Requirements Modal Callbacks
@callback(
    Output("financial-req-modal", "is_open"),
    [
        Input("create-financial-req-btn", "n_clicks"),
        Input("financial-req-close", "n_clicks")
    ],
    [State("financial-req-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_financial_req_modal(create_click, close_click, is_open):
    """Toggle the financial requirements modal"""
    from dash import ctx
    if not ctx.triggered:
        return dash.no_update
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if trigger_id == "create-financial-req-btn":
        return True
    elif trigger_id == "financial-req-close":
        return False
    return is_open

@callback(
    [
        Output("financial-req-error", "children"),
        Output("course-name", "value"),
        Output("tuition-amount", "value"),
        Output("home-office-amount", "value"),
        Output("session-year", "value"),
        Output("requirement-checkpoints", "value"),
        Output("financial-req-submit", "style"),
        Output("financial-req-success-message", "style"),
        Output("financial-req-form-content", "style")
    ],
    Input("financial-req-submit", "n_clicks"),
    [
        State("course-name", "value"),
        State("tuition-amount", "value"),
        State("home-office-amount", "value"),
        State("session-year", "value"),
        State("requirement-checkpoints", "value"),
        State("session-store", "data")
    ],
    prevent_initial_call=True
)
def handle_financial_req_submit(n_clicks, course_name, tuition_amount, home_office_amount, session_year, checkpoints, session_data):
    """Handle financial requirement form submission"""
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Validate required fields
    if not all([course_name, tuition_amount, home_office_amount, session_year]):
        return "Please fill in all required fields.", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Get org_id from session
    if not session_data or not session_data.get('user_info', {}).get('org_id'):
        return "Session expired. Please log in again.", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    try:
        from functions.database import create_financial_requirements_table, insert_financial_requirement
        
        # Create table if it doesn't exist
        create_financial_requirements_table()
        
        # Calculate total finance
        total_finance = float(tuition_amount) + float(home_office_amount)
        
        # Prepare requirement data
        requirement_data = {
            "org_id": session_data['user_info']['org_id'],
            "course_name": course_name,
            "tuition_amount": float(tuition_amount),
            "home_office_amount": float(home_office_amount),
            "total_finance": total_finance,
            "session_year": session_year,
            "home_office_check": "home_office_check" in (checkpoints or []),
            "tuition_check": "tuition_check" in (checkpoints or []),
            "exchange_rate_risks": "exchange_rate_risks" in (checkpoints or []),
            "basic_balance_check": "basic_balance_check" in (checkpoints or []),
            "payment_default_forecast": "payment_default_forecast" in (checkpoints or [])
        }
        
        # Insert the requirement
        success, message, requirement_id = insert_financial_requirement(requirement_data)
        
        if success:
            # Show success message, hide form and submit button
            return "", "", "", "", "", [], {"display": "none"}, {"display": "block"}, {"display": "none"}
        else:
            return f"Error: {message}", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            
    except Exception as e:
        print(f"Error during financial requirement creation: {str(e)}")
        return "An error occurred. Please try again.", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Reset financial requirements modal state when reopened
@callback(
    [
        Output("financial-req-success-message", "style", allow_duplicate=True),
        Output("financial-req-form-content", "style", allow_duplicate=True),
        Output("financial-req-submit", "style", allow_duplicate=True),
        Output("course-name", "value", allow_duplicate=True),
        Output("tuition-amount", "value", allow_duplicate=True),
        Output("home-office-amount", "value", allow_duplicate=True),
        Output("session-year", "value", allow_duplicate=True),
        Output("requirement-checkpoints", "value", allow_duplicate=True),
        Output("financial-req-error", "children", allow_duplicate=True)
    ],
    Input("create-financial-req-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_financial_req_modal(n_clicks):
    """Reset financial requirements modal to initial state when reopened"""
    if n_clicks:
        return (
            {"display": "none"},  # Hide success message
            {"display": "block"},  # Show form content
            {"display": "inline-block"},  # Show submit button
            "",  # Clear course name
            "",  # Clear tuition amount
            "",  # Clear home office amount
            "",  # Clear session year
            [],  # Clear checkpoints
            ""   # Clear error message
        )
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Create batch check modal
def create_batch_check_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("Batch Applicant Check"),
            dbc.ModalBody([
                # Success message (initially hidden)
                html.Div(
                    id="batch-success-message",
                    children=[
                        html.Div([
                            html.I(className="bi bi-check-circle-fill me-2", style={"fontSize": "24px", "color": "#28a745"}),
                            html.Span(id="batch-success-text", 
                                     style={"color": "#28a745", "fontSize": "18px", "fontWeight": "500"})
                        ], className="text-center p-4")
                    ],
                    style={"display": "none"}
                ),
                # Form content (initially visible)
                html.Div(
                    id="batch-form-content",
                    children=[
                        html.P("Please upload the excel file with name, course, email, country, application_date, for applicants for whom you want to conduct checks. Once you click on 'start check', an email will be sent to the applicants with a link to commence their checks.", 
                               className="mb-4"),
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Start Date"),
                                    dbc.Input(
                                        type="date",
                                        id="batch-start-date",
                                        className="mb-3"
                                    ),
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("End Date"),
                                    dbc.Input(
                                        type="date",
                                        id="batch-end-date",
                                        className="mb-3"
                                    ),
                                ], width=6),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Upload CSV File"),
                                    dcc.Upload(
                                        id="batch-upload",
                                        children=html.Div([
                                            "Drag and Drop or ",
                                            html.A("Select CSV File")
                                        ]),
                                        style={
                                            'width': '100%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },
                                        accept='.csv',
                                        className="mb-3"
                                    ),
                                ]),
                            ]),
                            html.Div(id="batch-upload-status", className="mb-3"),
                            html.Div(id="batch-error", className="text-danger mb-3"),
                        ]),
                    ]
                )
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Close",
                    id="batch-close",
                    className="ms-auto",
                    n_clicks=0
                ),
                dbc.Button(
                    "Start Check",
                    id="batch-start",
                    color="primary",
                    className="ms-2",
                    n_clicks=0,
                    disabled=True
                ),
            ]),
        ],
        id="batch-check-modal",
        is_open=False,
        size="lg"
    )

# Batch Check Modal Callbacks
@callback(
    Output("batch-check-modal", "is_open"),
    [
        Input("batch-check-btn", "n_clicks"),
        Input("batch-close", "n_clicks")
    ],
    [State("batch-check-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_batch_check_modal(open_click, close_click, is_open):
    """Toggle the batch check modal"""
    from dash import ctx
    if not ctx.triggered:
        return dash.no_update
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if trigger_id == "batch-check-btn":
        return True
    elif trigger_id == "batch-close":
        return False
    return is_open

@callback(
    [
        Output("batch-upload-status", "children"),
        Output("batch-start", "disabled")
    ],
    Input("batch-upload", "contents"),
    State("batch-upload", "filename"),
    prevent_initial_call=True
)
def handle_batch_upload(contents, filename):
    """Handle CSV file upload and validation"""
    if contents is None:
        return "", True
    
    try:
        import pandas as pd
        import base64
        import io
        
        # Decode the file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Read CSV
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Validate required columns
        required_columns = ['name', 'course', 'email', 'country', 'application_date']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return f"Missing required columns: {', '.join(missing_columns)}", True
        
        # Check for empty required fields
        for col in ['name', 'course', 'email', 'country']:
            if df[col].isnull().any() or (df[col] == '').any():
                return f"Column '{col}' cannot have empty values", True
        
        return f"✓ File uploaded successfully. {len(df)} applicants found.", False
        
    except Exception as e:
        return f"Error reading file: {str(e)}", True

@callback(
    [
        Output("batch-error", "children"),
        Output("batch-start-date", "value"),
        Output("batch-end-date", "value"),
        Output("batch-upload", "contents"),
        Output("batch-start", "style"),
        Output("batch-success-message", "style"),
        Output("batch-form-content", "style"),
        Output("batch-success-text", "children")
    ],
    Input("batch-start", "n_clicks"),
    [
        State("batch-start-date", "value"),
        State("batch-end-date", "value"),
        State("batch-upload", "contents"),
        State("batch-upload", "filename"),
        State("session-store", "data")
    ],
    prevent_initial_call=True
)
def handle_batch_start(n_clicks, start_date, end_date, contents, filename, session_data):
    """Handle batch check start"""
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Validate inputs
    if not all([start_date, end_date, contents]):
        return "Please fill in all fields and upload a CSV file.", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Get org_id from session
    if not session_data or not session_data.get('user_info', {}).get('org_id'):
        return "Session expired. Please log in again.", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    try:
        import pandas as pd
        import base64
        import io
        from functions.database import create_applicant_table, insert_batch_applicants
        
        # Create table if it doesn't exist
        create_applicant_table()
        
        # Decode and read CSV
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Convert DataFrame to list of dictionaries
        applicants_data = df.to_dict('records')
        
        # Insert into database
        success, message, count = insert_batch_applicants(applicants_data, start_date, end_date)
        
        if success:
            # Show success message, hide form and start button
            success_text = f"✓ Successfully inserted {count} applicants. Emails will be sent to applicants. Click 'Close' to exit."
            return "", "", "", None, {"display": "none"}, {"display": "block"}, {"display": "none"}, success_text
        else:
            return f"Error: {message}", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            
    except Exception as e:
        print(f"Error during batch processing: {str(e)}")
        return "An error occurred. Please try again.", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Reset modal state when reopened
@callback(
    [
        Output("batch-success-message", "style", allow_duplicate=True),
        Output("batch-form-content", "style", allow_duplicate=True),
        Output("batch-start", "style", allow_duplicate=True),
        Output("batch-start-date", "value", allow_duplicate=True),
        Output("batch-end-date", "value", allow_duplicate=True),
        Output("batch-upload", "contents", allow_duplicate=True),
        Output("batch-upload-status", "children", allow_duplicate=True),
        Output("batch-error", "children", allow_duplicate=True)
    ],
    Input("batch-check-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_batch_modal(n_clicks):
    """Reset modal to initial state when reopened"""
    if n_clicks:
        return (
            {"display": "none"},  # Hide success message
            {"display": "block"},  # Show form content
            {"display": "inline-block"},  # Show start button
            "",  # Clear start date
            "",  # Clear end date
            None,  # Clear upload
            "",  # Clear upload status
            ""   # Clear error message
        )
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Callback to refresh applicants table data
@callback(
    Output('applicants-table', 'data'),
    [
        Input('url', 'pathname'),
        Input('batch-start', 'n_clicks')
    ],
    prevent_initial_call=False
)
def refresh_applicants_table(pathname, batch_clicks):
    """Refresh applicants table data from database"""
    try:
        from functions.database import retrieve_data_from_sql
        df = retrieve_data_from_sql('applicant_table')
        
        if df is not None and len(df) > 0:
            # Convert DataFrame to list of dictionaries for the table
            data = []
            for _, row in df.iterrows():
                # Format status with icons
                status = row['check_status']
                if status == 'pending':
                    status_display = '⚠️ Pending'
                elif status == 'completed':
                    status_display = '✅ Completed'
                elif status == 'expired':
                    status_display = '❌ Expired'
                else:
                    status_display = status
                
                data.append({
                    'applicant_id': row['applicant_id'],
                    'name': row['name'],
                    'email': row['email'],
                    'course': row['course'],
                    'country': row['country'],
                    'date_applied': str(row['application_date']) if row['application_date'] else '',
                    'status': status_display,
                    'actions': 'View'
                })
            return data
        else:
            return []
    except Exception as e:
        print(f"Error fetching applicant data: {e}")
        return []

# Change from static layout to function-based layout
def layout():
    return html.Div([
        # Page Header
        create_page_header(),
        
        # Container for all profile sections
        dbc.Container([

            
            # Second Row: Timeline Cards
            html.Div(className="mb-4", children=[create_timeline_cards()]),
            
            # Third Row: Account Settings
            html.Div(className="mb-4", children=[
                dbc.Row([
                    dbc.Col(create_account_settings_card(), width=12)
                ])
            ]),
            
            # # Fourth Row: Security
            # html.Div(className="mb-4", children=[
            #     dbc.Row([
            #         dbc.Col(create_security_card(), width=12)
            #     ])
            # ]),
            
            # # Fifth Row: Notifications
            # html.Div(children=[
            #     dbc.Row([
            #         dbc.Col(create_notifications_card(), width=12)
            #     ])
            # ])
        ]),
        
        # Financial Requirements Modal
        create_financial_requirements_modal(),
        
        # Batch Check Modal
        create_batch_check_modal(),
    ])