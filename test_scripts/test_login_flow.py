import sys
import os
from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, project_root)
os.environ['PYTHONPATH'] = project_root

def test_login_flow():
    """Test the complete login flow with database authentication"""
    
    print("🔐 Testing Complete Login Flow with Database Authentication")
    print("=" * 60)
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = None
    
    try:
        # Initialize Chrome driver
        print("\n1. Starting Chrome browser...")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        # Navigate to the app
        print("2. Navigating to the application...")
        driver.get("http://localhost:8050")
        
        # Wait for the login page to load
        print("3. Waiting for login page to load...")
        wait.until(EC.presence_of_element_located((By.ID, "email-input")))
        print("✅ Login page loaded successfully")
        
        # Test 1: Invalid credentials
        print("\n4. Testing invalid credentials...")
        email_input = driver.find_element(By.ID, "email-input")
        password_input = driver.find_element(By.ID, "password-input")
        login_button = driver.find_element(By.ID, "login-button")
        
        email_input.clear()
        email_input.send_keys("invalid@example.com")
        password_input.clear()
        password_input.send_keys("wrongpassword")
        login_button.click()
        
        # Wait for error message
        time.sleep(2)
        try:
            error_element = driver.find_element(By.ID, "login-error")
            if error_element.text:
                print("✅ Invalid credentials correctly rejected")
            else:
                print("❌ No error message displayed for invalid credentials")
        except NoSuchElementException:
            print("❌ Error element not found")
        
        # Test 2: Valid credentials
        print("\n5. Testing valid credentials...")
        email_input.clear()
        email_input.send_keys("demo@example.com")
        password_input.clear()
        password_input.send_keys("password123")
        login_button.click()
        
        # Wait for successful login (should redirect to dashboard)
        print("6. Waiting for successful login...")
        try:
            # Look for elements that indicate successful login
            wait.until(EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard")),
                EC.presence_of_element_located((By.ID, "logout-btn")),
                EC.presence_of_element_located((By.CLASS_NAME, "header"))
            ))
            print("✅ Login successful! Dashboard loaded")
            
            # Check if user name is displayed
            try:
                # Look for any element that might contain the user name
                page_source = driver.page_source
                if "Abel Demo" in page_source or "Demo University" in page_source:
                    print("✅ User information correctly displayed")
                else:
                    print("⚠️  User information not found in page")
            except Exception as e:
                print(f"⚠️  Could not verify user information: {str(e)}")
            
            # Test logout
            print("\n7. Testing logout functionality...")
            try:
                logout_button = driver.find_element(By.ID, "logout-btn")
                logout_button.click()
                
                # Wait for redirect back to login page
                wait.until(EC.presence_of_element_located((By.ID, "email-input")))
                print("✅ Logout successful! Redirected to login page")
                
            except Exception as e:
                print(f"❌ Logout test failed: {str(e)}")
                
        except TimeoutException:
            print("❌ Login failed - dashboard not loaded")
            # Check for error messages
            try:
                error_element = driver.find_element(By.ID, "login-error")
                if error_element.text:
                    print(f"   Error message: {error_element.text}")
            except:
                pass
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        
    finally:
        if driver:
            print("\n8. Closing browser...")
            driver.quit()
    
    print("\n" + "=" * 60)
    print("🎉 Login flow testing completed!")

if __name__ == "__main__":
    test_login_flow() 