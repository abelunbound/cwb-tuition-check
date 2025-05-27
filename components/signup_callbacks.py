from dash import Input, Output, State, callback, no_update, ctx
from functions.database import (
    create_enterprise_clients_table,
    insert_enterprise_client,
    get_enterprise_client_by_email,
    hash_password
)

@callback(
    Output("signup-modal", "is_open"),
    [
        Input("signup-link", "n_clicks"),
        Input("signup-close", "n_clicks"),
        Input("signup-submit", "n_clicks")
    ],
    [State("signup-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_signup_modal(signup_click, close_click, submit_click, is_open):
    """Toggle the signup modal"""
    if not ctx.triggered:
        return no_update
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if trigger_id == "signup-link":
        return True
    elif trigger_id in ["signup-close", "signup-submit"]:
        return False
    return is_open

@callback(
    [
        Output("signup-error", "children"),
        Output("signup-enterprise-name", "value"),
        Output("signup-first-name", "value"),
        Output("signup-last-name", "value"),
        Output("signup-group-email", "value"),
        Output("signup-person-email", "value"),
        Output("signup-phone", "value"),
        Output("signup-password", "value")
    ],
    Input("signup-submit", "n_clicks"),
    [
        State("signup-enterprise-name", "value"),
        State("signup-first-name", "value"),
        State("signup-last-name", "value"),
        State("signup-group-email", "value"),
        State("signup-person-email", "value"),
        State("signup-phone", "value"),
        State("signup-password", "value")
    ],
    prevent_initial_call=True
)
def handle_signup_submit(n_clicks, enterprise_name, first_name, last_name, group_email, person_email, phone, password):
    """Handle signup form submission"""
    if not n_clicks:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # Validate required fields
    if not all([enterprise_name, first_name, last_name, person_email, password]):
        return "Please fill in all required fields.", no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # Check if user already exists
    existing_user = get_enterprise_client_by_email(person_email)
    if existing_user:
        return "A user with this email already exists.", no_update, no_update, no_update, no_update, no_update, no_update, no_update

    try:
        # Create the enterprise clients table if it doesn't exist
        create_enterprise_clients_table()

        # Prepare client data
        client_data = {
            "enterprise_name": enterprise_name,
            "first_name": first_name,
            "last_name": last_name,
            "group_email": group_email,
            "person_email": person_email,
            "phone": phone,
            "password": password  # Pass plain password, let insert_enterprise_client handle hashing
        }

        # Insert the new client
        insert_enterprise_client(client_data)

        # Clear form fields on success
        return "Signup successful! You can now log in.", "", "", "", "", "", "", ""

    except Exception as e:
        print(f"Error during signup: {str(e)}")
        return f"An error occurred during signup. Please try again.", no_update, no_update, no_update, no_update, no_update, no_update, no_update 