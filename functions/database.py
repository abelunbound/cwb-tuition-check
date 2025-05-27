import psycopg2
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from pathlib import Path
import bcrypt
np.bool = np.bool_ # https://stackoverflow.com/questions/74893742/how-to-solve-attributeerror-module-numpy-has-no-attribute-bool

# Load environment variables from the functions directory
env_path = Path(__file__).parent / 'cwb-db.env'
load_dotenv(env_path)

# Insert the data into the SQL database - modified to use execute many

def get_column_name_and_datatype_dictionary(df):
    """
    Convert DataFrame column names and types to SQL-compatible dictionary format.
    
    Parameters:
    df (DataFrame): Pandas DataFrame to extract column information from
    
    Returns:
    dict: Dictionary mapping column names to SQL data types
    """
    # Get DataFrame dtypes as dictionary
    dtype_dict = df.dtypes.to_dict()
    
    # Map pandas dtypes to SQL types
    sql_type_mapping = {
        'int64': 'INTEGER',
        'int32': 'INTEGER',
        'float64': 'FLOAT',
        'float32': 'FLOAT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP',
        'object': 'VARCHAR(255)',  # Default for strings/objects
        'category': 'VARCHAR(255)',
        'timedelta64[ns]': 'INTERVAL'
    }
    
    # Create column definitions dictionary
    column_definitions = {}
    for column, dtype in dtype_dict.items():
        # Convert dtype to string and extract the type name
        dtype_str = str(dtype)
        # Map pandas dtype to SQL type
        if dtype_str in sql_type_mapping:
            sql_type = sql_type_mapping[dtype_str]
        else:
            sql_type = 'VARCHAR(255)'  # Default fallback
        
        column_definitions[column] = sql_type
    
    return column_definitions



# Helper function to convert boolean values to Python bool type (this resolve the "can't adapt type 'numpy.bool_'" error.)
def convert_value(value, col, boolean_columns):
    if isinstance(value, np.bool_):
        return bool(value)
    elif col in boolean_columns:
        return bool(value)
    return value


def prepare_sql_queries_and_values(column_definitions, table_name, data):
    """
    Prepare SQL queries and values for creating a table and upserting data based on a composite key.
    
    Parameters:
    column_definitions (dict): Dictionary mapping column names to SQL data types
    table_name (str): Name of the table to create/insert into
    data (DataFrame): Pandas DataFrame containing the data to insert
    
    Returns:
    tuple: (table_query, insert_query, values_list)
    """
    # Extract just the column names for other operations
    columns = list(column_definitions.keys())
    
    # Define the composite unique columns for upsert operations
    primary_key_columns = ["applicant_id", "sn"]
    
    # Boolean columns for conversion
    boolean_columns = [col for col, type_def in column_definitions.items() if type_def == 'BOOLEAN']
    
    # Create table query with unique constraint on the composite key
    table_columns_definition = ",\n            ".join(f"{col} {data_type}" for col, data_type in column_definitions.items())
    constraints = f",\n            CONSTRAINT {table_name}_pk PRIMARY KEY ({', '.join(primary_key_columns)})"
    
    table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
            {table_columns_definition}{constraints}
    ) 
    """
    
    # Create upsert query (INSERT ... ON CONFLICT)
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    
    # Create the update clause for all columns except the primary key columns
    non_key_columns = [col for col in columns if col not in primary_key_columns]
    update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in non_key_columns])
    
    insert_query = f"""
    INSERT INTO {table_name} ({columns_str}) 
    VALUES ({placeholders})
    ON CONFLICT ({', '.join(primary_key_columns)}) 
    DO UPDATE SET {update_clause}
    """
    
    # Create values list with proper type conversion
    # values_list = [
    #     tuple(bool(row[col]) if col in boolean_columns else row[col] for col in columns)
    #     for index, row in data.iterrows()
    # ]
    
    values_list = [
    tuple(convert_value(row[col], col, boolean_columns) for col in columns)
    for index, row in data.iterrows()
]
    return table_query, insert_query, values_list



def get_db_connection():
    """
    Creates a database connection using environment variables
    
    TODO: Security Improvement Needed
    - Remove hardcoded fallback credentials before deploying to production
    - Add proper error handling for missing environment variables
    - See TODO.md for complete list of pending security improvements
    """
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'cwb-database').strip("'"),
            user=os.getenv('DB_USER', 'abelakeni').strip("'"),
            password=os.getenv('DB_PASSWORD', 'unbound365').strip("'"),
            host=os.getenv('DB_HOST', '35.192.88.249').strip("'"),
            port=os.getenv('DB_PORT', '5432').strip("'")   
        )
        print(f"\nConnected to database...'{os.getenv('DB_NAME', 'cwb-database')}'")
        return connection 
    
    except psycopg2.Error as error:
        print(f"Error connecting to the database: {error}")
        return None

def insert_data_into_sql_data_base(table_query, insert_query, values_list):
    """
    Insert data into the database using prepared SQL components.
    
    Parameters:
    table_query (str): SQL query to create the table
    insert_query (str): SQL query to insert data
    values_list (list): List of value tuples to insert
    
    Returns:
    None
    """
    try:
        # Create connection to the SQL database
        connection = get_db_connection()

        # Defensive programming - check if connection was successful
        if not connection:
            return
        
        # Create a cursor 
        cursor = connection.cursor()

        # Extract table name from the CREATE TABLE query

        # This assumes your table_query follows the format "CREATE TABLE IF NOT EXISTS table_name (...)"
        table_name = table_query.split('CREATE TABLE IF NOT EXISTS ')[1].split('(')[0].strip()
        
        # # Drop the existing table - added once when I needed to have a table with a different column structyre but same name
        # drop_query = f"DROP TABLE IF EXISTS {table_name}"
        # cursor.execute(drop_query)
        # print(f"Dropped table {table_name} if it existed")
      
        # Create a table
        cursor.execute(table_query)
        
        # Execute batch insert
        print(f"Inserting {len(values_list)} rows in a batch...into table '{table_name}'")
        
        cursor.executemany(insert_query, values_list)
        
        # Commit the data into the connection
        connection.commit()
        
        # Success note/ Inform user
        print("Your data has been inserted successfully into the SQL database...")
        
    except psycopg2.Error as error:
        print(f" an error has occurred : {error}")
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()
            print("Your connection is closed\n")




def retrieve_data_from_sql(table_name):
    """
    Retrieve data from a specified SQL table and return it as a pandas DataFrame.
    
    This function establishes a connection to the database, executes a SELECT query
    to fetch records from the specified table, and converts the results into a
    pandas DataFrame with appropriate column names.
    
    Parameters:
    ----------
    table_name : str
        The name of the SQL table to retrieve data from
        
    Returns:
    -------
    pandas.DataFrame
        A DataFrame containing all records from the specified table,
        with columns named according to the table schema.
        Returns None if connection fails or an error occurs.
    
    Raises:
    ------
    The function handles exceptions internally and prints error messages,
    but does not raise exceptions to the caller.
    """
    try:
        # Create connection to the SQL database
        connection = get_db_connection()

        # Defensive programming - check if connection was successful
        if not connection:
            return
        
        # Create a cursor
        cursor = connection.cursor()
        
        # Retrieve Data from the table
        table_query = f"SELECT * FROM {table_name}"
        cursor.execute(table_query)
        result = cursor.fetchall()
        
        # Convert the data from the SQL database to a dataframe
        column_name = [header[0] for header in cursor.description] # what other items are held in the cursor.description 
        df = pd.DataFrame(result, columns= column_name) 

        # Success note/ Inform user
        
        print("Your data has retrieved successfully from the SQL database...")
        print(f"Data frame with length: {len(df)} retrieved from {table_name}...")
        
    except psycopg2.Error as error:
        print(f"You have encountered an error: {error}")
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()
            print("Your connection is closed")
    return df



def add_metadata_columns(df, applicant_id="123456789"):
    """
    Add metadata columns to a DataFrame with user ID, current date, and transaction time.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame to add columns to
    applicant_id : str, optional
        The user ID to add to all rows (default: "1234")
        
    Returns:
    -------
    pandas.DataFrame
        The DataFrame with the additional columns
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()
    
    # Add metadata columns with proper datetime objects
    result_df['applicant_id'] = applicant_id
    result_df['date_added'] = pd.Timestamp.now().date()
    result_df['transaction_time'] = pd.Timestamp.now()

    # Add sequence number starting from 1
    result_df['sn'] = range(1, len(result_df) + 1)
    
    return result_df

def create_enterprise_clients_table():
    """
    Create the enterprise_clients table if it doesn't exist.
    This table stores university signup information.
    """
    table_query = """
    CREATE TABLE IF NOT EXISTS enterprise_clients (
        org_id SERIAL PRIMARY KEY,
        enterprise_name VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        group_email VARCHAR(255) NOT NULL,
        person_email VARCHAR(255) NOT NULL UNIQUE,
        phone VARCHAR(50),
        password VARCHAR(255) NOT NULL,
        address_line1 VARCHAR(255),
        address_line2 VARCHAR(255),
        address_line3 VARCHAR(255),
        city VARCHAR(255),
        postcode VARCHAR(50),
        country VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        cursor.execute(table_query)
        connection.commit()
        print("Enterprise clients table created successfully")
        return True
        
    except psycopg2.Error as error:
        print(f"Error creating enterprise_clients table: {error}")
        return False
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Parameters:
    password (str): The plain text password to hash
    
    Returns:
    str: The hashed password as a string
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Convert bytes to string for storage
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Parameters:
    plain_password (str): The password to verify
    hashed_password (str): The hashed password to check against (as string)
    
    Returns:
    bool: True if the password matches, False otherwise
    """
    try:
        # Convert string hash back to bytes
        hashed_bytes = hashed_password.encode('utf-8')
        # Convert plain password to bytes and verify
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_bytes
        )
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def insert_enterprise_client(client_data):
    """
    Insert a new enterprise client into the database.
    
    Parameters:
    client_data (dict): Dictionary containing client information with keys:
        - enterprise_name
        - first_name
        - last_name
        - group_email
        - person_email
        - phone
        - password
        - address_line1 (optional)
        - address_line2 (optional)
        - address_line3 (optional)
        - city (optional)
        - postcode (optional)
        - country (optional)
    
    Returns:
    tuple: (success, message, org_id)
        - success (bool): Whether the insertion was successful
        - message (str): Success or error message
        - org_id (int): The ID of the inserted client if successful, None otherwise
    """
    insert_query = """
    INSERT INTO enterprise_clients (
        enterprise_name, first_name, last_name, group_email,
        person_email, phone, password, address_line1, address_line2,
        address_line3, city, postcode, country
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) RETURNING org_id
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return False, "Database connection failed", None
        
        cursor = connection.cursor()
        
        # Hash the password before storing
        hashed_password = hash_password(client_data['password'])
        
        # Prepare values tuple with hashed password
        values = (
            client_data.get('enterprise_name'),
            client_data.get('first_name'),
            client_data.get('last_name'),
            client_data.get('group_email'),
            client_data.get('person_email'),
            client_data.get('phone'),
            hashed_password,  # Store the hashed password
            client_data.get('address_line1'),
            client_data.get('address_line2'),
            client_data.get('address_line3'),
            client_data.get('city'),
            client_data.get('postcode'),
            client_data.get('country')
        )
        
        cursor.execute(insert_query, values)
        org_id = cursor.fetchone()[0]
        connection.commit()
        
        return True, "Enterprise client created successfully", org_id
        
    except psycopg2.IntegrityError as error:
        if "person_email" in str(error):
            return False, "Email already registered", None
        return False, f"Database integrity error: {error}", None
        
    except psycopg2.Error as error:
        return False, f"Database error: {error}", None
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()

def get_enterprise_client_by_email(email, include_password=False):
    """
    Retrieve an enterprise client by their email address.
    
    Parameters:
    email (str): The email address to search for
    include_password (bool): Whether to include the hashed password in the result
    
    Returns:
    dict: Client information if found, None otherwise
    """
    query = """
    SELECT org_id, enterprise_name, first_name, last_name, group_email,
           person_email, phone, password, address_line1, address_line2,
           address_line3, city, postcode, country
    FROM enterprise_clients
    WHERE person_email = %s
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        
        if result:
            client_data = {
                'org_id': result[0],
                'enterprise_name': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'group_email': result[4],
                'person_email': result[5],
                'phone': result[6],
                'address_line1': result[8],
                'address_line2': result[9],
                'address_line3': result[10],
                'city': result[11],
                'postcode': result[12],
                'country': result[13]
            }
            if include_password:
                client_data['password'] = result[7]
            return client_data
        return None
        
    except psycopg2.Error as error:
        print(f"Error retrieving enterprise client: {error}")
        return None
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()

def verify_enterprise_client(email: str, password: str) -> tuple[bool, str, dict]:
    """
    Verify an enterprise client's credentials.
    
    Parameters:
    email (str): The client's email address
    password (str): The plain text password to verify
    
    Returns:
    tuple: (success, message, client_data)
        - success (bool): Whether the verification was successful
        - message (str): Success or error message
        - client_data (dict): Client information if successful, None otherwise
    """
    try:
        # Get client data including password
        client_data = get_enterprise_client_by_email(email, include_password=True)
        
        if not client_data:
            return False, "Invalid email or password", None
            
        # Verify the password
        if not verify_password(password, client_data['password']):
            return False, "Invalid email or password", None
            
        # Remove password from client data before returning
        del client_data['password']
        return True, "Authentication successful", client_data
        
    except Exception as error:
        return False, f"Authentication error: {str(error)}", None

def create_financial_requirements_table():
    """
    Create the financial_requirements table if it doesn't exist.
    This table stores financial requirements for courses.
    """
    table_query = """
    CREATE TABLE IF NOT EXISTS financial_requirements (
        requirement_id SERIAL PRIMARY KEY,
        org_id INTEGER NOT NULL REFERENCES enterprise_clients(org_id),
        course_name VARCHAR(255) NOT NULL,
        tuition_amount DECIMAL(10,2) NOT NULL,
        home_office_amount DECIMAL(10,2) NOT NULL,
        total_finance DECIMAL(10,2) NOT NULL,
        session_year VARCHAR(50) NOT NULL,
        home_office_check BOOLEAN DEFAULT FALSE,
        tuition_check BOOLEAN DEFAULT FALSE,
        exchange_rate_risks BOOLEAN DEFAULT FALSE,
        basic_balance_check BOOLEAN DEFAULT FALSE,
        payment_default_forecast BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        cursor.execute(table_query)
        connection.commit()
        print("Financial requirements table created successfully")
        return True
        
    except psycopg2.Error as error:
        print(f"Error creating financial_requirements table: {error}")
        return False
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()

def insert_financial_requirement(requirement_data):
    """
    Insert a new financial requirement into the database.
    
    Parameters:
    requirement_data (dict): Dictionary containing requirement information
    
    Returns:
    tuple: (success, message, requirement_id)
    """
    insert_query = """
    INSERT INTO financial_requirements (
        org_id, course_name, tuition_amount, home_office_amount, total_finance,
        session_year, home_office_check, tuition_check, exchange_rate_risks,
        basic_balance_check, payment_default_forecast
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) RETURNING requirement_id
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return False, "Database connection failed", None
        
        cursor = connection.cursor()
        
        values = (
            requirement_data.get('org_id'),
            requirement_data.get('course_name'),
            requirement_data.get('tuition_amount'),
            requirement_data.get('home_office_amount'),
            requirement_data.get('total_finance'),
            requirement_data.get('session_year'),
            requirement_data.get('home_office_check', False),
            requirement_data.get('tuition_check', False),
            requirement_data.get('exchange_rate_risks', False),
            requirement_data.get('basic_balance_check', False),
            requirement_data.get('payment_default_forecast', False)
        )
        
        cursor.execute(insert_query, values)
        requirement_id = cursor.fetchone()[0]
        connection.commit()
        
        return True, "Financial requirement created successfully", requirement_id
        
    except psycopg2.Error as error:
        return False, f"Database error: {error}", None
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()

def create_applicant_table():
    """
    Create the applicant_table if it doesn't exist.
    This table stores batch applicant check information.
    """
    table_query = """
    CREATE TABLE IF NOT EXISTS applicant_table (
        applicant_id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        course VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL,
        application_date DATE,
        start_date DATE,
        end_date DATE,
        check_status VARCHAR(50) DEFAULT 'pending'
    )
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        cursor.execute(table_query)
        connection.commit()
        print("Applicant table created successfully")
        return True
        
    except psycopg2.Error as error:
        print(f"Error creating applicant_table: {error}")
        return False
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()

def get_next_applicant_id():
    """
    Get the next available applicant ID in format ap086xxxxx
    """
    query = """
    SELECT applicant_id FROM applicant_table 
    WHERE applicant_id LIKE 'ap086%' 
    ORDER BY applicant_id DESC 
    LIMIT 1
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return "ap08600001"  # Default first ID
        
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            last_id = result[0]
            # Extract number part and increment
            number_part = int(last_id[5:])  # Remove 'ap086' prefix
            next_number = number_part + 1
            return f"ap086{next_number:05d}"
        else:
            return "ap08600001"  # First ID
            
    except psycopg2.Error as error:
        print(f"Error getting next applicant ID: {error}")
        return "ap08600001"
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()

def insert_batch_applicants(applicants_data, start_date, end_date):
    """
    Insert batch applicants into the database.
    
    Parameters:
    applicants_data (list): List of dictionaries containing applicant information
    start_date (str): Start date for the batch check
    end_date (str): End date for the batch check
    
    Returns:
    tuple: (success, message, inserted_count)
    """
    insert_query = """
    INSERT INTO applicant_table (
        applicant_id, name, course, email, country, application_date, start_date, end_date, check_status
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    
    try:
        connection = get_db_connection()
        if not connection:
            return False, "Database connection failed", 0
        
        cursor = connection.cursor()
        
        # Get the starting ID once at the beginning
        cursor.execute("""
            SELECT applicant_id FROM applicant_table 
            WHERE applicant_id LIKE 'ap086%' 
            ORDER BY applicant_id DESC 
            LIMIT 1
        """)
        result = cursor.fetchone()
        
        if result:
            last_id = result[0]
            next_number = int(last_id[5:]) + 1  # Remove 'ap086' prefix and increment
        else:
            next_number = 1  # First ID
        
        inserted_count = 0
        
        for applicant in applicants_data:
            # Generate ID for this applicant
            applicant_id = f"ap086{next_number:05d}"
            
            values = (
                applicant_id,
                applicant.get('name'),
                applicant.get('course'),
                applicant.get('email'),
                applicant.get('country'),
                applicant.get('application_date'),
                start_date,
                end_date,
                'pending'
            )
            
            cursor.execute(insert_query, values)
            inserted_count += 1
            next_number += 1  # Increment for next applicant
        
        connection.commit()
        return True, f"Successfully inserted {inserted_count} applicants", inserted_count
        
    except psycopg2.Error as error:
        return False, f"Database error: {error}", 0
        
    finally:
        if "connection" in locals() and connection is not None:
            cursor.close()
            connection.close()