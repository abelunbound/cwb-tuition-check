from dash import Input, Output, State, callback, no_update, ctx

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