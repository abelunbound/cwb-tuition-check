from functions.database import verify_enterprise_client

# Session timeout (24 hours)
# SESSION_TIMEOUT = 24 * 60 * 60  # in seconds
SESSION_TIMEOUT = 0.5 * 60 * 60  # in seconds

def validate_user(email, password):
    """
    Validate user credentials against the enterprise_clients database table.
    
    Parameters:
    email (str): User's email address
    password (str): User's plain text password
    
    Returns:
    dict: User information if valid, None if invalid
    """
    try:
        # Use the database verification function
        success, message, client_data = verify_enterprise_client(email, password)
        
        if success and client_data:
            # Return user info in the format expected by app.py
            return {
                'email': client_data['person_email'],
                'name': f"{client_data['first_name']} {client_data['last_name']}",
                'org_id': client_data['org_id'],
                'enterprise_name': client_data['enterprise_name']
            }
        else:
            print(f"Authentication failed: {message}")
            return None
            
    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return None