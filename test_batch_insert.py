#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from functions.database import (
    create_applicant_table, 
    insert_batch_applicants, 
    get_next_applicant_id,
    get_db_connection
)
import pandas as pd

def test_database_connection():
    """Test if we can connect to the database"""
    print("Testing database connection...")
    conn = get_db_connection()
    if conn:
        print("✅ Database connection successful")
        conn.close()
        return True
    else:
        print("❌ Database connection failed")
        return False

def test_table_creation():
    """Test if we can create the applicant table"""
    print("\nTesting table creation...")
    result = create_applicant_table()
    if result:
        print("✅ Table creation successful")
        return True
    else:
        print("❌ Table creation failed")
        return False

def test_applicant_id_generation():
    """Test applicant ID generation"""
    print("\nTesting applicant ID generation...")
    try:
        next_id = get_next_applicant_id()
        print(f"✅ Next applicant ID: {next_id}")
        return True
    except Exception as e:
        print(f"❌ Applicant ID generation failed: {e}")
        return False

def test_batch_insertion():
    """Test batch insertion with sample data"""
    print("\nTesting batch insertion...")
    
    # Sample data from CSV
    sample_data = [
        {
            'name': 'John Smith',
            'course': 'MSc Computer Science',
            'email': 'john.smith@email.com',
            'country': 'United Kingdom',
            'application_date': '2024-03-15'
        },
        {
            'name': 'Sarah Johnson',
            'course': 'BSc Business Administration',
            'email': 'sarah.j@email.com',
            'country': 'Canada',
            'application_date': '2024-03-14'
        }
    ]
    
    start_date = '2024-03-20'
    end_date = '2024-03-30'
    
    try:
        success, message, count = insert_batch_applicants(sample_data, start_date, end_date)
        if success:
            print(f"✅ Batch insertion successful: {message}")
            return True
        else:
            print(f"❌ Batch insertion failed: {message}")
            return False
    except Exception as e:
        print(f"❌ Batch insertion error: {e}")
        return False

def check_inserted_data():
    """Check if data was actually inserted"""
    print("\nChecking inserted data...")
    try:
        from functions.database import retrieve_data_from_sql
        df = retrieve_data_from_sql('applicant_table')
        if df is not None and len(df) > 0:
            print(f"✅ Found {len(df)} records in applicant_table:")
            print(df.to_string())
            return True
        else:
            print("❌ No data found in applicant_table")
            return False
    except Exception as e:
        print(f"❌ Error checking data: {e}")
        return False

def main():
    print("🧪 Testing Batch Applicant Insertion Functionality\n")
    
    # Run all tests
    tests = [
        test_database_connection,
        test_table_creation,
        test_applicant_id_generation,
        test_batch_insertion,
        check_inserted_data
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if not all(results):
        print("\n🔍 Some tests failed. Check the output above for details.")
    else:
        print("\n🎉 All tests passed!")

if __name__ == "__main__":
    main() 