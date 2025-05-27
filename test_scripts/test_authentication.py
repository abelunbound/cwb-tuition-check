import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, project_root)
os.environ['PYTHONPATH'] = project_root

from auth import validate_user

def test_authentication():
    """Test the new database authentication system"""
    
    print("🔐 Testing Database Authentication System")
    print("=" * 50)
    
    # Test 1: Valid credentials
    print("\n1. Testing valid credentials...")
    user_data = validate_user("demo@example.com", "password123")
    if user_data:
        print("✅ Authentication successful!")
        print(f"   Email: {user_data['email']}")
        print(f"   Name: {user_data['name']}")
        print(f"   Org ID: {user_data['org_id']}")
        print(f"   Enterprise: {user_data['enterprise_name']}")
    else:
        print("❌ Authentication failed!")
    
    # Test 2: Invalid password
    print("\n2. Testing invalid password...")
    user_data = validate_user("demo@example.com", "wrongpassword")
    if user_data:
        print("❌ Authentication should have failed!")
    else:
        print("✅ Authentication correctly rejected invalid password")
    
    # Test 3: Invalid email
    print("\n3. Testing invalid email...")
    user_data = validate_user("nonexistent@example.com", "password123")
    if user_data:
        print("❌ Authentication should have failed!")
    else:
        print("✅ Authentication correctly rejected invalid email")
    
    # Test 4: Empty credentials
    print("\n4. Testing empty credentials...")
    user_data = validate_user("", "")
    if user_data:
        print("❌ Authentication should have failed!")
    else:
        print("✅ Authentication correctly rejected empty credentials")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication testing completed!")

if __name__ == "__main__":
    test_authentication() 