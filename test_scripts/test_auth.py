import sys
import os
from pathlib import Path
import uuid

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from functions.database import (
    create_enterprise_clients_table,
    insert_enterprise_client,
    get_enterprise_client_by_email,
    verify_enterprise_client
)

def test_enterprise_client_signup_and_auth():
    """Test the complete flow of enterprise client signup and authentication."""
    
    # First, ensure the table exists
    print("Creating enterprise clients table...")
    create_enterprise_clients_table()
    
    # Generate unique email for this test run
    unique_id = str(uuid.uuid4())[:8]
    email = f"john.doe.{unique_id}@testuniversity.edu"
    
    # Test data
    test_client = {
        'enterprise_name': 'Test University',
        'first_name': 'John',
        'last_name': 'Doe',
        'group_email': f'admin.{unique_id}@testuniversity.edu',
        'person_email': email,
        'phone': '+1234567890',
        'password': 'SecurePass123!',
        'address_line1': '123 Campus Drive',
        'city': 'Test City',
        'postcode': '12345',
        'country': 'Test Country'
    }
    
    # Test 1: Create new client
    print("\nTest 1: Creating new enterprise client...")
    success, message, org_id = insert_enterprise_client(test_client)
    print(f"Success: {success}")
    print(f"Message: {message}")
    print(f"Org ID: {org_id}")
    assert success, "Failed to create enterprise client"
    
    # Test 2: Verify correct password
    print("\nTest 2: Verifying correct password...")
    success, message, client_data = verify_enterprise_client(
        test_client['person_email'],
        test_client['password']
    )
    print(f"Success: {success}")
    print(f"Message: {message}")
    print(f"Retrieved client data: {client_data}")
    assert success, "Password verification failed for correct password"
    
    # Test 3: Verify incorrect password
    print("\nTest 3: Testing incorrect password...")
    success, message, client_data = verify_enterprise_client(
        test_client['person_email'],
        'WrongPassword123!'
    )
    print(f"Success: {success}")
    print(f"Message: {message}")
    assert not success, "Password verification should fail for incorrect password"
    
    # Test 4: Verify non-existent email
    print("\nTest 4: Testing non-existent email...")
    success, message, client_data = verify_enterprise_client(
        'nonexistent@email.com',
        'anypassword'
    )
    print(f"Success: {success}")
    print(f"Message: {message}")
    assert not success, "Should fail for non-existent email"
    
    # Test 5: Test duplicate email registration
    print("\nTest 5: Testing duplicate email registration...")
    success, message, org_id = insert_enterprise_client(test_client)
    print(f"Success: {success}")
    print(f"Message: {message}")
    assert not success, "Should not allow duplicate email registration"
    
    print("\nAll tests completed successfully!")

if __name__ == '__main__':
    test_enterprise_client_signup_and_auth() 