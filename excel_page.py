import streamlit as st
import pandas as pd
import pyodbc
import re
import show_table
import os
from dotenv import load_dotenv

# Function to check if a table exists in the database
def table_exists(cursor, table_name):
    cursor.execute(f"""
        SELECT * 
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{table_name}'
    """)
    return cursor.fetchone() is not None

# Function to create the table dynamically based on DataFrame structure
def create_table(cursor, df, table_name):
    columns = []
    for column in df.columns:
        # Use a simple heuristic to decide the SQL data type based on column data types
        if pd.api.types.is_integer_dtype(df[column]):
            dtype = "INT"
        elif pd.api.types.is_float_dtype(df[column]):
            dtype = "FLOAT"
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            dtype = "DATETIME"
        else:
            dtype = "VARCHAR(255)"
        
        # Append column definition to the list
        columns.append(f"[{column}] {dtype}")
    
    columns_str = ", ".join(columns)

    # SQL query to create the table
    create_query = f"""
        CREATE TABLE {table_name} (
            {columns_str}
        )
    """
    cursor.execute(create_query)

# Function to upload data to SQL Server
def upload_excel_to_sql(df, table_name):
    try:
        load_dotenv(dotenv_path=r".\.gitignore\.env")
        # Clean up column names: rename 'Unnamed' columns and strip extra spaces
        df.columns = [re.sub(r'Unnamed:\s*\d+', f"Column_{i}", col).strip() for i, col in enumerate(df.columns)]

        # Remove any columns that are completely empty
        df = df.dropna(axis=1, how='all')

        # Connect to SQL Server using Windows Authentication (Trusted Connection)
        rds_endpoint = st.secrets["MSSQL"]["host"]
        database = st.secrets["MSSQL"]["db_excel"]
        username = st.secrets["MSSQL"]["user"]
        password = st.secrets["MSSQL"]["password"]

        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={rds_endpoint};DATABASE={database};UID={username};PWD={password};"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # If the table does not exist, create it
        if not table_exists(cursor, table_name):
            st.write(f"Table '{table_name}' does not exist. Creating the table...")
            create_table(cursor, df, table_name)
            st.write(f"Table '{table_name}' created successfully.")

        # Insert DataFrame data into the SQL Server table
        for index, row in df.iterrows():
            sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['?' for _ in df.columns])})"
            cursor.execute(sql, tuple(row))

        # Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        st.success(f"Data from the Excel file has been uploaded to the '{table_name}' table in the '{database}' database.")
        return True
    except Exception as e:
        st.error(f"Error uploading data to SQL Server: {e}")

# Streamlit app UI
def get_excel():
    # Upload Excel file and insert data into DB
    st.subheader("Upload Excel File to Database")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        try:
            # Try to read all sheets as a dictionary
            sheets = pd.read_excel(uploaded_file, engine="openpyxl", sheet_name=None)  # This reads all sheets

            # Display the available sheet names (keys of the dictionary)
            sheet_names = list(sheets.keys())
            st.write("Available sheets:", sheet_names)

            # Ask the user to select a sheet
            selected_sheet = st.selectbox("Select a sheet to preview", sheet_names)

            # Retrieve the DataFrame for the selected sheet
            df = pd.DataFrame(sheets[selected_sheet])

            # Display the first few rows of the selected sheet
            st.write(f"Preview of the '{selected_sheet}' sheet:")
            st.dataframe(df.head())

            # Input for SQL Server credentials
            #st.subheader("SQL Server Credentials")
            
            table_name = st.text_input("Enter table name to store data", "testing")  # Make sure to use the correct table name

            # Button to trigger upload
            if st.button("Upload to SQL Server"):
                # Upload data to SQL Server
                return upload_excel_to_sql(df, table_name)
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")

