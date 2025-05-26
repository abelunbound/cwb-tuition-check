from dash import html
import dash_bootstrap_components as dbc

def create_signup_modal():
    """Create the signup modal component"""
    return dbc.Modal(
        [
            dbc.ModalHeader("Sign Up for GoodFaith Platform"),
            dbc.ModalBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Enterprise Name"),
                            dbc.Input(
                                type="text",
                                id="signup-enterprise-name",
                                placeholder="Enter your institution name",
                                className="mb-3"
                            ),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("First Name"),
                            dbc.Input(
                                type="text",
                                id="signup-first-name",
                                placeholder="Enter your first name",
                                className="mb-3"
                            ),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Last Name"),
                            dbc.Input(
                                type="text",
                                id="signup-last-name",
                                placeholder="Enter your last name",
                                className="mb-3"
                            ),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Group Email"),
                            dbc.Input(
                                type="email",
                                id="signup-group-email",
                                placeholder="Enter department/group email",
                                className="mb-3"
                            ),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Personal Email"),
                            dbc.Input(
                                type="email",
                                id="signup-person-email",
                                placeholder="Enter your email",
                                className="mb-3"
                            ),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Phone"),
                            dbc.Input(
                                type="tel",
                                id="signup-phone",
                                placeholder="Enter phone number",
                                className="mb-3"
                            ),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Password"),
                            dbc.Input(
                                type="password",
                                id="signup-password",
                                placeholder="Create password",
                                className="mb-3"
                            ),
                        ], width=6),
                    ]),
                    html.Div(id="signup-error", className="text-danger mb-3"),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Close",
                    id="signup-close",
                    className="ms-auto",
                    n_clicks=0
                ),
                dbc.Button(
                    "Sign Up",
                    id="signup-submit",
                    color="primary",
                    className="ms-2",
                    n_clicks=0
                ),
            ]),
        ],
        id="signup-modal",
        is_open=False,
    ) 