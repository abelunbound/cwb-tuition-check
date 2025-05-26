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
                html.I(className="fas fa-chart-pie mb-3", style={"fontSize": "36px", "color": "#5F2EEA"}),
                html.H5("Financial Requirements", className="mb-3"),
                html.P("Verify your income and expenses", className="text-muted mb-3"),
                dbc.Button("Create new", color="primary", outline=True)
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
                html.I(className="fas fa-chart-line mb-3", style={"fontSize": "36px", "color": "#5F2EEA"}),
                html.H5("Single applicant check", className="mb-3"),
                html.P("Soft credit check for group trust", className="text-muted mb-3"),
                dbc.Button("Perform Check", color="primary", outline=True)
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
                html.I(className="fas fa-credit-card mb-3", style={"fontSize": "36px", "color": "#5F2EEA"}),
                html.H5("Batch applicant check", className="mb-3"),
                html.P("Configure automatic contributions", className="text-muted mb-3"),
                dbc.Button("Add Bank Details", color="primary", outline=True)
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
    # Sample data for the table
    data = [
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP002',
            'name': 'Sarah Johnson',
            'email': 'sarah.j@email.com',
            'course': 'BSc Business Administration',
            'date_applied': '2024-03-14',
            'actions': 'View'
        },
        {
            'applicant_id': 'APP003',
            'name': 'Michael Chen',
            'email': 'michael.c@email.com',
            'course': 'MSc Data Science',
            'date_applied': '2024-03-13',
            'actions': 'View'
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },
        {
            'applicant_id': 'APP001',
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'course': 'MSc Computer Science',
            'date_applied': '2024-03-15',
            'actions': 'View'  # Simple text that will be clickable
        },

    ]

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
                        {'name': 'Date Applied', 'id': 'date_applied'},
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
                        'padding': '10px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        },
                        {
                            'if': {'column_id': 'actions'},
                            'cursor': 'pointer',
                            'color': 'blue',
                            'textDecoration': 'underline'
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
        ])
    ])