import pyodbc
import streamlit as st

def init_databases_and_tables(host, user, password, dbs_to_create):
    """
    Connects to the master database, creates the required databases if they don't exist,
    and initializes sample tables in the primary database.
    """
    # Use master database for checking/creating databases
    master_conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host};DATABASE=master;UID={user};PWD={password};"
    
    try:
        # Autocommit must be True to execute CREATE DATABASE
        conn = pyodbc.connect(master_conn_str, autocommit=True)
        cursor = conn.cursor()
        
        for db in dbs_to_create:
            cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{db}'")
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE [{db}]")
                
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Failed to initialize databases: {e}")
        return False

    # Initialize sample tables in the primary 'database'
    primary_db = st.secrets["MSSQL"]["database"]
    db_conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host};DATABASE={primary_db};UID={user};PWD={password};"
    
    try:
        conn = pyodbc.connect(db_conn_str)
        cursor = conn.cursor()
        
        # Check and create department table
        cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'department'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE department (
                    id INT PRIMARY KEY,
                    name VARCHAR(255)
                )
            """)
            cursor.execute("INSERT INTO department (id, name) VALUES (1, 'HR'), (2, 'Engineering'), (3, 'Sales')")
            
        # Check and create employee table
        cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'employee'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE employee (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    department_id INT,
                    salary DECIMAL(10, 2)
                )
            """)
            cursor.execute("""
                INSERT INTO employee (id, name, department_id, salary) 
                VALUES 
                (1, 'Alice', 1, 60000), 
                (2, 'Bob', 2, 80000), 
                (3, 'Charlie', 2, 85000),
                (4, 'David', 3, 70000)
            """)
            
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to initialize tables: {e}")
        return False
